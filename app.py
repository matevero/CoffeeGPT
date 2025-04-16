from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from dotenv import load_dotenv

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    print("📥 Mensagem recebida no webhook!")
    print("🔍 request.values:", request.values)  # <-- Adicionado aqui

    incoming_msg = request.values.get('Body', '').strip()


# Carrega variáveis do .env
load_dotenv()
print("Chave da OpenAI:", os.getenv("OPENAI_API_KEY"))

# Chave da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("🚨 A chave da OpenAI não foi carregada!")
else:
    print("🔑 Chave da OpenAI carregada com sucesso!")


# Cria o app Flask
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    print("📥 Mensagem recebida no webhook!")  # <-- ESSENCIAL PRA VER SE TÁ CHEGANDO
    incoming_msg = request.values.get('Body', '').strip()

    response = MessagingResponse()
    msg = response.message()

    try:
        # Envia a pergunta pra IA
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é o Zé do Café, um especialista simpático em café e agricultura."},
                {"role": "user", "content": incoming_msg}
            ]
        )

        reply = completion.choices[0].message.content
        print("🤖 Resposta da OpenAI:", reply)
        msg.body(reply)

    except Exception as e:
        print("❌ Erro na cabeça do Zé:", e)
        msg.body("Eita, deu ruim aqui com a cabeça do Zé... tenta de novo depois 😅")

    return str(response)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

