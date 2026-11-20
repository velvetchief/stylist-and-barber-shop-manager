# Stylist and Barber Shop Manager

A free [Grok Bot template](https://x.ai/bot/GAJk-Smtnl-Dv7xChVpMu) and agent skills for solo stylists and barbers who rent a suite.

Know what you actually made this week, after rent and product. Know how full your book is and which clients come back. Have your receipts sorted before anyone asks. Be told when your color is running low and when a new review lands. Your records live in your own Google Drive.

## What you get

- **A Monday note.** Every Monday morning: what you made last week after rent and costs, and how much to set aside for taxes at the percentage you chose.
- **Receipts, filed.** Send a photo of a receipt in chat. It is filed in your Drive and logged in your Sheet. If a receipt is blurry or the numbers don't add up, it goes on a Review list for you. It never logs a number it couldn't read.
- **Your sales in one place.** Upload a report from Square, GlossGenius, Vagaro or Booksy, or any CSV or Excel file. The first time, the bot checks with you what each column means.
- **A mileage log** for house calls and events, at the per-mile rate you set.
- **Reminders on your tax dates.** Type in the dates you want to be reminded on, and the bot reminds you that morning. It never works out a date or an amount.
- **Low-stock alerts** for color and retail product, with who you usually buy from.

## Your week and your clients

Turn these on at setup, or later. Each one is optional.

- **Your week at a glance.** The bot reads the Google calendar your booking app syncs to and tells you what is booked, how many hours, and how full your open hours are. It reads the calendar and never changes it. Square, GlossGenius and Vagaro can sync their appointments to Google Calendar. Booksy stylists upload their report instead.
- **The numbers on your clients.** Upload an appointment report from Square, GlossGenius, Vagaro or Booksy, and the bot works out your rebook rate, no-shows, cancellations, new and returning clients, average ticket and how full your book is, week by week. Square stylists can skip the upload. Only totals go in your Sheet. No client names, emails or phone numbers are saved.
- **Visits to your booking page.** With Google Analytics on your website, the bot shows visits and clicks on your booking link next to your new bookings when the bot can see them, day by day.
- **Square changes, with your yes.** Square Appointments stylists can ask the bot to book, move or cancel an appointment, or change a service price. The bot shows you the exact change first and does it only after you say yes to that one change.
- **Google Business Profile (optional).** The bot shows how people find you on Google and checks for new reviews twice a day. Each new review comes with a reply ready for you to read. Nothing is posted until you say yes. Google gives access to approved applicants only, and your profile must be verified for at least 60 days and list a website.

## Every change is yours to approve

A booking, a price, a review reply, a post or new hours reaches your clients or the public. For each one the bot writes the exact change, shows it to you, and waits for your yes. One yes covers one change. The bot never changes anything on a schedule, and it never messages your clients.

## Set it up in 9 steps or fewer

You need a Grok Bot account and a Google account.

1. Copy the [Stylist and Barber Shop Manager template](https://x.ai/bot/GAJk-Smtnl-Dv7xChVpMu) into your own Grok Bot.
2. Tell the bot your business name.
3. Connect Google Drive and Google Sheets.
4. The bot creates a folder and one Sheet in your Drive.
5. Choose your set-aside percentage, your rent, and whether you want a mileage log and the rate to use. If you want reminders on estimated-tax dates, type the dates in.
6. Pick your booking app: Square, GlossGenius, Vagaro, Booksy or Other. Export a report from it and upload it in chat.
7. Add the color and retail items you want to watch, or skip this and add them later.
8. Pick the optional add-ons you want: your week, client numbers, website visits, Square changes, Business Profile.
9. Send one receipt photo. Check that the vendor, date and total match the paper.

## Your original report files

The bot keeps the original of every report you upload in a Reports folder in your own Google Drive. The originals may hold client names, because that is whatever your booking app put in the file. They stay in your own Drive. The bot does not copy client names into your Sheet.

## Tips

- Send receipt photos flat and in good light.
- Export sales reports and appointment reports. You don't need to upload your client list, and the bot ignores it.
- Never type a password, token or key into the chat. The bot never asks for one. Square, Google Analytics and Google sign in on their own pages.

## What it won't do

- It will not move money, pay anyone or file anything with a tax agency.
- It will not order product. It tells you what's low and you decide.
- It will not give tax advice. The set-aside is a reminder at the number you chose. Your tax preparer can tell you what's right for you.
- It will not work out, look up or suggest an estimated-tax date or amount. It only reminds you on the dates you type in.
- It will not guess a number it could not read.
- It will not decide whether a trip or a purchase is deductible.
- It will not message your clients, block time on your calendar, or post anything on its own.
- It will not change a booking, a price, a review reply or your hours without your yes to that one change.
- It will not save a client's name, email or phone number in your Sheet.

## What's in this repo
- `skills/stylist-getting-started/SKILL.md`: the first-run setup the bot walks you through, including the add-on choices.
- `skills/stylist-books/SKILL.md`: the weekly work. It covers receipts, booking-app reports, the Monday note, mileage, your tax-date reminders and low-stock alerts.
- `skills/stylist-schedule-funnel/SKILL.md`: your week from Google Calendar, the client numbers, and website visits from Google Analytics. `stylist_ops.py` in the same folder holds the exact calculations.
- `skills/stylist-square/SKILL.md`: reading Square bookings and making changes you approve one at a time.
- `skills/stylist-business-profile/SKILL.md`: Google Business Profile numbers and new-review drafts.

To use the skills in your own Grok Bot without the template, add every folder under `skills/` as a skill, then ask the bot to run `stylist-getting-started`.

## Not affiliated

Square, GlossGenius, Vagaro, Booksy and Google are named only to say which exports and connections the bot can use. This project is not affiliated with or endorsed by any of them.

## License

MIT. Stylist and Barber Shop Manager is free. Your records stay in your own Google Drive.
