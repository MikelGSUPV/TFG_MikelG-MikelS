""" Authors: Ane López Mena & Maite López Mena """
import asyncio

from spade.behaviour import CyclicBehaviour

# ========================================================================== #
#                         ** NEGOTIATION BEHAVIOUR **                        #
# ========================================================================== #
# Define el comportamiento del Agente como "CyclicBehaviour"
class NegotiationBehaviour(CyclicBehaviour):

    def __init__(self, a, thread, targets, criteria):
        # Heredamos el init de la clase super
        super().__init__()

        # Definir atributos propios del agente:
        #  1) Instancia del agente que ejecuta el comportamiento
        self.myAgent = a

        self.thread = thread
        self.targets = targets
        self.criteria = criteria

        self.step = 0
        self.replyNum = 0

    async def run(self):
        print("\n[" + self.agent.id + "] [NegotiationBehaviour, run]")
        await self.myAgent.functionality.negotiation(self, self.myAgent)

    async def on_end(self):
        print("\n[" + self.agent.id + "] [NegotiationBehaviour, on_end] nb kaput")