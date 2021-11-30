import psycopg2
import getpass

from Brandwatch.Usuario import *

class ConectorBasedeDatos:

    conn = ''
    cur = ''
    schema = ''
    sqlTotal = ''
    con = ''
    cur = ''
    database = ''
    user = ''
    password = ''
    host = ''
    port = ''
    usuarios = []

    def __init__(self):
        self.schema = 'earned_media.'
        self.database = ''
        self.user = ''
        self.password = ''
        self.host = ''
        self.port = ''

    def ejecutarConsulta(self, sql):
        try:
            self.con = psycopg2.connect(database= self.database, user=self.user , password=self.password, host=self.host, port=self.port)
            self.cur = self.con.cursor()
            self.cur.execute(sql)
            #print(sql)
            self.con.commit()
            self.con.close()
        except (Exception, psycopg2.DatabaseError) as error:  
            controlarErr = str(error)         
            if controlarErr.find('(0x0000274C/10060)')>1 :
                print('Reintento de acceder')
                self.ejecutarConsulta(sql)
            else:   
                print(error) 
                print('*************************************')
                print(sql)
                print('*************************************')
       
    def crearUsuario(self, **kwargs):
        sql = str("INSERT INTO admon.user_brandwatch(usuario,password,token)"
        "values ('{}','{}','{}');"
        ).format (kwargs['user']
        ,kwargs['passwrod']
        ,kwargs['token'])
        self.ejecutarConsultaDesarrollo(sql)

    def actualizarUsuario(self, **kwargs):
        sql = str("update admon.user_brandwatch "
        "set password = '{}', token = '{}'"
        "where usuario = '{}';"
        ).format (kwargs['passwrod']
        ,kwargs['token']
        ,kwargs['user'])
        self.ejecutarConsultaDesarrollo(sql)     

    def eliminarUsuario(self, **kwargs):
        sql = str("delete from admon.user_brandwatch where usuario = '{}';"
        ).format (kwargs['user'])
        self.ejecutarConsultaDesarrollo(sql)     
    
    def ejecutarConsultaDesarrollo(self, sql):
        try:
            self.con = psycopg2.connect(database= "db_marketingWeb", user=self.user , password=self.password, host=self.host, port='5433')
            self.cur = self.con.cursor()
            self.cur.execute(sql)
            #print(sql)
            self.con.commit()
            self.con.close()
        except (Exception, psycopg2.DatabaseError) as error:  
            controlarErr = str(error)         
            if controlarErr.find('(0x0000274C/10060)')>1 :
                print('Reintento de acceder')
                self.ejecutarConsulta(sql)
            else:   
                print(error) 
                print('*************************************')
                print(sql)
                print('*************************************')

    def obtenerUsuarios(self):
        self.usuarios = []
        c = psycopg2.connect(database= "db_marketingWeb", user=self.user , password=self.password, host=self.host, port='5433')
        try:
            with c.cursor() as cursor:
                sql = str("select usuario, password, token,usada "
                        "from admon.user_brandwatch where usada = false order by key_id")
                cursor.execute(sql)
                for (usuario, password, token,usada) in cursor:
                    user = Usuario()
                    user.setUser(usuario)
                    user.setPassword(password)
                    user.setToken(token)
                    user.setUsado(usada) 
                    self.usuarios.append(user)
                cursor.close()
                c.close()
            return self.usuarios
        finally:
            pass     

    def activaUsuarios(self):
        sql = str("update admon.user_brandwatch set usada = 'false'")
        self.ejecutarConsultaDesarrollo(sql)

    def bitacoraEjecucion(self,horaejecucion, horafin, num_correos, tarearealizada):
        try:
            self.con = psycopg2.connect(database= 'db_brand_buzz', user='app_knime' , password='knime2020#', host='10.170.3.3', port='5432')
            self.cur = self.con.cursor()
            sql = str("insert into br_tramiq.bitacoraejecucion (usuario,horaejecucion, horafin, num_correos, tarearealizada)" +
              "values ('" + getpass.getuser() + "','" + horaejecucion + "','" + horafin + "','" + num_correos + "','" + tarearealizada + "');")
            self.cur.execute(sql)
            #print(sql)
            self.con.commit()
            self.con.close()
        except (Exception, psycopg2.DatabaseError) as error:  
            controlarErr = str(error)         
            if controlarErr.find('(0x0000274C/10060)')>1 :
                print('Reintento de acceder')
                self.ejecutarConsulta(sql)
            else:   
                print(error) 
                print('*************************************')
                print(sql)
                print('*************************************')

