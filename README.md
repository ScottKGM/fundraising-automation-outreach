# HOSA Sponsorship Emailer

Automated outreach tool to send personalized follow-up emails to local businesses for HOSA sponsorships.

##  What It Does

- Reads a list of business leads from a Google Sheet
- Generates personalized email content using OpenAI
- Sends emails with a sponsorship flyer attached
- Updates the Google Sheet to mark which contacts have been emailed

## Tech Stack

- Python
- Google Sheets API via `gspread`
- OpenAI API (`gpt-3.5-turbo`)
- Gmail SMTP
- `.env` for secrets (not included in repo)
