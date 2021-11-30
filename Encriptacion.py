import onetimepad
import getpass
from Brandwatch.ConectorBasedeDatos import *

class Encriptacion():

    def __init__(self):
        self.__con = ConectorBasedeDatos()
        self.__opcion = None
        self.__usuario = None
        self.__password = None
        self.__token = None

    def menu(self):
        # *****************************************
        # este es un menu de usuario para poder realizar las diferentes tareas de guardado de usuarios
        # *****************************************

        while True:
            print("************************************")
            print("1. CREATE USER")
            print("2. UPLOAD USER")
            print("3. DELETE USER")
            print("4. EXIT")
            print("************************************")
            self.__opcion = int(input("SELECT A OPTION: "))
            self.reiniciarVariables()
            if self.__opcion == 1:
                self.crearusuario()
            elif self.__opcion == 2:
                self.actualizaUsuario()
            elif self.__opcion == 3:
                self.eliminaUsuario()
            elif self.__opcion == 4:
                break    
            else:
                print('NOT A VALID SELECTION') 

            print("************************************")
            if input("WANT TO MAKE MORE REQUESTS?""WANT TO MAKE MORE REQUESTS?/y: ").upper() != 'Y':
                break

    def crearusuario(self):
        print("************************************")
        print("CREATE USER")
        print("************************************")
        while True:
            self.__usuario = self.encryptMessage(input("User: "))
            if self.__usuario == '':
                print('NOT A VALID USER')
            else:
                break
        while True:
            self.__password = self.encryptMessage(getpass.getpass("Password: ")) 
            if self.__password == '':
                print('NOT A VALID PASSWORD')
            else:
                break
        while True:    
            self.__token = input("Token: ")
            if self.__token == '':
                print('-- NOT A VALID TOKEN')
            else:
                break
        self.__con.crearUsuario(user = self.__usuario,
            passwrod = self.__password, token = self.__token)

    def actualizaUsuario(self):
        print("************************************")
        print("UPDATE USER")
        print("************************************")
        while True:
            self.__usuario = self.encryptMessage(input("User: "))
            if self.__usuario == '':
                print('NOT A VALID USER')
            else:
                break
        while True:
            self.__password = self.encryptMessage(getpass.getpass("Password: ")) 
            if self.__password == '':
                print('-- NOT A VALID PASSWORD')
            else:
                break
        while True:    
            self.__token = input("Token: ")
            if self.__token == '':
                print('-- NOT A VALID TOKEN')
            else:
                break
        self.__con.actualizarUsuario(user = self.__usuario,
            passwrod = self.__password, token = self.__token)   
        
    def eliminaUsuario(self):
        print("************************************")
        print("DELETE USER")
        print("************************************")
        while True:
            self.__usuario = self.encryptMessage(input("User: "))
            if self.__password == '':
                print('NOT A VALID USER')
            else:
                break 
        self.__con.eliminarUsuario(user = self.__usuario)

    def encryptMessage(self, texto):
        #Encripta el texto que se quiera enviar
        ct = onetimepad.encrypt(texto, 'random')
        return ct 

    def decryptMessage(self, texto):
        #Desencripta el texto que se envie
        pt1 = onetimepad.decrypt(texto, 'random')
        return pt1

    def reiniciarVariables(self):
        self.__usuario = None
        self.__password = None
        self.__token = None
