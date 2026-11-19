---
name: stylist-getting-started
description: >-
  Use for the first conversation with a solo suite-renting hairstylist or
  barber who just installed the Stylist and Barber Ops Manager template:
  connect Drive and Sheets, create the folder and Sheet, set the tax
  set-aside percentage, rent, mileage rate and reminder dates, link their
  booking app, and schedule the Monday note.
---
# Getting started (solo stylist or barber)

Say in one line: "I keep your receipts, what you made, your miles and your product in your own Google Drive, and every Monday I tell you what you kept. You just chat with me." Then ask the questions below one at a time, and wait for each answer.

1. **Name.** Ask what to call the business. If they don't have one, use their own name. It names the Drive folder and the Sheet.
2. **Connect Google Drive and Google Sheets.** If they aren't connected, show the connect card. Wait until both work.
3. **Create the files.** Create the top folder `<Name> Books` with Receipts and Reports inside it. Then create one Sheet, `<Name> Books`. **Create the Sheet with the Google Drive connector, as a spreadsheet inside the top folder.** Don't create it with the Sheets connector: it saves it in the root of My Drive, and it can't be moved or deleted afterward. Once it exists, use the Sheets connector to add the tabs and headers:
   - Receipts: Date, Vendor, Category, Total, Paid with, Items, File, Status, Key, Added
   - Income: Date, Source, Type, Amount, Report file, Row key, Added
   - Mileage: Date, From, To, Purpose, Miles, Rate, Amount, How logged, Added
   - Stock and par: Item, Type, Unit, On hand, Par, Usual supplier, Last updated
   - Weekly notes: Week of, Money in, Costs, What you made, Set aside, After set-aside, Receipts in review
   - Settings: Setting, Value, Updated
   - Review: Date added, Type, File link, What's unclear, Status
   - Column maps: App, Report, Their column, Means, Confirmed on

   Read the folder back and show the stylist its link.
4. **Settings.** Ask these one at a time and write each answer to Settings with today's date. Never fill an answer in for them.
   - **Tax set-aside.** "What percentage do you want me to remind you to set aside each week?" Wait for a number. If they ask what to pick, say that's a question for their tax preparer, and that you'll use whatever number they choose. Then ask whether the percentage applies to what they made after costs, or to everything that came in. Say once: "This is a reminder at your number. It's not tax advice."
   - **Tips.** "Should I count tips in what you made?" Default yes if they have no preference.
   - **Rent.** "What do you pay for your suite, and is it weekly or monthly?" Wait for an amount.
   - **Mileage.** "Do you drive to clients or events and want a mileage log?" If yes, ask for the per-mile rate they want to use. If they don't know it, point them to https://www.irs.gov/tax-professionals/standard-mileage-rates and wait for the number they pick. If no, set Mileage to off.
   - **Estimated-tax reminders.** "Do you want me to remind you on dates for estimated tax payments? Type the dates you want, with a label for each, and tell me if each repeats every year." They can skip this. If they ask which dates to use, say that is a question for their tax preparer. Never suggest a date or an amount.
   - **Time zone** and the **time** they want the Monday note. Default 8:00 AM.
5. **Booking app.** Ask "Which app do you use for bookings and payments?" and offer Square, GlossGenius, Vagaro, Booksy and Other. Note the answer in Settings. Explain that they export a report from the app and upload it in chat. Give the steps for their app from the stylist-books skill. Never ask for an app password or key. On the first upload, run the column mapping from stylist-books and confirm it with them.
6. **Product (optional now).** Ask which color and retail items they want to watch, with a par for each and a usual supplier. They can type a list, upload a file, or skip and add items later. Write what they give into Stock and par.
7. **Routines.** Create a routine that runs the Monday note from the stylist-books skill at the chosen time, and reports to the stylist in this chat. If they typed estimated-tax reminder dates, create a second routine that runs each morning, checks Settings, and messages only on a date they typed. If Mileage is on, offer one more routine: a one-line Friday evening message, "Any drives to log this week?" Create it only if they say yes.
8. **Test.** Ask them to send one receipt photo now. When it's read, show the vendor, date and total, and ask whether they match the paper. If the photo couldn't be opened, ask for a flatter, brighter one.

Save the business name, booking app, time zone and the Monday time to memory. Never save keys, passwords or client details anywhere. Finish with a short summary of what's set up and what's still missing.
