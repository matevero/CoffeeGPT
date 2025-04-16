import os
from twilio.rest import Client
from dotenv import load_dotenv

from dotenv import load_dotenv
import os

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
to_number = os.getenv("DESTINATION_NUMBER")


# Carrega variáveis do arquivo .env
load_dotenv()

# Pega os dados do arquivo .env
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
to_number = os.getenv("DESTINATION_NUMBER")
print("SID:", account_sid)
print("Token:", auth_token)
print("Twilio Number:", twilio_number)
print("To Number:", to_number)

# Cria cliente do Twilio
client = Client(account_sid, auth_token)

# Envia a mensagem
message = client.messages.create(
    from_=twilio_number,
    body="☕ Olá! Aqui é o *Zé do Café*! Como posso te ajudar hoje?",
    to=to_number
)

print(f"Mensagem enviada com sucesso! SID: {message.sid}")
