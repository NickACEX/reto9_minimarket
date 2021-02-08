#importamos metodos de  Modelo Libros
from models.productos import Productos
from models.facturas import Facturas
from models.usuarios import Usuarios
from helpers.menu import Menu
from helpers.helper import input_data, print_table, question

#Nuestros metodos
class AdminController:
    def __init__(self):
        self.productos=Productos()
        self.facturas=Facturas()
        self.usuarios=Usuarios()
        self.salir=False
    
    def menu(self):
        try:
            while True:
                print('''
                =============================
                    Consola Administracion
                =============================
                ''')
                lista_menu=['Reporte Almacen','Reporte Ventas','Reporte Usuarios','Crear Usuario','Editar Usuario','Eliminar Usuario','Salir']
                respuesta=Menu(lista_menu).show()

                if respuesta==1:
                    self.reporte_productos()
                elif respuesta==2:
                    self.reporte_ventas()
                elif respuesta==3:
                    self.all_usuarios()
                elif respuesta==4:
                    self.crea_usuario()
                elif respuesta==5:
                    self.search_usuario_update()
                elif respuesta==6:
                    self.search_usuario_delete()
                else:
                    self.salir=True
                    break  

        except Exception as e:
            print(f'{str(e)}')

    def reporte_productos(self):
        print('''
        =============================
              Reporte Productos
        =============================
        ''')
        producto=self.productos.get_productos('producto_id')
        print(print_table(producto,['Producto_ID','Nombre','Stock','Precio Unit']))
        input('\nPresiona una tecla para continuar . . .')


    def reporte_ventas(self):
        print('''
        =============================
               Reporte Ventas
        =============================
        ''')
        factura=self.facturas.get_facturas('factura_id')
        print(print_table(factura,['Factura_ID','Producto_ID','Fecha_Registro','Cantidad','Costo']))
        input('\nPresiona una tecla para continuar . . .')

    def all_usuarios(self):
        print('''
        =============================
               Reporte Usuario
        =============================
        ''')
        usuario=self.usuarios.get_usuarios('usuario_id')
        print(print_table(usuario,['Usuario_ID','Usuario','Contraseña','Perfil_ID']))
        input('\nPresiona una tecla para continuar . . .')


    def crea_usuario(self):
        usuario=input_data('Ingrese el usuario del sistema : ')
        contraseña=input_data('Ingrese la contraseña del usuario : ')
        perfil_id=input_data('Ingrese el perfil del usuario, Tener en cuenta "1(admin),2(cajero),3(almacenero)":')
        self.usuarios.insert_usuario({
            'usuario':usuario,
            'contraseña':contraseña,
            'perfil_id':perfil_id
        })
        print('''
        ***Usuario Agregado***
        ''')    
        self.all_usuarios()

    def search_usuario_update(self):
        self.all_usuarios()
        print('''
        =============================
               Buscar Producto
        =============================
        ''')
        try:
            usuario_id=input_data('Ingrese el ID del Usuario : ','int')
            usuario=self.usuarios.get_usuario({
                'usuario_id': usuario_id
            })
            #print(print_table(usuario,['Usuario_ID','Usuario','Contraseña','Perfil_ID']))
            self.update_usuario(usuario_id)

        except Exception as e:
            print(f'{str(e)}')
        input('\nPresiona una tecla para continuar . . .')

    def update_usuario(self, usuario_id):
        usuario=input_data('Ingrese el usuario del sistema : ')
        contraseña=input_data('Ingrese la contraseña del usuario : ')
        perfil_id=input_data('Ingrese el perfil del usuario, Tener en cuenta "1(admin),2(cajero),3(almacenero)":')
        self.usuarios.update_usuario({
            'usuario_id':usuario_id
        },{
            'usuario':usuario,
            'contraseña':contraseña,
            'perfil_id':perfil_id
        })
        print('\n Datos del Usuario Actualizado \n')
    
    def search_usuario_delete(self):
        self.all_usuarios()
        print('''
        =============================
               Buscar Producto
        =============================
        ''')
        try:
            usuario_id=input_data('Ingrese el ID del Usuario : ','int')
            usuario=self.usuarios.get_usuario({
                'usuario_id': usuario_id
            })
            print(usuario_id)
            #print(print_table(usuario,['Usuario_ID','Usuario','Contraseña','Perfil_ID']))
            self.delete_usuario(usuario_id)

        except Exception as e:
            print(f'{str(e)}')
        input('\nPresiona una tecla para continuar . . .')

    def delete_usuario(self, usuario_id):
        self.usuarios.delete_usuario({
            'usuario_id': usuario_id
        })
        print('\n Datos del Usuario Actualizado \n')

