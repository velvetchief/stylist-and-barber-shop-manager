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

1. **Names.** Ask for their suite name. If the suite has no name, use their own name. Then say "I'll call your folder and your Sheet <Suite name> Back Office. Want a different name?" Use what they pick for both. Hold the two names until the Settings tab exists in step 3. The default is only a default. Never hardcode a name.
2. **Connect Google Drive and Google Sheets.** If they aren't connected, show the connect card. Wait until both work.
3. **Create the files.** Create the top folder with the folder name they chose, with Receipts and Reports inside it. Don't create the YYYY-MM month folders now. The stylist-books skill creates each one the first time it's needed. Then create one Sheet with the Sheet name they chose. **Create the Sheet with the Google Drive connector, as a spreadsheet inside the top folder.** Don't create it with the Sheets connector: it saves it in the root of My Drive, and it can't be moved or deleted afterward. A new Sheet starts with one tab called Sheet1. Rename that tab to Receipts, and don't leave a Sheet1 behind. Then use the Sheets connector to add the other tabs and set the headers on all of them:
   - Receipts: Date, Vendor, Category, Total, Paid with, Items, File, Status, Key, Added
   - Income: Date, Source, Type, Amount, Report file, Row key, Added
   - Mileage: Date, From, To, Purpose, Miles, Rate, Amount, How logged, Added
   - Stock and par: Item, Type, Unit, Current stock, Par, Usual supplier, Last updated
   - Weekly notes: Week of, Money in, Costs, What you made, Set aside, After set-aside, Receipts in review
   - Settings: Setting, Value, Updated, Repeat yearly. Repeat yearly is filled in only on Reminder rows, with exactly Yes or No. It stays empty on every other row.
   - Review: Date added, Type, File link, What's unclear, Status
   - Column maps: App, Report, Their column, Means, Confirmed on

   Once the Settings tab exists, write two rows to it, with today's date: Folder name and Sheet name, set to the names they chose. Don't write them earlier. Then read the folder back and show the stylist its link.
4. **Settings.** Ask these one at a time and write each answer to Settings with today's date. Never fill an answer in for them.
   - **Tax set-aside.** "What percentage do you want me to remind you to set aside each week?" Wait for a number. If they ask what to pick, say that's a question for their tax preparer, and that you'll use whatever number they choose. Then ask whether the percentage applies to what they made after costs, or to everything that came in. Say once: "This is a reminder at your number. It's not tax advice."
   - **Tips.** "Should I count tips in what you made?" Default yes if they have no preference.
   - **Rent.** "What do you pay for your suite, and is it weekly or monthly?" Wait for an amount.
   - **Mileage.** "Do you drive to clients or events and want a mileage log?" If yes, ask for the per-mile rate they want to use. If they don't know it, point them to https://www.irs.gov/tax-professionals/standard-mileage-rates and wait for the number they pick. If no, set Mileage to off.
   - **Estimated-tax reminders.** "Do you want me to remind you on dates for estimated tax payments? Type the dates you want, with a label for each, and tell me if each repeats every year." They can skip this. For each date, read it back as a full date, for example "April 15, 2027, repeats every year. Right?", and write it only after they say yes. Store each one as a Reminder row in Settings, exactly as the stylist-books skill defines. If they ask which dates to use, say that is a question for their tax preparer. Never suggest a date or an amount.
   - **Time zone** and the **time** they want the Monday note. Default 8:00 AM.
5. **Booking app.** Ask "Which app do you use for bookings and payments?" and offer Square, GlossGenius, Vagaro, Booksy and Other. Note the answer in Settings. Explain that they export a report from the app and upload it in chat. Give the steps for their app from the stylist-books skill. Never ask for an app password or key. On the first upload, run the column mapping from stylist-books and confirm it with them.
6. **Product (optional now).** Ask which color and retail items they want to watch, with a par for each and a usual supplier. They can type a list, upload a file, or skip and add items later. Write what they give into Stock and par.
7. **Routines.** Create a routine that runs the Monday note from the stylist-books skill at the chosen time, and reports to the stylist in this chat. If they typed estimated-tax reminder dates, create a second routine that runs each morning, checks Settings, and messages only on a date they typed. If Mileage is on, offer one more routine: a one-line Friday evening message, "Any drives to log this week?" Create it only if they say yes.
8. **Test.** Ask them to send one receipt photo now. When it's read, show the vendor, date and total, and ask whether they match the paper. If the photo couldn't be opened, ask for a flatter, brighter one.

Save the suite name, the folder and Sheet names, booking app, time zone and the Monday time to memory. Never save keys, passwords or client details anywhere. Finish with a short summary of what's set up and what's still missing.
