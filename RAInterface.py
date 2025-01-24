""" Authors: Ane López Mena & Maite López Mena """
# ========================================================================== #
#                          ** RAINTERFACE **                           #
# ========================================================================== #
# Estos métodos funcionan a modo de "esqueletos", puesto que la implementación de
# los mismos se sobreescribirá en las clases 'MachineFunctionality' y
# 'TransportFunctionality'.

class RAInterface():
    # 1) rcvDataFromAsset -----------------------
    def rcvDataFromAsset(self):
        print("rcvDataFromAsset generic method")

    # 2) rcvDataFromAsset -----------------------
    def sendDataToAsset(self):
        print("sendDataToAsset generic method")
