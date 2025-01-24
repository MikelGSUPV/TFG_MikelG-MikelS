import calendar
import json
import os
import time
from urllib.parse import parse_qs

import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class GUIAgent(Agent):

    def __init__(self, jid, password, local_resource_agent_jid):
        print("[" + jid + "] [GUIAgent] entering init")
        super().__init__(jid, password)
        self.local_resource_agent_jid = local_resource_agent_jid


    class SendBehaviour(OneShotBehaviour):

        async def setup(self):
            self.acl_sent = False  # se inicializa en False

        async def run(self):
            data_json = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(self.msg_data).items()}
            print("[" + str(self.agent.jid) + "] [GUIAgent, SendBehaviour] " + str(data_json))
            service = data_json['service']
            position = data_json['position']

            msg = Message()
            msg.metadata = {'performative': 'REQUEST',
                            'ontology': 'agent_service'}

            if service == '1':
                msg.to = "transportagent_" + data_json['ta_id'] + "@ubuntu.min.vm"
                msg.body = "DELIVERY:" + position
            elif service == '2':
                msg.to = str(self.agent.local_resource_agent_jid)
                msg.body = "COLLECTION:" + position

            await self.send(msg)
            print("[" + str(self.agent.jid) + "] [GUIAgent, SendBehaviour] service request to " + str(msg.to) + ": " + msg.body)


    async def hello_controller(self, request):
        return {"status": "OK"}

    async def acl_post_controller(self, request):
        self.acl_sent = False  # se inicializa en False

        data_bytes = b''
        async for line in request.content:
            data_bytes = data_bytes + line
        data_str = data_bytes.decode('utf-8')
        print("[" + str(self.jid) + "] [GUIAgent, acl_post_controller] HTTP message from HTML form: " + data_str)

        self.b = self.SendBehaviour()
        self.b.msg_data = data_str
        self.add_behaviour(self.b)
        print("[" + str(self.jid) + "] [GUIAgent, acl_post_controller] adding SendBehaviour")
        await self.b.join()
        self.acl_sent = True

        return {"status": "OK"}
