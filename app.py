from flask import Flask, request
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests

# Carrega variáveis do .env
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

client = OpenAI(api_key=openai_key)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    print("📨 Mensagem recebida:", data)

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_msg = data["message"]["text"]

        try:
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é o Zé do Café, um especialista simpático em café e agricultura."},
                    {"role": "user", "content": user_msg}
                ]
            )

            reply = chat_completion.choices[0].message.content
            print("🤖 Resposta do Zé:", reply)

            # Envia a resposta pro Telegram
            send_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
            requests.post(send_url, json={"chat_id": chat_id, "text": reply})

        except Exception as e:
            print("❌ Deu ruim na cabeça do Zé:", e)

    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

