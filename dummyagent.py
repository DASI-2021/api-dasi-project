

import time
import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

class DummyAgent(Agent):
    class MyBehav(CyclicBehaviour):
        async def on_start(self):
            print("Starting behaviour . . .")
            self.counter = 0

        async def run(self):
            print("Counter: {}".format(self.counter))
            self.counter += 1
            await asyncio.sleep(1)

    async def setup(self):
        print("Agent starting . . .")
        b = self.MyBehav()
        self.add_behaviour(b)

if __name__ == "__main__":
    dummy = DummyAgent("velasquezerik@01337.io", "u0P765*Yd!")
    dummy.start()
    dummy.web.start(hostname="localhost", port="8000")

    print("Wait until user interrupts with ctrl+C")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    dummy.stop()
