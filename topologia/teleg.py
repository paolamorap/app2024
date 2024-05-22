import telebot

# Token de tu bot de Telegram
TOKEN = '6719870472:AAFerw5_cbcI1w_3kMqfqw963cwQYTIrcP8'

# ID de chat al que quieres enviar el mensaje
chat_id = -4179209636

# Inicializar el bot con tu token
bot = telebot.TeleBot(TOKEN)

# Función para enviar mensaje
def enviar_mensaje(message):
    try:
        bot.send_message(chat_id, message)
        print("Mensaje enviado exitosamente.")
    except Exception as e:
        print("Ocurrió un error al enviar el mensaje:", e)
