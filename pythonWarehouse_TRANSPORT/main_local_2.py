
import asyncio
import random
import signal
import sys
import time
import netifaces
import spade
from Agents.TransportAgent import TransportAgent
from agent_gui.gui_agent import GUIAgent


async def main():

    print("+-----------------------------------------------------------+")
    print("|            MULTIAGENT SYSTEM COMMUNICATION                |")
    print("|           Mikel González ---- Mikel Sasiain               |")
    print("|             =============================                 |")
    print("|                - Trabajo Fin de Grado -                   |")
    print("|                     - 2024-2025 -                         |")
    print("+-----------------------------------------------------------+\n")

    id_num_ma = input("INTRODUCE EL NÚMERO DE IDENTIFICADOR DEL AGENTE MÁQUINA: ")
    machine_jid = "machineagent_" + id_num_ma + "@ubuntu.min.vm"
    print("EL ID DEL AGENTE MÁQUINA ES: " + machine_jid)

    transport1_jid = "transportagent_1@ubuntu.min.vm"
    transport2_jid = "transportagent_2@ubuntu.min.vm"
    passwd = "upv123"

    # Inicialización de agente transporte
    ta1 = TransportAgent(transport1_jid, passwd, machine_jid, random.uniform(0, 100))
    await ta1.start()
    while not ta1.ready:
        await asyncio.sleep(1)
    print()

    # Inicialización de agente transporte
    ta2 = TransportAgent(transport2_jid, passwd, machine_jid, random.uniform(0, 100))
    await ta2.start()
    while not ta2.ready:
        await asyncio.sleep(1)
    print()

    # Inicialización de agente GUI
    gui_jid = "gui_ta_1@ubuntu.min.vm"
    guia = GUIAgent(gui_jid, passwd, transport1_jid)
    await guia.start()
    # Add customized webpages
    guia.web.add_get("/acl_message", guia.hello_controller, "./Desktop/pythonWarehouse/agent_gui/htmls/send_acl.html")
    guia.web.add_post("/acl_message/submit", guia.acl_post_controller, "./Desktop/pythonWarehouse/agent_gui/htmls/send_acl_submit.html")
    guia.web.start(hostname="0.0.0.0", port="10002")  # https://spade-mas.readthedocs.io/en/latest/web.html#
    guia.web.add_menu_entry("Send ACL message", "/acl_message",
                            "fa fa-envelope")  # https://github.com/javipalanca/spade/blob/master/docs/web.rst#menu-entries
    ip = netifaces.ifaddresses('ens33')[netifaces.AF_INET][0]['addr']
    print("[" + gui_jid + "] Abre 'http://" + ip + ":10002/acl_message' en un navegador en Windows\n")

    # Dejar código a la espera hasta finalización de agentes
    await spade.wait_until_finished(ta1)
    await spade.wait_until_finished(ta2)
    await spade.wait_until_finished(guia)


def handler(sig_num, frame):
    print("Gestor de señales llamado con la señal " + str(sig_num))
    print("Comprueba el número de señal en "
          "https://en.wikipedia.org/wiki/Signal_%28IPC%29#Default_action")

    loop = asyncio.get_event_loop()
    loop.stop()

    print('Saliendo del programa')
    sys.exit(0)


# Programa principal 'MAIN', desde el que se iniciará el entorno
if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    print("Programa iniciado. Teclea Ctrl-C para salir.\n")

    spade.run(main())
    start = time.time()
