import time

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from classifier import ClassificationAgent
from extractions import ExtractionAgent
from flask import Flask, render_template, request
from spade import quit_spade
from utils import SenderAgent

status = 0

sender_jid = "dasiprojectsender@01337.io"
sender_passwd = "1q2w3e4r5t"

classification_jid = "dasiprojectclassifier@01337.io"
classification_passwd = "1q2w3e4r5t"

extraction_jid = "dasiprojectextraction@01337.io"
extraction_passwd = "1q2w3e4r5t"

classificationAgent = None
senderagent = None

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
    global senderagent
    global classification_jid
    global extraction_jid
    userText = request.args.get('msg')

    if( userText == "add"):
        status = 1
        return str("Please add the new news!")
    
    if( userText == "news"):
        status = 0
        result = "This is the new news!\n"
        result += "News!\n"
        return str(result)

    if( userText == "exit"):
        status = 0
        return str("Resetting chatbot status")
    
    if( status == 1):
        status = 0
        result = ""

        # classification
        senderagent.send_message(classification_jid, str(userText))
        time.sleep(2)
        result += senderagent.get_classification_message()

        time.sleep(2)
        result += "\n\n"

        # extraction
        senderagent.send_message(extraction_jid, str(userText), False)
        time.sleep(2)
        result += senderagent.get_extraction_message()
        # send_agent_message(senderagent, extraction_jid, str(userText))

        return str(result)

    if (status == 0):
        return str(english_bot.get_response(userText))


if __name__ == "__main__":

    classificationAgent = ClassificationAgent(sender_jid, classification_jid, classification_passwd)
    future_classification = classificationAgent.start()
    future_classification.result() # wait for receiver agent to be prepared.

    extractionAgent = ExtractionAgent(sender_jid, extraction_jid, extraction_passwd)
    future_extraction = extractionAgent.start()
    future_extraction.result() # wait for receiver agent to be prepared.

    senderagent = SenderAgent(sender_jid, sender_passwd)
    senderagent.start()

    try:
        app.run()

    except KeyboardInterrupt:
        # CTRL+C
        print("\nKeyboard interrupt")
    except:
        print("Another interruption")
    finally:
        quit_spade()
