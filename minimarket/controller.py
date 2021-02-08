from view import MenuView,pedir_contrasena,Tabla
from model import Administrador, Factura, Trabajador,Persona,Nivel

def run():
    print("INICIAR SESION")
    correo = input("Correo: ")
    contrasena = pedir_contrasena("Contraseña: ")

    trabajador = Trabajador.obtener_trabajador(correo,contrasena)

    if trabajador is None:
        print("Algunos de los datos ingresados son incorrectos")
    else:
        while True:
            print(f"Bienvenido {trabajador.nombre}")

            if trabajador.nivel == "almacen":
                controlador = Controlador_Almacen(trabajador)
                menu = MenuView({
                    'Cambiar correo': controlador.cambiar_correo,
                    'Cambiar contraseña':controlador.cambiar_contrasena,
                    'Agregar producto':controlador.agregar_producto,
                    'Eliminar producto':controlador.eliminar_producto,
                    'Cambiar nombre de producto: ':controlador.cambiar_nombre_producto,
                    'Cambiar precio de producto':controlador.cambiar_precio_producto,
                    'Salir':exit
                },titulo="MENU")
                menu.ejecutar_accion()

            elif trabajador.nivel == "cajero":
                controlador = Controlador_Cajero(trabajador)
                menu = MenuView({
                    'Cambiar correo': controlador.cambiar_correo,
                    'Cambiar contraseña':controlador.cambiar_contrasena,
                    'Crear Factura':controlador.crear_factura,
                    'Salir':exit
                })
                menu.ejecutar_accion()
            else:
                controlador = Controlador_Administrador(trabajador)
                menu = MenuView({
                    'Cambiar correo': controlador.cambiar_correo,
                    'Cambiar contraseña':controlador.cambiar_contrasena,
                    'Ver productos':controlador.ver_productos,
                    'Ver reportes':controlador.ver_facturas,
                    'Crear Trabajador':controlador.crear_trabajador,
                    'Salir':exit
                })
                menu.ejecutar_accion()

            continuar = input("Desea continuar? (s/n): ").lower().strip()

            if continuar != 's':
                break

class Controlador_Trabajador:
    
    def __init__(self,trabajador):
        self.__trabajador = trabajador

    @property
    def trabajador(self):
        return self.__trabajador

    def cambiar_correo(self):
        nuevo_correo = input("Ingrese el nuevo correo: ")
        self.__trabajador.correo = nuevo_correo
    
    def cambiar_contrasena(self):
        nueva_contrasena = pedir_contrasena("Ingrese nueva contraseña: ")
        self.__trabajador.cambiar_contrasena(nueva_contrasena)


class Controlador_Almacen(Controlador_Trabajador):
    
    def __init__(self, trabajador):
        super().__init__(trabajador)

    def agregar_producto(self):
        codigo = input("Ingrese codigo del producto: ")
        precio = float(input("Ingrese precio del producto: "))
        nombre = input("Ingrese el nombre del producto: ")

        self.trabajador.agregar_producto(codigo,precio,nombre)

    def eliminar_producto(self):
        codigo = input("Ingrese codigo del producto a eliminar: ")
        self.trabajador.eliminar_producto(codigo)

    def cambiar_nombre_producto(self):
        codigo = input("Ingrese codigo del producto a editar: ")
        nombre = input("Ingrese nuevo nombre del producto: ")
        self.trabajador.cambiar_nombre_producto(codigo,nombre)
        print("se cambio el nombre del producto satisfactoriamente")
    
    def cambiar_precio_producto(self):
        codigo = input("Ingrese codigo del producto a editar: ")
        precio = float(input("Ingrese nuevo precio del producto: "))
        self.trabajador.cambiar_precio_producto(codigo,precio)    
        print("se cambio el precio del producto satisfactoriamente")

class Controlador_Cajero(Controlador_Trabajador):

    def __init__(self, trabajador):
        super().__init__(trabajador)

    def crear_factura(self):
        dni = input("Ingrese dni del cliente: ")
        nombre = input("Ingrese nombre del cliente: ")
        persona = Persona(dni,nombre)
        controlador_carrito = Controlador_Carrito(persona)
        while True:
            menu_carrito = MenuView({
                    "Agregar al carrito":controlador_carrito.agregar,
                    "Eliminar del carrito":controlador_carrito.eliminar,
                    "Salir":controlador_carrito.salir
                },
                titulo="Carrito")
            rpta = menu_carrito.ejecutar_accion()
            if rpta == "salir":
                break

        print("Los productos ingresados son: ")
        tabla = Tabla({
            'Codigo':[i.codigo for i in persona.carrito],
            'Nombre':[i.nombre for i in persona.carrito],
            'Precio':[i.precio for i in persona.carrito]
        })
        tabla.mostrar_tabla()

        conforme = input("Conforme? (s/n): ").strip()
        if conforme != 's':
            print()
        else:
            Factura.crear_factura(persona)

class Controlador_Carrito:
    
    def __init__(self,persona):
        self.__persona = persona

    def agregar(self):
        codigo = input("Ingrese codigo del producto: ")
        self.__persona.agregar_producto_carrito(codigo)
            
    def eliminar(self):
        codigo = input("Ingrese codigo del producto: ")
        self.__persona.eliminar_producto_carrito(codigo)

    def salir(self):
        return 'salir'

    
class Controlador_Administrador(Controlador_Trabajador):

    def __init__(self, trabajador):
        super().__init__(trabajador)

    def ver_productos(self):
        productos = self.trabajador.obtener_productos()
        if productos:
            tabla = Tabla({
                'Codigo':[i[0] for i in productos],
                'Precio':[i[1] for i in productos],
                'Nombre':[i[2] for i in productos]
            })
            tabla.mostrar_tabla()
        else:
            print("Aun no hay productos registrados")

    def ver_facturas(self):
        facturas = Factura.obtener_facturas()
        if facturas:
            tabla = Tabla({
                'Codigo':[i[1] for i in facturas],
                'dni':[Persona.obtener_nombre_id(i[2]) for i in facturas],
                'fecha emision':[i[3] for i in facturas]
            })
        else:
            print("Aun no hay facturas registradas")

    def crear_trabajador(self):
        nombre = input("Ingrese nombre del trabajador ")
        correo = input("Ingrese correo del trabajador: ")
        contrasena = pedir_contrasena("Ingrese contraseña del trabajador: ")
        print("Niveles: ")
        niveles = Nivel.obtener_nombres()
        
        indice = 1
        for i in niveles:
            print(f"{indice}. {i[0]}")
            indice += 1
        nivel = input("Ingrese nivel: ")

        self.trabajador.crear_trabajador(nombre,correo,contrasena,nivel)