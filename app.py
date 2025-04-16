from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
print("🔑 Chave da OpenAI:", os.getenv("OPENAI_API_KEY"))

# Inicializa cliente da OpenAI com nova sintaxe
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Cria o app Flask
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    print("📥 Mensagem recebida no webhook!")  # Confirma que chegou
    incoming_msg = request.values.get('Body', '').strip()

    response = MessagingResponse()
    msg = response.message()

    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é o Zé do Café, um especialista simpático em café e agricultura."},
                {"role": "user", "content": incoming_msg}
            ]
        )

        reply = chat_completion.choices[0].message.content
        print("🤖 Resposta do Zé:", reply)
        msg.body(reply)

    except Exception as e:
        print("❌ Deu ruim na cabeça do Zé:", e)
        msg.body("Eita, deu ruim aqui com a cabeça do Zé... tenta de novo depois 😅")

    return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


