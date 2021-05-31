from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

status = 0

app = Flask(__name__)

english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("chatterbot.corpus.english")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    global status
    userText = request.args.get('msg')

    if( userText == "add"):
        status = 1
        return str("Agrega la nueva noticia")
    
    if( userText == "news"):
        status = 0
        return str("Mostrando nueva noticia")

    if( userText == "exit"):
        status = 0
        return str("Reiniciando status del bot")
    
    if( status == 1):
        status = 0
        return str("Noticia Enviada para clasificar y Extraer información")

    if (status == 0):
        return str(english_bot.get_response(userText))


if __name__ == "__main__":
    app.run()
