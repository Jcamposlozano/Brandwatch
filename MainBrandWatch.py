from Brandwatch.DescargaQuery import *
from Brandwatch.ConectorBasedeDatos import *
from datetime import datetime


class MainBrandWatch:

    def descargaBrandWatch(self):
        #************************************************
        # Se declara la hora en que inicia el proceso
        con = ConectorBasedeDatos()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        #************************************************

        d = DescargaQuery()
        d.accesos()

        #************************************************
        # Declaro la hora en que finaliza el proceso

        now2 = datetime.now()
        current_time2 = now2.strftime("%H:%M:%S")
            #envio del resumen del proceso a las bases de datos
        con.bitacoraEjecucion(horaejecucion = current_time
                                ,horafin = current_time2
                                ,num_correos = '0'
                                ,tarearealizada = 'BRANDWATCH')
        #************************************************
