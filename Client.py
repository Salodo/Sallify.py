from pyngrok import ngrok
url = ngrok.connect(5000).public_url

from twilio.rest import Client
client = Client()

# set the SMS webhook
client.incoming_phone_numbers.list(phone_number=NUMBER)[0].update(
    sms_url=SMS_URL)

# set the voice webhook
client.incoming_phone_numbers.list(phone_number=NUMBER)[0].update(
    voice_url=VOICE_URL)

# set both webhooks together!
client.incoming_phone_numbers.list(phone_number=NUMBER)[0].update(
    sms_url=SMS_URL, voice_url=VOICE_URL)