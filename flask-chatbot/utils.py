import datetime

from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message


class SenderAgent(Agent):
    class InformBehav(PeriodicBehaviour):
        async def run(self):

            if self.agent.has_message :
                print(f"SenderAgent: running at {datetime.datetime.now().time()}: {self.counter}")
                
                msg = Message(to=self.agent.recv_jid)  # Instantiate the message

                msg.set_metadata(
                    "performative", "inform"
                )  # Set the "inform" FIPA performative
                msg.body = str(f"{self.agent.message_to_send}")

                await self.send(msg)

                print("SenderAgent: Message sent!")

                self.counter += 1

                msg = await self.receive(timeout=10)
                
                if msg:
                    print("SenderAgent: Response Message received: {}".format(msg.body))
                    if self.agent.to_send:
                        self.agent.response_classification_message = msg.body
                    else:
                        self.agent.response_extraction_message = msg.body
                else:
                    print("SenderAgent: Did not received any response message after 10 seconds")
                
                self.agent.has_message = False

        async def on_end(self):
            # stop agent from behaviour
            await self.agent.stop()

        async def on_start(self):
            self.counter = 0

    async def setup(self):
        print(f"SenderAgent: started at {datetime.datetime.now().time()}")
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
        b = self.InformBehav(period=2, start_at=start_at)
        #b = self.InformBehav()
        self.add_behaviour(b)
    
    def __init__(self, *args, **kwargs):
        self.recv_jid = None
        self.has_message = False
        self.to_send = True
        self.message_to_send = ""
        self.response_extraction_message = ""
        self.response_classification_message = ""
        super().__init__(*args, **kwargs)
    
    def send_message(self, recv_jid, message_to_send, to_send=True):
        self.recv_jid = recv_jid
        self.has_message = True
        self.message_to_send = message_to_send
        self.to_send = to_send

    def get_extraction_message(self):
        return self.response_extraction_message
    
    def get_classification_message(self):
        return self.response_classification_message