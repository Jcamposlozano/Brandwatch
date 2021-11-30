from bwapi.bwproject import BWProject, BWUser
from bwapi.bwresources import BWQueries, BWGroups, BWAuthorLists, BWSiteLists, BWLocationLists, BWTags, BWCategories, BWRules, BWMentions, BWSignals
import datetime
import logging
import pandas as pd

#*********************************************
from Brandwatch.ConectorBasedeDatos import *
from Brandwatch.Usuario import * 
from Brandwatch.Encriptacion import *


class DescargaQuery:

    def __init__(self):
        self.__project= None
        self.__usuarioActual = None
        self.enc = Encriptacion()
        self.con = ConectorBasedeDatos()

    lista = [["AB InBev - COPEC","ADHOC: Corona Virus Colombia - NO BORRAR"],
            ["AB InBev - MA","1 COVID-19_MÉXICO_NO BORRAR"]]        

    def accesos(self):
        intentos = 0
        for i in self.lista:
            while True:
                if intentos == 10:
                    break
                self.recorrerUsuarios()
                conSdk= self.conectionSDK(i[0],self.__usuarioActual)
                print('**************************************')
                print(self.__usuarioActual)
                print('**************************************')
                print(conSdk)
                if conSdk == True:
                    print(self.descargaDataCovid(i[1]))
                    self.con.ejecutarConsultaDesarrollo(self.__usuarioActual.cambiarEstado())
                    break
                else:
                    print("entro en el error")
                    self.con.ejecutarConsultaDesarrollo(self.__usuarioActual.cambiarEstado())
                    self.recorrerUsuarios()
                    intentos += 1
            self.con.ejecutarConsultaDesarrollo(self.__usuarioActual.cambiarEstado())      

    def recorrerUsuarios(self):
        self.validaUsuarios()
        for usuario in self.usuarios:
            self.__usuarioActual = usuario
            self.escribeTokens(self.__usuarioActual.getToken())
            break            

    def validaUsuarios(self):
        self.usuarios = self.con.obtenerUsuarios()
        print(len(self.usuarios))
        if len(self.usuarios) == 0:
            self.con.activaUsuarios()
            self.usuarios = self.con.obtenerUsuarios()


    def escribeTokens(self, token):
        f = open('tokens.txt', 'w')
        f.write('token:	' + token) 
        f.close()

    def conectionSDK(self,projectConsulta,usuario: Usuario):
        try:
            logger = logging.getLogger("bwapi")
            BWUser(username= self.enc.decryptMessage(usuario.getUser()) 
                    , password=self.enc.decryptMessage(usuario.getPassword())
                    , token_path="tokens.txt")
            self.__project = BWProject(username= self.enc.decryptMessage(usuario.getUser()) 
                    , project=projectConsulta
                    , token_path="tokens.txt")
            return True
        except (Exception) as error:
            return False

    def calculaFechas(self):
        ahora = datetime.datetime.now()
        if len(str(ahora.hour)) == 1:
            horaFin = "T0" + str(ahora.hour) + ":00:00"
        else:
            horaFin = "T" + str(ahora.hour) + ":00:00"
        today = (datetime.date.today()).isoformat() + horaFin        

        if len(str(ahora.hour-1)) == 1:
            horaInicio = "T0" + str(ahora.hour-1) + ":00:00"
            if horaInicio == 'T0-1:00:00':
                start = (datetime.date.today() + datetime.timedelta(days=-1)).isoformat() +  'T23:00:00'
            else:
                start = (datetime.date.today()).isoformat() + horaInicio
        else:
            horaInicio = "T" + str(ahora.hour-1) + ":00:00"
            start = (datetime.date.today()).isoformat() +  horaInicio

        return today,start

    def descargaDataCovid(self,query):
        try:
            queries = BWQueries(self.__project)        
            today,start = self.calculaFechas()
            print('today = ' +str(today)+ ' start = ' + str(start))         
            sql = 'insert into sl.pb_ProcessP1 (sub,category,sentiment,total,fecha,hora,queryid) values '
            sql2 = 'insert into sl.pb_ProcessP2 (sentiment,total,fecha,hora,queryid) values '
            filtered = queries.get_mentions(name = query,
                                            startDate = start, 
                                            endDate = today)
            df = pd.DataFrame(filtered)
            #datacompleta = df[["author","categories","categoryDetails","city","country","domain","gender",
            #                  "impressions","interest","queryId","queryName","reachEstimate","sentiment","url","impact"]]

            #datacompleta.to_csv('column_data.csv', index=False)
            #self.con.ejecutarConsulta(str("copy sl.pb_processp3 (author,categories,categoryDetails,city ,country ,domain ,gender "
	        #",impressions ,interest,queryId,queryName,reachEstimate,sentiment,url,impact) "
            #"from '/home/ProcessAll/Boty/Brandwatch/column_data.csv' delimiter ',' csv header;"))


            column_name = ["sub","category","id","parentId","sentiment"]
            resultado = []
            contador = 0
            resultadosSentimientos = []

            for sentiment in df["sentiment"].unique(): 
                nameCategoria = []
                contador = 0
                for datos in df["categoryDetails"][df["sentiment"]== sentiment]:
                    contador += 1
                    if len(datos) >0:
                        for j in datos:
                            linea = []
                            linea.append(j["name"])
                            linea.append(j["parentName"])
                            linea.append(j["id"])
                            linea.append(j["parentId"])
                            linea.append(sentiment)
                            nameCategoria.append(linea)
                
                linea2 = []            
                linea2.append(sentiment)
                linea2.append(contador)
                resultadosSentimientos.append(linea2)
            
                categorias = pd.DataFrame(nameCategoria, columns = column_name)
                resultadoP = categorias.groupby([categorias["sub"]
                                ,categorias["category"]
                                ,categorias["sentiment"]], as_index=True).agg(
                                                                {
                                                                    'sub':'first',
                                                                    'category': 'first',
                                                                    'sentiment': 'first',
                                                                    'id':"count"    # Sum duration per group
                                                                })

                                #.count().to_csv('week_grouped.csv')
                resultadoP.columns = ["sub","category","sentiment","total"]
                print("**********************")
                #print(resultadoP)
                for k in resultadoP.values.tolist():
                    sql += str("('{}','{}','{}',{},'{}','{}','{}'),").format(
                    k[0].replace("'",""),k[1],k[2],k[3]
                    ,(datetime.date.today()).isoformat(),datetime.datetime.now(),
                    df["queryId"].unique().tolist()[0])
            self.con.ejecutarConsulta(sql[:-1])

            for s in resultadosSentimientos:
                sql2 += str("('{}',{},'{}','{}','{}'),").format(
                s[0],s[1],(datetime.date.today()).isoformat(),datetime.datetime.now(),df["queryId"].unique().tolist()[0])
            self.con.ejecutarConsulta(sql2[:-1])
            self.con.ejecutarConsulta('select sl.agregadatosCovid();')
            return True
        except (Exception) as error:
            print(error)
            return False    
