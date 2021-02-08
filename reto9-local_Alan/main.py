#Importamos Menu
from helpers.menu import Menu
from controllers.almacen import AlmacenController
from controllers.admin import AdminController
from controllers.facturas import FacturaController
from controllers.usuario import UsuarioLogin


#Creamos el Menu de la APP
def app():
    try:
        while True:      
            print('''
            +++++++++++++++++++++++++++++++
                Sistema de Minimarket
                   Ingrese Usuario
            +++++++++++++++++++++++++++++++
            ''')
            menu_principal=['Ingreso','Salir']
            respuesta=Menu(menu_principal).show()
            
            if respuesta==1:
                users=UsuarioLogin()
                user=users.login()
                if user==1:
                    admin=AdminController()
                    admin.menu()
                    if admin.salir:
                        app()
                elif user==2:
                    fact=FacturaController()
                    fact.menu()
                    if fact.salir:
                        app()
                elif user==3:
                    alma=AlmacenController()
                    alma.menu()
                    if alma.salir:
                        app()
            else:
                break  

        print('\n Gracias por utilizar nuestro sistema \n')
    except KeyboardInterrupt:
        print('\n Se interrumpio la aplicacion')
    except Exception as e:
        print(f'{str(e)}')

app()