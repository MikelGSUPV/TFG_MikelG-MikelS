
import random
import string

from spade.message import Message
from RAInterface import RAInterface
from Agents.GWAgentOPCUA import GWAgentOPCUA

# ========================================================================== #
#                      ** MachineFunctionality **                           #
# ========================================================================== #
# Esta clase heredará dos métodos de la interfaz 'RAInterface'
#   1) rcvDataFromAsset
#   2) sendDataToAsset
class MachineFunctionality(RAInterface):
    #   [BOOTING BEHAVIOUR]
    async def init(self, myAgent):
        # Metodo de inicialización del agente MÁQUINA
        print("[" + myAgent.id + "] [MachineFunctionality, init] booting")

        # Inicializar variables:
        #   1) Flag WIP (WorkInProgress)
        self.WIP = False
        #   2) Flag callForProposals, para iniciar la negociación
        self.callForProposals = False
        #   3) JID del ganador de la negociación
        self.winner_jid = ""

        # Guardar JID + password de GWAgentOPCUA
        gw_jid = "gwagentopcua_" + myAgent.id.split('_')[1]
        myAgent.gw_jid = gw_jid
        passwd = "upv123"

        # Instanciar el GWAgentOPCUA que enviará una solicitud al Asset Físico (PLC).
        ga = GWAgentOPCUA(gw_jid, passwd)
        await ga.start()

        print("[" + myAgent.id + "] [MachineFunctionality, init] booting finished")

# ============================================================================================================
#   [RUNNING BEHAVIOUR]
    async def execute(self, behav, myAgent):
        # Metodo de ejecución de las funcionalidades del agente máquina. Aquí, el agente se
        # quedará a la escucha de mensajes, y tras recibir una petición, la añadirá al plan de máquina
        print("[" + myAgent.id + "] [MachineFunctionality, execute] running")

        if not myAgent.ready:
            myAgent.ready = True

        # A espera de recibir mensajes
        receivedMsg = await behav.receive(timeout=60)
        if receivedMsg:
            print("\n[" + myAgent.id + "] [MachineFunctionality, execute] message from " + str(receivedMsg.sender) + ": " + receivedMsg.body)

            # Añadir petición al plan de transporte
            task = receivedMsg.body
            myAgent.machinePlan.append(task)
            print("[" + myAgent.id + "] [MachineFunctionality, execute] request added to machinePlan: " + str(myAgent.machinePlan))

        else:
            # No ha recibido mensaje en un intervalo de 1 minuto
            print("[" + myAgent.id + "] [MachineFunctionality, execute] No message received within 60 seconds")

# ============================================================================================================
#   [ASSET MANAGEMENT BEHAVIOUR]
    async def sendDataToAsset(self, behav, myAgent):
        # Evalúa el valor de un flag de “trabajo en proceso”(WIP) para determinar
        # si un recurso físico está disponible. Si es así, también comprueba las peticiones de
        # servicio pendientes relacionadas con el recurso (plan de máquina).
        # Si se dan esas condiciones, la información relativa a la siguiente petición de servicio
        # se envía al gateway (pasarela). Una vez se haya envíado la información, el flag “trabajo
        # en proceso” se activa para bloquear el envío de nueva información, hasta que el servicio actual
        # se haya completado (WIP=True).

        # Si no hay trabajo en progreso y hay tareas pendientes
        if (not self.WIP and len(myAgent.machinePlan) > 0):

            # Coge la primera tarea de la lista
            task = myAgent.machinePlan[0]
            print("[" + myAgent.id + "] [MachineFunctionality, sendDataToAsset] next task in queue: " + task)

            # Se marca como 'ocupado'
            self.WIP = True

            # Instancia un mensaje e informa a GWAgent OPCUA
            msg2send = Message(to=myAgent.gw_jid, sender=myAgent.id, body=str(task))
            msg2send.metadata = {'performative': 'REQUEST',
                                 'ontology': 'asset_service'}

            # Envía al mensaje al GWAgentOPCUA
            await behav.send(msg2send)
            print("[" + myAgent.id + "] [MachineFunctionality, sendDataToAsset] service request to " + str(msg2send.to) + ": " + msg2send.body)

    # ----------------------------------------------------------------------------------------------------
    async def rcvDataFromAsset(self, behav, myAgent):
        # Si el servicio se ha completado, su información es borrada de la cola de servicios asociados
        # y el flag “trabajo en proceso” es desactivado (WIP=False).

        # Espera al mensaje que indica que la tarea ha terminado
        receivedMsg = await behav.receive()
        if receivedMsg:
            if receivedMsg.body in ['STORED', 'EXTRACTED']:
                # Tarea finalizada
                task = myAgent.machinePlan[0]
                print("\n[" + myAgent.id + "] [MachineFunctionality, rcvDataFromAsset] task " + str(task) + " finished")

                # Quitar tarea del plan de máquina
                myAgent.machinePlan.pop(0)
                print("[" + myAgent.id + "] [MachineFunctionality, rcvDataFromAsset] request removed from MachinePlan: " + str(myAgent.machinePlan))

                if (receivedMsg.body == "STORED"):
                    self.WIP = False
                    print("[" + myAgent.id + "] [MachineFunctionality, rcvDataFromAsset] ready")

                elif (receivedMsg.body == "EXTRACTED"):
                    print("[" + myAgent.id + "] [MachineFunctionality, rcvDataFromAsset] request a transportation service")

                    # Activar señal para comienzo de negociación entre transportes
                    self.callForProposals = True

            elif receivedMsg.body == 'IN WAREHOUSE':
                print("[" + myAgent.id + "] [MachineFunctionality, rcvDataFromAsset] transport arrived")
                self.WIP = False
                print("[" + myAgent.id + "] [MachineFunctionality, rcvDataFromAsset] ready")

# ============================================================================================================
#   [NEGOTIATION BEHAVIOUR]
    async def negotiation(self, behav, myAgent):



        if (self.callForProposals):
            print("[" + myAgent.id + "] [MachineFunctionality, negotiation] start")


            CFPmsg = "contractors="+str(myAgent.targets)+"#negotiationCriteria=battery".replace('"', "")

            thread = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))


            for jid in myAgent.targets:
                print("[" + myAgent.id + "] [MachineFunctionality, negotiation, " + thread + "] CFP message to " + jid)
                msg2Send = Message(to=jid, sender=myAgent.id, body=str(CFPmsg))
                msg2Send.metadata = {'performative': 'CFP',
                                     'ontology': 'negotiation',
                                     'thread': thread}
                await behav.send(msg2Send)


            replyMsg = await behav.receive(timeout=60)
            if replyMsg:
                if 'performative' in replyMsg.metadata:
                    winner = replyMsg.sender
                    print("[" + myAgent.id + "] [MachineFunctionality, negotiation, " + thread + "] winner is " + str(winner))

                    if (winner):

                        self.winner_jid = str(winner)


                        msg2Send = Message(to=str(winner), sender=myAgent.id, body=str("COLLECTION"))
                        msg2Send.metadata = {'performative': 'REQUEST',
                                             'ontology': 'agent_service'}
                        await behav.send(msg2Send)
                        print("[" + myAgent.id + "] [MachineFunctionality, negotiation, " + thread + "] service request to " + str(winner) + ": " + msg2Send.body)


                        self.callForProposals  = False

            else:
                print("[" + myAgent.id + "] [MachineFunctionality, negotiation] No message received within 60 seconds")

# ============================================================================================================
#   [STOPPING BEHAVIOUR]
    def stop(self):
        print("Machine status: STOP")

# ============================================================================================================
#   [IDLE BEHAVIOUR]
    def idle(self):
        print("Machine status: IDLE")