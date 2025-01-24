
import asyncio
import signal
import sys
import time

import spade
from Agents.MachineAgent import MachineAgent
from agent_gui.gui_agent import GUIAgent


async def main():

    print("+-----------------------------------------------------------+")
    print("|            MULTIAGENT SYSTEM COMMUNICATION                |")
    print("|           Mikel González ---- Mikel Sasiain               |")
    print("|             =============================                 |")
    print("|                - Trabajo Fin de Grado -                   |")
    print("|                     - 2024-2025 -                         |")
    print("+-----------------------------------------------------------+\n")

    passwd = "upv123"

    targets = []
    num_ta = input("INTRODUCE EL NÚMERO DE AGENTES TRANSPORTE (RANGO 2-n): ")
    for i in range(1, int(num_ta)+1):
        targets.append('transportagent_' + str(i) + '@ubuntu.min.vm')

    # Inicialización de agente máquina
    id_num_ma = input("INTRODUCE EL NÚMERO DE IDENTIFICADOR DEL AGENTE MÁQUINA: ")
    machine_jid = "machineagent_" + id_num_ma + "@ubuntu.min.vm"
    print("EL ID DEL AGENTE MÁQUINA ES: " + machine_jid)
    ma = MachineAgent(machine_jid, passwd, targets)
    await ma.start()
    while not ma.ready:
        await asyncio.sleep(1)
    print()

    # Inicialización de agente GUI
    gui_jid = "gui_ma_" + id_num_ma + "@ubuntu.min.vm"
    guia = GUIAgent(gui_jid, passwd, machine_jid)
    await guia.start()
    # Add customized webpages
    guia.web.add_get("/acl_message", guia.hello_controller, "./agent_gui/htmls/send_acl.html")
    guia.web.add_post("/acl_message/submit", guia.acl_post_controller, "./agent_gui/htmls/send_acl_submit.html")
    guia.web.start(hostname="0.0.0.0", port="10002")  # https://spade-mas.readthedocs.io/en/latest/web.html#
    guia.web.add_menu_entry("Send ACL message", "/acl_message",
                            "fa fa-envelope")  # https://github.com/javipalanca/spade/blob/master/docs/web.rst#menu-entries
    print("[" + gui_jid + "] Abre 'http://localhost:10002/acl_message' en el navegador")

    # Dejar código a la espera hasta finalización de agentes
    await spade.wait_until_finished(ma)
    await spade.wait_until_finished(guia)


def handler(sig_num, frame):
    print("Gestor de señales llamado con la señal " + str(sig_num))
    print("Comprueba el número de señal en https://en.wikipedia.org/wiki/Signal_%28IPC%29#Default_action")

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
