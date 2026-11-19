# Stylist and Barber Ops Manager

A free Grok Bot template and agent skills for solo stylists and barbers who rent a suite.

Know what you actually made this week, after rent and product. Have your receipts sorted before anyone asks. Be told when your color is running low. Your records live in your own Google Drive.

## What you get

- **A Monday note.** Every Monday morning: what you made last week after rent and costs, and how much to set aside for taxes at the percentage you chose.
- **Receipts, filed.** Send a photo of a receipt in chat. It is filed in your Drive and logged in your Sheet. If a receipt is blurry or the numbers don't add up, it goes on a Review list for you. It never logs a number it couldn't read.
- **Your sales in one place.** Upload a report from Square, GlossGenius, Vagaro or Booksy, or any CSV or Excel file. The first time, the bot checks with you what each column means.
- **A mileage log** for house calls and events, at the per-mile rate you set.
- **Reminders on your tax dates.** Type in the dates you want to be reminded on, and the bot reminds you that morning. It never works out a date or an amount.
- **Low-stock alerts** for color and retail product, with who you usually buy from.

## Set it up in 8 steps or fewer

You need a Grok Bot account and a Google account.

1. Copy the Stylist and Barber Ops Manager template (link added at launch) into your own Grok Bot.
2. Tell the bot your business name.
3. Connect Google Drive and Google Sheets.
4. The bot creates a folder and one Sheet in your Drive.
5. Choose your set-aside percentage, your rent, and whether you want a mileage log and the rate to use. If you want reminders on estimated-tax dates, type the dates in.
6. Pick your booking app: Square, GlossGenius, Vagaro, Booksy or Other. Export a report from it and upload it in chat.
7. Add the color and retail items you want to watch, or skip this and add them later.
8. Send one receipt photo. Check that the vendor, date and total match the paper.

## Your original report files

The bot keeps the original of every report you upload in a Reports folder in your own Google Drive. The originals may hold client names, because that is whatever your booking app put in the file. They stay in your own Drive. The bot does not copy client names into your Sheet.

## Tips

- Send receipt photos flat and in good light.
- Export sales reports, not client lists. You don't need to upload your client list, and the bot ignores it.
- Never type a booking-app password into the chat. The bot never asks for one.

## What it won't do

- It will not move money, pay anyone or file anything with a tax agency.
- It will not order product. It tells you what's low and you decide.
- It will not give tax advice. The set-aside is a reminder at the number you chose. Your tax preparer can tell you what's right for you.
- It will not work out, look up or suggest an estimated-tax date or amount. It only reminds you on the dates you type in.
- It will not guess a number it could not read.
- It will not decide whether a trip or a purchase is deductible.

## What's in this repo

- `skills/stylist-getting-started/SKILL.md`: the first-run setup the bot walks you through.
- `skills/stylist-books/SKILL.md`: the weekly work. It covers receipts, booking-app reports, the Monday note, mileage, your tax-date reminders and low-stock alerts.

To use the skills in your own Grok Bot without the template, add both files as skills, then ask the bot to run `stylist-getting-started`.

## Not affiliated

Square, GlossGenius, Vagaro and Booksy are named only to say which exports the bot can read. This project is not affiliated with or endorsed by any of them.

## License

MIT. Stylist and Barber Ops Manager is free. Your records stay in your own Google Drive.
