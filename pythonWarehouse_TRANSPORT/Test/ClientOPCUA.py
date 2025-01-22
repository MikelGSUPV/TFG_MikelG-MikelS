import time

import opcua
from opcua import ua
from opcua import Client

client = Client("opc.tcp://192.168.0.101:4840") # Initiate
# Connect to Server
client.connect()

node_AuxInit = client.get_node("ns=4;i=9")
node_Marcha = client.get_node("ns=4;i=7")
node_Posicion = client.get_node("ns=4;i=66")

# ------- Simular arranque de máquina
node_AuxInit.set_attribute(ua.AttributeIds.Value, ua.DataValue(True))
time.sleep(1)
node_AuxInit.set_attribute(ua.AttributeIds.Value, ua.DataValue(False))

# Simular pulso de "Marcha"
node_Marcha.set_attribute(ua.AttributeIds.Value, ua.DataValue(True))
time.sleep(1)
node_Marcha.set_attribute(ua.AttributeIds.Value, ua.DataValue(False))

node_Posicion.set_attribute(ua.AttributeIds.Value, ua.DataValue(ua.Variant(22, ua.VariantType.Int16)))

def serviceFinished(node_ServiceFinished):
    return node_ServiceFinished.get_value()


def servicePosible(node_AlmacenOcupacion, service, target):
    print("AlmacénOcupacion: " + str(node_AlmacenOcupacion.get_value()))
    warehouseOcupation = node_AlmacenOcupacion.get_value()

    # Si se quiere INTRODUCIR Y la posición está ocupada
    if (service == 1 and warehouseOcupation[target-1] == True):
        return False
    if (service == 2 and warehouseOcupation[target-1] == False):
        return False
    return True


while True:
    maxServices = 2
    # Pedir el número de servicio a realizar

    nServ = int(input("                 |----> Choose SERVICE TYPE:  ** DELIVERY (1) / COLLECTION (2) **"))
    print("                 |           + SERVICE TYPE: " + str(nServ))

    while not 0 < nServ < (maxServices + 1):
        print("                  ** ERROR **: Service type is not valid [1-" + str(maxServices) + "]")
        nServ = int(input("                 |----> Choose SERVICE TYPE:\n  * DELIVERY (1)\n  * COLLECTION (2)"))
        print("                 |           + SERVICE TYPE: " + str(nServ))

    # Pedir el número de ítems a procesar
    targetPos = int(input("                 |----> Choose TARGET POSITION (1-54):"))
    print("                 |           + SHELF No.: " + str(targetPos))
    print("                 +---------------------------------------------------+\n")

    while not 0 < targetPos < 55:
        print("                  ** ERROR **: TARGET POSITION is not valid [1-54]")
        targetPos = int(input("                 |----> Choose TARGET POSITION (1-54):"))
        print("                 |           + SHELF No.: " + str(targetPos))
        print("                 +---------------------------------------------------+\n")

    #=====================================================================================


    try :

        target = targetPos
        serviceType = nServ

        # Instanciar nodos

        node_Reset = client.get_node("ns=4;i=8")
        node_CogerDejar = client.get_node("ns=4;i=10")
        node_Posicion = client.get_node("ns=4;i=66")
        node_ServiceFinished = client.get_node("ns=4;i=5")
        node_AlmacenOcupacion = client.get_node("ns=4;i=11")


        # ------- Prod. Normal
        # Definir tipo de servicio
        #     * INTRODUCIR ( CogerDejar = 1 )
        if (serviceType == 1):
            node_CogerDejar.set_value(True)
        else:
        #   * EXTRAER ( CogerDejar = 0 )
            node_CogerDejar.set_value(False)

        # Cambiar posición
        node_Posicion.set_value(target, varianttype=opcua.ua.VariantType.Int16)

        # Comproba si la acción es realizable
        ok = servicePosible(node_AlmacenOcupacion, serviceType, target)

        print("¿SE PUEDE HACER?: " + str(ok) )

        if (ok):
            # Simular pulso de Reset
            node_Reset.set_value(True)
            time.sleep(1)
            node_Reset.set_value(False)

            finished = False

            while not finished:
                finished = serviceFinished(node_ServiceFinished)
            print("SERVICE FINISHED!")
            #return True
        else:
            # Simular pulso de Reset
            node_Reset.set_value(True)
            time.sleep(1)
            node_Reset.set_value(False)
            #return False

    finally :
        pass
        #print("ERROR, Could not execute service")
        # Disconnect when finish
        #client.disconnect()
    #return False
