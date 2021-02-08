#importamos metodos de  Modelo Libros
from models.productos import Productos
from models.facturas import Facturas
from helpers.menu import Menu
from helpers.helper import input_data, print_table, question
from datetime import datetime


#Nuestros metodos
class FacturaController:
    def __init__(self):
        self.productos=Productos()
        self.facturas=Facturas()
        self.now = datetime.now()
        self.salir=False
    
    def menu(self):
        try:
            while True:
                print('''
                =============================
                      Consola Facturas
                =============================
                ''')
                lista_menu=['Listar Ventas','Nueva Venta','Salir']
                respuesta=Menu(lista_menu).show()

                if respuesta==1:
                    self.all_facturas()
                elif respuesta==2:
                    self.nueva_factura()
                else:
                    self.salir=True
                    break  

        except Exception as e:
            print(f'{str(e)}')

    def all_facturas(self):
        print('''
        =============================
              Listar Facturas
        =============================
        ''')
        factura=self.facturas.get_facturas('factura_id')
        print(print_table(factura,['Factura_ID','Productoi_Id','Fecha Registro','Cantidad','Costo']))
        input('\nPresiona una tecla para continuar . . .')

    def all_productos(self):
        print('''
        =============================
              Listar Productos
        =============================
        ''')
        producto=self.productos.get_productos('producto_id')
        print(print_table(producto,['Producto_ID','Nombre','Stock','Precio']))
        input('\nPresiona una tecla para continuar . . .')
    

   
    def nueva_factura(self):
        try:
            while True:
                print('''
                =============================
                       Carrito Compras
                =============================
                ''')
                opciones = ['Agregar Producto', 'Eliminar Producto','Terminar', 'Salir']
                respuesta = Menu(opciones).show()           
                if respuesta == 1:
                    self.all_productos()
                    prod_id = input_data("Ingrese el ID del Producto >> ", "int")
                    self.insert_producto(prod_id)
                elif respuesta == 2:
                    pass
                elif respuesta == 3:
                    pass
                else:
                    self.salir=True
                    break  
        except Exception as e:
            print(f'{str(e)}')
        input('\nPresiona una tecla para continuar...')
    

    def insert_producto(self, producto_id):
        print('''
        Nota: Solo puedes agregar 1 vez el producto
        ''')
        factid=self.facturas.get_by_id_column_top('factura_id')
        if factid:
            factura_id=factid[0]+1
        else:
            factura_id=1

        fecha_reg=datetime.now()
        cantidad=input_data('Ingrese la Cantidad del Producto : ')
        valorx=int(cantidad)
        valory=self.productos.get_by_id_column({
            'producto_id': producto_id
        },'precio')
        costo=int(cantidad)*valory[0]
        self.facturas.insert_factura({
            'factura_id':factura_id,
            'producto_id':int(producto_id),
            'fecha_registro':fecha_reg,
            'cantidad':cantidad,
            'costo':costo
        })
        self.update_producto(producto_id, valorx)
        print('''
        ***Producto Agregado***
        ''')    
     
    
    def update_producto(self,producto_id,valorx):
        can1=self.productos.get_by_id_column({
            'producto_id': producto_id
        },'stock')
        can2=can1[0]-int(valorx)
        self.productos.update_producto({
            'producto_id': producto_id
        }, {
            'stock': can2
        })
    


