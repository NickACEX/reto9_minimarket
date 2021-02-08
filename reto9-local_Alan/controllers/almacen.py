#importamos metodos de  Modelo Libros
from models.productos import Productos
from helpers.menu import Menu
from helpers.helper import input_data, print_table, question

#Nuestros metodos
class AlmacenController:
    def __init__(self):
        self.productos=Productos()
        self.salir=False
    
    def menu(self):
        try:
            while True:
                print('''
                =============================
                      Almacen Productos
                =============================
                ''')
                lista_menu=['Listar Productos','Nuevo Producto','Editar Producto','Eliminar Producto','Salir']
                respuesta=Menu(lista_menu).show()

                if respuesta==1:
                    self.all_productos()
                elif respuesta==2:
                    self.insert_producto()
                elif respuesta==3:
                    self.search_producto_update()
                elif respuesta==4:
                    self.search_producto_delete()
                else:
                    self.salir=True
                    break  

        except Exception as e:
            print(f'{str(e)}')

    def all_productos(self):
        print('''
        =============================
              Listar Productos
        =============================
        ''')
        producto=self.productos.get_productos('producto_id')
        print(print_table(producto,['Producto_ID','Nombre','Stock','Precio Unit']))
        input('\nPresiona una tecla para continuar . . .')

    def insert_producto(self):
        nombre=input_data('Ingrese el Nombre del Producto : ')
        stock=input_data('Ingrese el stock por unidad del Producto : ')
        precio=input_data('Ingrese el precio unitario del Producto : ')
        self.productos.insert_producto({
            'nombre':nombre,
            'stock':stock,
            'precio':precio
        })
        print('''
        =============================
           Listar Libro Agregado
        =============================
        ''')    
        self.all_productos()

    
    def search_producto_update(self):
        self.all_productos()
        print('''
        =============================
               Buscar Producto
        =============================
        ''')
        try:
            producto_id=input_data('Ingrese el ID del Producto : ','int')
            producto=self.productos.get_producto({
                'producto_id': producto_id
            })
            #print(print_table(producto,['Producto_ID','Nombre','Stock','Precio Unit']))
            self.update_producto(producto_id)

        except Exception as e:
            print(f'{str(e)}')
        input('\nPresiona una tecla para continuar . . .')

    def search_producto_delete(self):
        self.all_productos()
        print('''
        =============================
               Buscar Producto
        =============================
        ''')
        try:
            producto_id=input_data('Ingrese el ID del Producto : ','int')
            producto=self.productos.get_producto({
                'producto_id': producto_id
            })
            #print(print_table(producto,['Producto_ID','Nombre','Stock','Precio Unit']))
            print(producto_id)
            self.delete_producto(producto_id)

        except Exception as e:
            print(f'{str(e)}')
        input('\nPresiona una tecla para continuar . . .')


    def update_producto(self, producto_id):
        nombre=input_data('Ingrese el Nombre del Producto : ')
        stock=input_data('Ingrese el stock por unidad del Producto : ')
        precio=input_data('Ingrese el precio unitario del Producto : ')
        self.productos.update_producto({
            'producto_id':producto_id
        },{
            'nombre':nombre,
            'stock':stock,
            'precio':precio
        })
        print('\n Datos del Producto Actualizado \n')

    def delete_producto(self, producto_id):
        self.productos.delete_producto({
            'producto_id':producto_id
        })
        print('\n Datos del Producto Actualizado \n')

