""" Authors: Ane López Mena & Maite López Mena """
from spade.behaviour import CyclicBehaviour


# ========================================================================== #
#                               ** IDLE BEHAVIOUR **                         #
# ========================================================================== #
# Define el comportamiento del Agente como "CyclicBehaviour"
class IdleBehaviour(CyclicBehaviour):
    # Definir método constructor
    def __init__(self, a):
        # Definir atributos propios del agente:
        #  1) Instancia del agente que ejecuta el comportamiento
        self.myAgent = a

    # ------------------------------------------------------------------
    async def run(self):
        print("    Idle state tasks...")

        # Definir las funcionalidades propias del recurso para estado IDLE
        self.myAgent.functionality.idle()

        # Finalizar comportamiento BootingBehav
        self.kill()