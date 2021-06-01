import datetime

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template


class ClassificationAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            # print("ClassificationAgent: Agent running")

            msg = await self.receive(timeout=1)
            
            if msg:
                print("ClassificationAgent: Message received with content: {}".format(msg.body))

                msg = Message(to=self.agent.recv_jid)  # Instantiate the message
                msg.set_metadata(
                    "performative", "inform"
                )  # Set the "inform" FIPA performative
                msg.body = str(f"ClassificationAgent: Message Received {datetime.datetime.now().time()}")
                await self.send(msg)

        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print("ClassificationAgent: started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
    
    def __init__(self, recv_jid, *args, **kwargs):
        self.recv_jid = recv_jid
        super().__init__(*args, **kwargs)
