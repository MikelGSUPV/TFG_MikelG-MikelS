""" Authors: Ane López Mena & Maite López Mena """
from spade.behaviour import CyclicBehaviour

# ========================================================================== #
#                         ** NEGOTIATION BEHAVIOUR **                        #
# ========================================================================== #
# Define el comportamiento del Agente como "CyclicBehaviour"
class NegotiationBehaviour(CyclicBehaviour):
    def __init__(self, a):
        # Heredamos el init de la clase super
        super().__init__()

        # Definir atributos propios del agente:
        #  1) Instancia del agente que ejecuta el comportamiento
        self.myAgent = a

    # ------------------------------------------------------------------
    async def run(self):
        await self.myAgent.functionality.negotiation(self, self.myAgent)