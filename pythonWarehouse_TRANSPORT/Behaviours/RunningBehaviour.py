""" Authors: Ane López Mena & Maite López Mena """
import asyncio

from spade.behaviour import CyclicBehaviour

# ========================================================================== #
#                           ** RUNNING BEHAVIOUR **                          #
# ========================================================================== #
# Running es el comportamiento para la gestión de servicios.
# Es decir, cuando llega un mensaje ACL con una solicitud de servicio, este comportamiento
# es el encargado de ordenar, supervisar y reportar la ejecución del servicio solicitado.

# Define el comportamiento del Agente como "CyclicBehaviour"
class RunningBehaviour(CyclicBehaviour):

    def __init__(self, a):
        # Heredamos el init de la clase super
        super().__init__()

        # Definir atributos propios del agente:
        #  1) Instancia del agente que ejecuta el comportamiento
        self.myAgent = a

    async def run(self):
        print("\n[" + self.agent.id + "] [RunningBehaviour, run]")
        await self.myAgent.functionality.execute(self, self.myAgent)

    async def on_end(self):
        print("\n[" + self.agent.id + "] [RunningBehaviour, on_end] rb kaput")



