#importamos metodos de  Modelo Libros
from models.usuarios import Usuarios
from helpers.menu import Menu
from helpers.helper import input_data, print_table, question
from getpass import getpass


#Nuestros metodos
class UsuarioLogin:
    def __init__(self):
        self.usuarios=Usuarios()
        self.salir=False


    def login(self):
        try:
            usuario=input_data('Ingrese el Usuario del Sistema : ')
            contra=getpass('Ingrese la Contraseña del Sistema : ')   
            valida=self.usuarios.get_by_login({
                'usuario': usuario
            },{
                'contraseña': contra
            })
            if valida:
                return valida[0]
            else:
                print('Porfavor intenta de nuevo')
        except Exception as e:
            print(f'{str(e)}')
        input('\nPresiona una tecla para continuar . . .')


