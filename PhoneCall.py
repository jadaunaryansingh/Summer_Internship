import os
from twilio.rest import Client

# Load sensitive data from environment variables
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
acc_token = os.environ.get("TWILIO_AUTH_TOKEN")
to_number = os.environ.get("TWILIO_TO_NUMBER")
from_number = os.environ.get("TWILIO_FROM_NUMBER")

# Initialize the client
client = Client(account_sid, acc_token)

# Make the call
call = client.calls.create(
    twiml='<Response><Say>Hi, this is a Python call</Say></Response>',
    to=to_number,
    from_=from_number
)
