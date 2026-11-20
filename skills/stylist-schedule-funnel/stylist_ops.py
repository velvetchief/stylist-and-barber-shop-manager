#!/usr/bin/env python3
"""Reference calculations for the Stylist and Barber Shop Manager skills.

Global option: --today YYYY-MM-DD (before the subcommand) fixes the date for tests.
Subcommands (all print JSON, none writes anywhere but stdout):
  square    Square bookings JSON (API pages)            -> weekly funnel aggregates
  uploads   appointment export (csv/xlsx) + column map  -> weekly funnel aggregates
  calendar  Google Calendar list_events JSON            -> booked hours per week
  ga4       GA4 runReport JSON (sessions, clicks)       -> weekly traffic row
  gbp-perf  Business Profile fetchMultiDailyMetricsTimeSeries JSON -> weekly row
  reviews   reviews.list JSON + IDs already seen        -> new reviews to draft for

Client identifiers are hashed in memory with a random per-run salt and are never
printed. Output holds counts, rates, hours and dates only.
"""
from zoneinfo import ZoneInfo
import argparse, csv, hashlib, json, os, sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
SALT = os.urandom(16)
TODAY = None  # set by --today for repeatable tests


def h(value):
    return hashlib.sha256(SALT + str(value).strip().lower().encode()).hexdigest()[:16]


def monday(d):
    return d - timedelta(days=d.weekday())


def money(s):
    s = str(s or "").replace("$", "").replace(",", "").strip()
    if s in ("", "-"):
        return None
    neg = s.startswith("(") and s.endswith(")")
    v = float(s.strip("()"))
    return -v if neg else v


def parse_date(s, fmts):
    s = str(s).strip()
    for f in fmts:
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    raise ValueError(f"unreadable date: {s!r}")


def parse_clock(s):
    s = str(s or "").strip()
    for f in ("%H:%M", "%I:%M %p", "%I:%M%p", "%H:%M:%S"):
        try:
            t = datetime.strptime(s, f)
            return t.hour * 60 + t.minute
        except ValueError:
            pass
    return None


def parse_duration(s):
    """Minutes from '45', '45 min', '1h 30min', '1 h 30 min' or '1:30'."""
    import re
    s = str(s).strip().lower()
    if re.fullmatch(r"\d+(\.\d+)?", s):
        return int(float(s))
    m = re.fullmatch(r"(\d+):(\d{2})", s)
    if m:
        return int(m[1]) * 60 + int(m[2])
    m = re.fullmatch(r"(?:(\d+)\s*h(?:ours?|rs?)?)?\s*(?:(\d+)\s*m(?:in(?:ute)?s?)?)?", s)
    if m and (m[1] or m[2]):
        return int(m[1] or 0) * 60 + int(m[2] or 0)
    raise ValueError(f"unreadable duration: {s!r}")


def read_rows(path, sheet=None):
    if path.lower().endswith((".xlsx", ".xlsm")):
        import openpyxl
        ws = openpyxl.load_workbook(path, data_only=True)[sheet] if sheet else openpyxl.load_workbook(path, data_only=True).worksheets[0]
        it = ws.iter_rows(values_only=True)
        head = [str(c).strip() if c is not None else "" for c in next(it)]
        out = []
        for r in it:
            if all(c is None for c in r):
                continue
            row = {}
            for k, v in zip(head, r):
                if isinstance(v, datetime):
                    v = v.strftime("%Y-%m-%d %H:%M")
                row[k] = "" if v is None else str(v)
            out.append(row)
        return head, out
    with open(path, newline="", encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        return rd.fieldnames, list(rd)


def merged_minutes(spans):
    """Total minutes covered by (start,end) spans, overlaps counted once."""
    total, cur_s, cur_e = 0, None, None
    for s, e in sorted(spans):
        if cur_e is None or s > cur_e:
            if cur_e is not None:
                total += cur_e - cur_s
            cur_s, cur_e = s, e
        else:
            cur_e = max(cur_e, e)
    if cur_e is not None:
        total += cur_e - cur_s
    return total


def open_hours(spec):
    out = {}
    for part in (spec or "").split(","):
        if "=" in part:
            k, v = part.split("=")
            out[k.strip().lower()[:3]] = float(v)
    return out


def week_open_hours(oh, ws):
    return sum(oh.get(DAYS[i], 0) for i in range(7)) if oh else None


# ---------------------------------------------------------------- uploads
def cmd_uploads(a):
    m = json.load(open(a.map))
    head, rows = read_rows(a.file, m.get("sheet"))
    c = m["columns"]
    for role in ("date", "status"):
        if c[role] not in head:
            sys.exit(f"column for {role!r} not in file: {c[role]!r}")
    fmts = m.get("date_formats", ["%Y-%m-%d"])
    smap = {}
    for kind, names in m["status_map"].items():
        for n in names:
            smap[n.strip().lower()] = kind
    new_true = {x.lower() for x in m.get("new_client_true", [])}
    recs, unknown = [], defaultdict(int)
    for r in rows:
        st = smap.get(str(r[c["status"]]).strip().lower())
        if st is None:
            unknown[r[c["status"]]] += 1
            continue
        dt = parse_date(r[c["date"]], fmts)
        start = dt.hour * 60 + dt.minute
        if c.get("start") and c["start"] in head:
            ck = parse_clock(r[c["start"]])
            if ck is not None:
                start = ck
        if c.get("duration_min") and r.get(c["duration_min"], "") != "":
            dur = parse_duration(r[c["duration_min"]])
        elif c.get("end") and c["end"] in head and parse_clock(r[c["end"]]) is not None:
            dur = parse_clock(r[c["end"]]) - start
        else:
            dur = None
        key = ""
        for col in c.get("client", []):
            if col in head and str(r.get(col, "")).strip():
                key = str(r[col]).strip()
                break
        price = money(r.get(c["price"])) if c.get("price") in head else None
        tip = money(r.get(c["tip"])) if c.get("tip") in head else None
        flag = None
        if c.get("new_client") in head:
            flag = str(r[c["new_client"]]).strip().lower() in new_true
        recs.append(dict(day=dt.date(), start=start, dur=dur, status=st, who=h(key) if key else None,
                         price=price, tip=tip, new_flag=flag))
    if unknown:
        sys.exit("status values not in the map, ask the stylist: " + json.dumps(unknown))
    weekly(recs, m.get("app"), a.open_hours, a.count_tips)


def weekly(recs, app, open_hours_spec, count_tips, sales_by_week=None, extra=None):
    a = argparse.Namespace(open_hours=open_hours_spec, count_tips=count_tips)
    today = date.fromisoformat(TODAY) if TODAY else date.today()
    m = {"app": app}
    if not recs:
        sys.exit("no rows")
    last_day = max(r["day"] for r in recs)
    by_week = defaultdict(list)
    for r in recs:
        by_week[monday(r["day"])].append(r)
    first_seen = {}
    for r in sorted(recs, key=lambda r: (r["day"], r["start"])):
        if r["status"] == "completed" and r["who"] and r["who"] not in first_seen:
            first_seen[r["who"]] = monday(r["day"])
    oh = open_hours(a.open_hours)
    out, caveats = [], set()
    basis = "app flag" if any(r["new_flag"] is not None for r in recs) else "first visit in this file"
    for ws in sorted(by_week):
        rs = by_week[ws]
        we = ws + timedelta(days=6)
        comp = [r for r in rs if r["status"] == "completed"]
        ns = sum(r["status"] == "no_show" for r in rs)
        cx = sum(r["status"] == "cancelled" for r in rs)
        scheduled = len(comp) + ns + cx
        seen = {r["who"] for r in comp if r["who"]}
        # new vs returning
        if basis == "app flag":
            newc = {r["who"] for r in comp if r["who"] and r["new_flag"]}
        else:
            newc = {w for w in seen if first_seen.get(w) == ws}
        # rebook
        mature = we + timedelta(days=28) <= last_day
        rebooked = None
        if mature and seen:
            rebooked = 0
            for w in seen:
                lastv = max((r["day"], r["start"]) for r in comp if r["who"] == w)
                later = any(r["who"] == w and r["status"] != "cancelled" and (r["day"], r["start"]) > lastv for r in recs)
                rebooked += later
        # ticket
        priced = [r for r in comp if r["price"] is not None]
        tot = sum(r["price"] + (r["tip"] or 0 if a.count_tips else 0) for r in priced)
        if sales_by_week is not None:
            sw = sales_by_week.get(ws.isoformat())
            priced = comp if sw is not None else []
            tot = sw or 0
        # hours: per day merged spans of non-cancelled, non-no-show-excluded? held slots = completed + no_show + upcoming
        held_min, no_dur = 0, 0
        byday = defaultdict(list)
        for r in rs:
            if r["status"] == "cancelled":
                continue
            if r["dur"] is None:
                no_dur += 1
                continue
            byday[r["day"]].append((r["start"], r["start"] + r["dur"]))
        held_min = sum(merged_minutes(v) for v in byday.values())
        oh_week = week_open_hours(oh, ws)
        out.append({
            "week_of": ws.isoformat(),
            "scheduled": scheduled, "completed": len(comp), "no_shows": ns, "cancellations": cx,
            "no_show_rate": round(ns / scheduled, 4) if scheduled else None,
            "cancellation_rate": round(cx / scheduled, 4) if scheduled else None,
            "clients_seen": len(seen), "new_clients": len(newc), "returning_clients": len(seen) - len(newc),
            "rebook_rate": round(rebooked / len(seen), 4) if rebooked is not None else None,
            "rebook_note": None if mature else "too recent: fewer than 28 days of data after this week",
            "average_ticket": round(tot / len(priced), 2) if priced else None,
            "completed_without_price": len(comp) - len(priced),
            "booked_hours": round(held_min / 60, 2),
            "open_hours": oh_week,
            "utilization": round(held_min / 60 / oh_week, 4) if oh_week else None,
            "rows_without_duration": no_dur,
            "rows_without_client": sum(1 for r in rs if not r["who"]),
            "new_client_basis": basis,
            "complete": we <= last_day and we < today,
        })
    json.dump({"source": m.get("app"), "data_through": last_day.isoformat(), **(extra or {}), "weeks": out}, sys.stdout, indent=1)
    print()


# ----------------------------------------------------------------- square
def cmd_square(a):
    """Square ListBookings/SearchBookings JSON (one or more pages) -> same weekly metrics."""
    pages = json.load(open(a.bookings))
    pages = pages if isinstance(pages, list) else [pages]
    today = date.fromisoformat(a.as_of)
    recs, skipped = [], defaultdict(int)
    for p in pages:
        for b in p.get("bookings", []):
            st = b["status"]
            start = datetime.fromisoformat(b["start_at"].replace("Z", "+00:00")).astimezone(ZoneInfo(a.tz))
            day = start.date()
            if st in ("CANCELLED_BY_CUSTOMER", "CANCELLED_BY_SELLER"):
                kind = "cancelled"
            elif st == "NO_SHOW":
                kind = "no_show"
            elif st == "ACCEPTED":
                kind = "completed" if day < today else "upcoming"
            elif st == "PENDING" and day >= today:
                kind = "upcoming"
            else:
                skipped[st] += 1
                continue
            dur = sum(sg.get("duration_minutes", 0) + sg.get("intermission_minutes", 0) for sg in b.get("appointment_segments", [])) or None
            recs.append(dict(day=day, start=start.hour * 60 + start.minute, dur=dur, status=kind,
                             who=h(b["customer_id"]) if b.get("customer_id") else None, price=None, tip=None, new_flag=None))
    created = defaultdict(int)
    for p in pages:
        for b in p.get("bookings", []):
            if b["status"] != "DECLINED":
                created[datetime.fromisoformat(b["created_at"].replace("Z", "+00:00")).astimezone(ZoneInfo(a.tz)).date().isoformat()] += 1
    sales = json.load(open(a.sales_by_week)) if a.sales_by_week else {}
    weekly(recs, "Square (API)", a.open_hours, False, sales_by_week=sales,
           extra={"rows_not_counted": dict(skipped), "bookings_created_by_day": dict(sorted(created.items())),
                  "note": "ACCEPTED bookings before today are counted as completed visits. Square has no completed status."})


# --------------------------------------------------------------- calendar
def cmd_calendar(a):
    ev = json.load(open(a.events))
    events = ev["events"] if isinstance(ev, dict) else ev
    oh = open_hours(a.open_hours)
    byday = defaultdict(list)
    counted = skipped = 0
    for e in events:
        if e.get("status") == "cancelled" or e.get("transparency") == "transparent" or "dateTime" not in e.get("start", {}):
            skipped += 1
            continue
        if any(x.get("self") and x.get("responseStatus") == "declined" for x in e.get("attendees", [])):
            skipped += 1
            continue
        s = datetime.fromisoformat(e["start"]["dateTime"].replace("Z", "+00:00"))
        en = datetime.fromisoformat(e["end"]["dateTime"].replace("Z", "+00:00"))
        # local wall-clock minutes in the event's own offset
        day = s.date()
        byday[day].append((s.hour * 60 + s.minute, s.hour * 60 + s.minute + int((en - s).total_seconds() // 60)))
        counted += 1
    weeks = defaultdict(lambda: {"booked_min": 0, "appointments": 0, "days": {}})
    for d, spans in sorted(byday.items()):
        w = weeks[monday(d)]
        mins = merged_minutes(spans)
        w["booked_min"] += mins
        w["appointments"] += len(spans)
        w["days"][d.isoformat()] = {"appointments": len(spans), "booked_hours": round(mins / 60, 2),
                                    "open_hours": oh.get(DAYS[d.weekday()]) if oh else None}
    res = []
    for ws, w in sorted(weeks.items()):
        ohw = week_open_hours(oh, ws)
        res.append({"week_of": ws.isoformat(), "appointments": w["appointments"],
                    "booked_hours": round(w["booked_min"] / 60, 2), "open_hours": ohw,
                    "utilization": round(w["booked_min"] / 60 / ohw, 4) if ohw else None, "days": w["days"]})
    json.dump({"events_counted": counted, "events_skipped": skipped, "weeks": res}, sys.stdout, indent=1)
    print()


# -------------------------------------------------------------------- ga4
def ga_rows(report):
    dims = [d["name"] for d in report.get("dimensionHeaders", [])]
    mets = [m["name"] for m in report.get("metricHeaders", [])]
    for r in report.get("rows", []):
        d = dict(zip(dims, (x["value"] for x in r["dimensionValues"])))
        d.update({k: float(v["value"]) for k, v in zip(mets, r["metricValues"])})
        yield d


def ymd(s):
    return date(int(s[:4]), int(s[4:6]), int(s[6:]))


def cmd_ga4(a):
    sess = json.load(open(a.sessions))
    clicks = json.load(open(a.clicks)) if a.clicks else None
    booking_domain = (a.booking_domain or "").lower()
    weeks = defaultdict(lambda: {"sessions": 0, "clicks": 0, "sources": defaultdict(float), "days": defaultdict(lambda: [0, 0])})
    for r in ga_rows(sess):
        d = ymd(r["date"])
        w = weeks[monday(d)]
        w["sessions"] += r["sessions"]
        w["sources"][r.get("sessionSource", "(unknown)")] += r["sessions"]
        w["days"][d.isoformat()][0] += r["sessions"]
    if clicks:
        for r in ga_rows(clicks):
            if r.get("outbound", "true") != "true":
                continue
            if booking_domain and r.get("linkDomain", "").lower() != booking_domain:
                continue
            d = ymd(r["date"])
            w = weeks[monday(d)]
            w["clicks"] += r["eventCount"]
            w["days"][d.isoformat()][1] += r["eventCount"]
    bk = defaultdict(int)
    if a.bookings_by_day:
        for k, v in json.load(open(a.bookings_by_day)).items():
            bk[monday(date.fromisoformat(k))] += v
    out = []
    for ws, w in sorted(weeks.items()):
        top = sorted(w["sources"].items(), key=lambda kv: -kv[1])[:3]
        out.append({"week_of": ws.isoformat(), "sessions": int(w["sessions"]),
                    "booking_link_clicks": int(w["clicks"]) if clicks else None,
                    "new_bookings_created": bk.get(ws) if a.bookings_by_day else None,
                    "top_sources": ", ".join(f"{k} {int(v)}" for k, v in top),
                    "by_day": {d: {"sessions": int(v[0]), "clicks": int(v[1])} for d, v in sorted(w["days"].items())}})
    json.dump({"weeks": out, "note": "by-day counts side by side; clicks are not completed bookings"}, sys.stdout, indent=1)
    print()


# ---------------------------------------------------------------- gbp-perf
def cmd_gbp_perf(a):
    data = json.load(open(a.file))
    weeks = defaultdict(lambda: defaultdict(int))
    for blk in data.get("multiDailyMetricTimeSeries", []):
        for s in blk.get("dailyMetricTimeSeries", []):
            met = s["dailyMetric"]
            for dv in s.get("timeSeries", {}).get("datedValues", []):
                dd = dv["date"]
                d = date(dd["year"], dd["month"], dd["day"])
                weeks[monday(d)][met] += int(dv.get("value", 0))  # omitted value means zero (Google docs)
    imp = [k for k in next(iter(weeks.values()), {}) if k.startswith("BUSINESS_IMPRESSIONS")]
    out = []
    for ws, m in sorted(weeks.items()):
        out.append({"week_of": ws.isoformat(),
                    "impressions": sum(v for k, v in m.items() if k.startswith("BUSINESS_IMPRESSIONS")),
                    "website_clicks": m.get("WEBSITE_CLICKS", 0), "calls": m.get("CALL_CLICKS", 0),
                    "direction_requests": m.get("BUSINESS_DIRECTION_REQUESTS", 0)})
    json.dump({"weeks": out}, sys.stdout, indent=1)
    print()


# ----------------------------------------------------------------- reviews
STARS = {"ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5}


def cmd_reviews(a):
    seen = set(json.load(open(a.seen))) if a.seen and os.path.exists(a.seen) else set()
    pages = json.load(open(a.reviews))
    pages = pages if isinstance(pages, list) else [pages]
    allr = [r for p in pages for r in p.get("reviews", [])]
    first_run = not seen
    new = []
    for r in allr:
        rid = r.get("reviewId") or r["name"].rsplit("/", 1)[-1]
        if rid in seen:
            continue
        new.append({"review_id": rid, "date": r["createTime"][:10], "stars": STARS[r["starRating"]],
                    "has_comment": bool(r.get("comment")), "already_replied": "reviewReply" in r,
                    # reviewer name is intentionally not carried into the result
                    })
    needs = [n for n in new if not n["already_replied"]]
    unanswered = len(needs) if first_run else None
    json.dump({"first_run": first_run, "unanswered_on_first_run": unanswered, "new_reviews": new,
               "to_draft": [] if first_run else [n["review_id"] for n in needs],
               "ids_to_store": [n["review_id"] for n in new]}, sys.stdout, indent=1)
    print()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    u = sub.add_parser("uploads"); u.add_argument("file"); u.add_argument("--map", required=True)
    u.add_argument("--open-hours"); u.add_argument("--count-tips", action="store_true"); u.set_defaults(f=cmd_uploads)
    q = sub.add_parser("square"); q.add_argument("bookings"); q.add_argument("--as-of", required=True); q.add_argument("--tz", default="UTC")
    q.add_argument("--open-hours"); q.add_argument("--sales-by-week"); q.set_defaults(f=cmd_square)
    c = sub.add_parser("calendar"); c.add_argument("events"); c.add_argument("--open-hours"); c.set_defaults(f=cmd_calendar)
    g = sub.add_parser("ga4"); g.add_argument("--sessions", required=True); g.add_argument("--clicks")
    g.add_argument("--booking-domain"); g.add_argument("--bookings-by-day"); g.set_defaults(f=cmd_ga4)
    b = sub.add_parser("gbp-perf"); b.add_argument("file"); b.set_defaults(f=cmd_gbp_perf)
    r = sub.add_parser("reviews"); r.add_argument("reviews"); r.add_argument("--seen"); r.set_defaults(f=cmd_reviews)
    p.add_argument("--today", help="YYYY-MM-DD, for repeatable tests")
    a = p.parse_args()
    global TODAY
    TODAY = a.today
    a.f(a)


if __name__ == "__main__":
    main()
