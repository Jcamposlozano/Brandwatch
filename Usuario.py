
class Usuario:

    #Esta es una clase personalizada, para poder utilizar los usuarios del BrandWatch
    # es una forma de poder consumir la información de un usuario de forma mas estructurada
    # ya que hace las veces de un tipo de variable. 

    def __init__(self):
        self.__user = None
        self.__password = None
        self.__token = None
        self.__usado = None

    #*******************************************************************
    # Se utiliza estos metodos para poder visualizar la informacion 
    # de la clase. Esto se realiza porque estas no deben ser utilizadas
    # sin metodos de acceso.

    def getUser(self):
        return self.__user
    def getPassword(self):
        return self.__password
    def getToken(self):
        return self.__token
    def getUsado(self):
        return self.__usado

    #*******************************************************************
    # Los metodos Set a diferencia de los metodos get, son para poder modificar la información
    # estos no retornan ninguna información.
    def setUser(self, user):
        self.__user = user
    def setPassword(self, password):
        self.__password = password
    def setToken(self, token):
        self.__token = token
    def setUsado(self, usado):
        self.__usado = usado      
    #*******************************************************************  

    #*******************************************************************  
    # El subString es un metodo que se encarga de visualizar la información de manera 
    # estructurada, en el momento en el que se quiera visualizar a los individuos.
    def __str__(self):
        return str("Usuario: {} \npassword: {}\ntoken: {}\nUsado: {}\n").format(self.getUser(),
        self.getPassword(),
        self.getToken(),
        self.getUsado())
    #*******************************************************************  


    def cambiarEstado(self):
        #Este metodo es utilizado en el momento en el que sea utilizado un usuario
        # o que este presente problemas. Este cambiara el estado permitiendole al sistema
        # poder continuar con el siguiente usuario y realizar las descargas necesarias.
        if str(self.getUsado()).upper() == 'TRUE':
            estadoCambiar = 'False'
        else: 
            estadoCambiar = 'True'
        return str("UPDATE admon.user_brandwatch "
                    "SET usada = '{}' "
                    "WHERE USUARIO = '{}'").format(
                    estadoCambiar,self.getUser())
