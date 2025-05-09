from flask import Flask, request
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    print("📥 Mensagem recebida:", data)

    # Verifica se é uma mensagem de texto válida
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_msg = data["message"]["text"]

        try:
            # Envia a pergunta para a OpenAI
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                    "role": "system",
                    "content": "Você é o Zé do Café, um especialista simpático em café e agricultura."
                    },
                    {
                        "role": "user",
                        "content": user_msg
        }
    ]
)

            reply = chat_completion.choices[0].message.content
            print("🤖 Resposta do Zé:", reply)

            # Envia a resposta para o usuário no Telegram
            send_message(chat_id, reply)

        except Exception as e:
            print("❌ Erro:", e)
            send_message(chat_id, "Eita, deu ruim aqui com a cabeça do Zé... tenta de novo depois 😅")

    return "ok", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests



