""" Authors: Ane López Mena & Maite López Mena """
from spade.behaviour import OneShotBehaviour
# ========================================================================== #
#                         ** STOPPING BEHAVIOUR **                           #
# ========================================================================== #
# Define el comportamiento del Agente como "OneShotBehaviour"
class StoppingBehaviour(OneShotBehaviour):
    # Definir método constructor
    def __init__(self, a):
        # Definir atributos propios del agente:
        #  1) Instancia del agente que ejecuta el comportamiento
        self.myAgent = a

    # ------------------------------------------------------------------
    async def run(self):
        print("    Stopping tasks...")
        # Ejecutar las tareas de finalización propias de este tipo de recurso
        self.myAgent.functionality.stop()

        # Finalizar comportamiento
        self.kill()