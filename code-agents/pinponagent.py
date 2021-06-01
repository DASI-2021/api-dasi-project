import datetime
import time

from spade import quit_spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template


class SenderAgent(Agent):
    class InformBehav(PeriodicBehaviour):
    #class InformBehav(CyclicBehaviour):
        async def run(self):

            if self.agent.has_message :
                print(f"SenderAgent: running at {datetime.datetime.now().time()}: {self.counter}")
                
                msg = Message(to=self.agent.recv_jid)  # Instantiate the message

                msg.set_metadata(
                    "performative", "inform"
                )  # Set the "inform" FIPA performative
                msg.body = str(f"Hello word at {datetime.datetime.now().time()}: {self.counter}")

                await self.send(msg)

                print("SenderAgent: Message sent!")

                self.counter += 1

                msg = await self.receive(timeout=10)
                
                if msg:
                    print("SenderAgent: Response Message received: {}".format(msg.body))
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
        self.message_to_send = ""
        super().__init__(*args, **kwargs)
    
    def send_message(self, recv_jid, message_to_send):
        self.recv_jid = recv_jid
        self.has_message = True
        self.message_to_send = message_to_send


class ClasificationAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            # print("ClasificationAgent: Agent running")

            msg = await self.receive(timeout=1)
            
            if msg:
                print("ClasificationAgent: Message received with content: {}".format(msg.body))

                msg = Message(to=self.agent.recv_jid)  # Instantiate the message
                msg.set_metadata(
                    "performative", "inform"
                )  # Set the "inform" FIPA performative
                msg.body = str(f"ClasificationAgent: Message Received {datetime.datetime.now().time()}")
                await self.send(msg)

        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print("ClasificationAgent: started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
    
    def __init__(self, recv_jid, *args, **kwargs):
        self.recv_jid = recv_jid
        super().__init__(*args, **kwargs)

class ExtractionAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            # print("ExtractionAgent: Agent running")

            msg = await self.receive(timeout=1)

            if msg:
                print("ExtractionAgent: Message received with content: {}".format(msg.body))

                msg = Message(to=self.agent.recv_jid)  # Instantiate the message
                msg.set_metadata(
                    "performative", "inform"
                )  # Set the "inform" FIPA performative
                msg.body = str(f"ExtractionAgent: Message Received {datetime.datetime.now().time()}")
                await self.send(msg)

        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print("ExtractionAgent: started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
    
    def __init__(self, recv_jid, *args, **kwargs):
        self.recv_jid = recv_jid
        super().__init__(*args, **kwargs)

if __name__ == "__main__":
    sender_jid = "dasiprojectsender@01337.io"
    sender_passwd = "1q2w3e4r5t"

    recv_jid = "dasiprojectclassifier@01337.io"
    recv_passwd = "1q2w3e4r5t"

    clasificationAgent = ClasificationAgent(sender_jid, recv_jid, recv_passwd)
    future = clasificationAgent.start()
    future.result() # wait for receiver agent to be prepared.

    senderagent = SenderAgent(sender_jid, sender_passwd)
    senderagent.start()

    while clasificationAgent.is_alive():
        try:
            time.sleep(5)
            senderagent.send_message(recv_jid, "Hola")
        except KeyboardInterrupt:
            senderagent.stop()
            clasificationAgent.stop()
            break
    print("Agents finished")
    quit_spade()