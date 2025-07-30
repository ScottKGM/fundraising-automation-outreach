
import gspread
from oauth2client.service_account import ServiceAccountCredentials

    
def get_leads(sheet_url: str) -> list[dict]:
    """
    Fetches leads from a Google Sheet.
    """

    scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).sheet1
    rows = sheet.get_all_records() 

    leads = []
    for i, row in enumerate(rows, start=2):
        if row.get("status") != "Sent":
            status_cell = f"H{i}"
            lead = {
                "owner_name": row.get("Name", "None"),
                "business_name": row.get("Business Name"),
                "email": row.get("Email Address"),
                "phone": row.get("Phone Number"),
                "website": row.get("website") 
            }
            if lead["email"] and lead["email"].strip():
                leads.append((lead, status_cell))

    return leads


def generate_prompt(lead: dict) -> str:

    
    return f"""
You are an AI email assistant helping a high school student write professional outreach emails on behalf of their HOSA club (Future Health Professionals).
The purpose of the email is to politely follow up with local businesses that were previously approached in-person about sponsoring or donating to the HOSA club.
The tone should be friendly, respectful, and professional — written from the perspective of a high school student who genuinely appreciates the business's time and potential support.

This is some backround information about our club:

Who We Are: HOSA- Future Health Professionals is a nationally recognized, student-led organization dedicated to empowering the next generation of medical professionals. At Kingwood High School, HOSA supports over 400 student members to explore careers in healthcare through hands-on experiences, competitive events, and leadership development.
Our Mission: We provide students with opportunities to compete, lead, and grow. Our members attend Area, State, and International conferences where they showcase their knowledge, sharpen their skills, and learn directly from industry professionals. However, our district does not fund these transformative opportunities.
Why We Need Support: That’s where you come in. Your sponsorship helps cover the cost of travel, lodging, registration fees, and more, removing financial barriers for students who dream of serving others. These are tomorrow’s nurses, doctors, therapists, EMTs, and researchers. The people who will one day take care of your family, your neighbors, and you.

You will be given the following structured information:
- Business Name: {lead['business_name']}
- Contact Person Name: {lead['owner_name']}
- Business Website: {lead['website']}
- Contact Email: {lead['email']}

If the contact person name is "None", do not include a name in the greeting.

Your task is to:
1. Write a personalized follow-up email using the above data
2. Briefly reintroduce the student (Scott Kelly) and the HOSA club (Kingwood High School HOSA)
3. Mention the previous in-person visit (lightly)
4. Kindly ask whether they’re interested or able to sponsor/donate
4a. Personalize the message:
- Naturally mention the business name (e.g., “It was great stopping by {lead['business_name']}” or “We really admire how {lead['business_name']} serves our community.”)
- If an owner name is provided, use it once in a friendly way (e.g., “Dana, your support would mean a lot…”)
- If the business is related to healthcare, wellness, education, or community services, highlight how their mission aligns with HOSA’s goals of training future healthcare professionals.

5. Provide the details for the following sponsorship packages:

WHITE – $100 Donation
Social media shoutout
Printed recognition sign


BLUE – $250
Social media shoutout
Printed recognition sign


MAROON – $500
Social media shoutout
Printed recognition sign
Guest speaker opportunity at one General Meeting
Logo featured on event t-shirts


SILVER – $750
Social media video shoutout
Printed recognition sign
Guest speaker opportunity at one General Meeting
Logo featured on event t-shirts


GOLD – $1,000+
Social media video shoutout
Framed recognition sign
Guest speaker opportunity at two General Meetings
Logo featured on HOSA t-shirts
Booth space at a Kingwood HOSA community event


6. Offer to provide more info or answer questions
7. Include a professional closing and sign-off

The objective of this email is to gently persuade the business owner to consider donating or sponsoring our high school HOSA chapter.

This is an example email you can base the message on:

\"\"\"
Hi Dr. Patel,

I hope you're doing well! My name is Scott, and I’m part of the HOSA chapter at Kingwood High School — a student-led organization focused on preparing future healthcare professionals.

We spoke recently about the possibility of your business sponsoring our chapter, and I wanted to follow up to see if you might still be interested. Your support helps over 400 students explore careers in medicine through competitions, conferences, and leadership training. Sponsorships cover important costs like travel, lodging, and event registration — and they make a huge difference for students like me who dream of serving others.

We offer multiple sponsorship levels with benefits like your logo placed on our t-shirts and shoutouts on social media. If you’d like more information or would like to help students heal the world today, I’d be happy to share everything you need.

Attached below is an outline of our sponsorship levels and how you can sponsor today!

Thank you again for your time and consideration!

Best regards,  
Scott Kelly  
Kingwood High School HOSA
\"\"\"

Please note:

- This email will be sent personally by Scott Kelly from his own email account.
- A sponsorship flyer image and a donation QR code will be attached below the message.
- The email body should mention that these resources are included for convenience, but do not include any image or file placeholders.
- Do not add links or fake contact info — just reference the flyer and QR code naturally in the body.
- Keep the email under 250-words
- Do not generate a Subject, only generate the text body


"""

import openai
import os

client = openai

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_email(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[

            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content.strip()


    
import smtplib
from email.message import EmailMessage

def send_email(to_adress: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = "Partner with Kingwood HOSA: Empower Student Health Careers"
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"] = to_adress
    msg.set_content(body)

    with open("hosa-flyer.pdf", "rb") as f:
        file_data = f.read()
        file_name = f.name
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_APP_PASSWORD"))
        smtp.send_message(msg)


scotts_email = "cpt.scottbk@gmail.com"


if __name__ == "__main__":
    SHEET_URL = "https://docs.google.com/spreadsheets/d/15XUXXHHf6d9NqdwNbkRhHQYdrjfOd6zCST8F2Na-X7A"
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    sheet = gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)).open_by_url(SHEET_URL).sheet1
    leads = get_leads(SHEET_URL)
    for lead, status_cell in leads:
        prompt = generate_prompt(lead)
        body = generate_email(prompt)
        print(f"TO: {lead['email']}\n")
        print(body)
        print("-" * 80)
        send_email(lead["email"], body)

        sheet.update(range_name=status_cell, values=[["Sent"]])
        

