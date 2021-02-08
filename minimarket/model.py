from psycopg2 import connect
from werkzeug.security import check_password_hash,generate_password_hash
from time import strftime

class Conector:

    def __init__(
            self,nombre_base="minimarket",
            usuario="postgres",
            contrasena="passwordpost_97"):
        self.nombre_base = nombre_base
        self.usuario = usuario
        self.contrasena = contrasena

    def __conectar(self):
        conexion = connect(
            dbname=self.nombre_base,
            user = self.usuario,
            password = self.contrasena
            )
        cursor = conexion.cursor()
        return conexion,cursor

    def __cerrar_conexion(self,conexion,cursor):
        cursor.close()
        conexion.close()
    
    def insertar(self,tabla,campos,valores):
        """
            tabla(str): nombre de la tabla\n
            campos(str): nombre de los campos donde se insertara los valores separados por comas (,)\n
            valores(tuple): tupla de los valores a insertar 
        """
        conexion,cursor = self.__conectar()
        instruccion = f"""
        insert into {tabla}({campos})
        values({('%s,'*len(valores))[:-1]})"""
        
        cursor.execute(instruccion,valores)
        conexion.commit()
        self.__cerrar_conexion(conexion,cursor)

    def actualizar(self,tabla,campos,donde,valores):
        """
            tabla(str): nombre de la tabla
            campos(str): nombre de los campos donde se insertara los valores separados por comas (,)
            donde(str):  condicion de la consulta
            valores(tuple): tupla de los valores a que reemplazan a %s
        """
        conexion,cursor = self.__conectar()
        instruccion = f"""update {tabla}
        set {campos}
        where {donde}"""
        cursor.execute(instruccion,valores)
        conexion.commit()
        self.__cerrar_conexion(conexion,cursor)

    def eliminar(self,tabla,condicion,valores):
        """
            tabla(str):nombre de la tabla
            condicion(str):nombre del campo o campos a evaluar con =%s
            valores(tuple): tupla de valores que reemplaza a %s
        """
        conexion,cursor = self.__conectar()
        instruccion = f"""delete from {tabla}
        where {condicion}"""
        cursor.execute(instruccion,valores)
        conexion.commit()
        self.__cerrar_conexion(conexion,cursor)

    def seleccionar(self,campos,tabla,condicion="",valores=(),todo=False):
        """
            campos(str):nombre de los campos a seleccionar separados por comas (,)
            tabla(str): nombre de la tabla
            condicion(str):opcional.Si desea especificar la busqueda
            valores(str):opcion. valores a analizar en la condicion
            todo(bool): si desea obtener todos los datos encontrados, por defecto es False
            return(None o tupla): si todo = False
            return(Lista): si todo =True
        """
        conexion,cursor = self.__conectar()
        instruccion = f"""select {campos} from {tabla}"""
        if condicion != "":
            instruccion += f"""
            where {condicion}"""
            cursor.execute(instruccion,valores)
        else:
            cursor.execute(instruccion)

        if todo:
            datos = cursor.fetchall()
        else:
            datos = cursor.fetchone() 

        self.__cerrar_conexion(conexion,cursor)

        return datos


class Trabajador:
    def __init__(self,nombre,correo,nivel):
        self.__nombre = nombre
        self.__correo = correo
        self.__nivel = nivel

    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def correo(self):
        return self.__correo

    @property
    def nivel(self):
        return self.__nivel

    @correo.setter
    def correo(self,correo):
        conector = Conector()
        conector.actualizar("trabajador",
            "correo=%s",
            "correo=%s",
            (correo,self.__correo)
            )
        self.__correo = correo

    def cambiar_contrasena(self,contrasena):
        contrasena_encriptada = generate_password_hash(contrasena,'sha256')
        conector = Conector()
        conector.actualizar("trabajador",
        "contrasena=%s",
        "correo=%s",
        (contrasena_encriptada,self.__correo))
        
    @staticmethod
    def obtener_trabajador(correo,contrasena):
        conector = Conector()
        datos_trabajador = conector.seleccionar("nombre,correo,idnivel,contrasena",
            "trabajador",
            "correo=%s",
            (correo,)
            )
        
        if datos_trabajador:
            if check_password_hash(datos_trabajador[-1],contrasena):
                nivel = conector.seleccionar("nombre","nivel","id=%s",(datos_trabajador[2],))
                if nivel[0] == "almacen":
                    return Almacenador(datos_trabajador[0],
                    datos_trabajador[1],
                    nivel[0])
                elif nivel[0] == "cajero":
                    return Cajero(datos_trabajador[0],
                    datos_trabajador[1],
                    nivel[0])
                else:
                    return Administrador(datos_trabajador[0],
                    datos_trabajador[1],
                    nivel[0])
        else:
            return None


class Almacenador(Trabajador):
    def __init__(self, nombre, correo, nivel):
        super().__init__(nombre, correo, nivel)

    def agregar_producto(self,codigo,precio,nombre):
        """ guarda productos en la base de datos
        """
        Producto.agregar_producto(codigo,precio,nombre)
    
    def eliminar_producto(self,codigo):
        Producto.eliminar_producto(codigo)

    def cambiar_nombre_producto(self,codigo,nombre):
        producto = Producto.obtener_producto(codigo)
        producto.nombre= nombre
    
    def cambiar_precio_producto(self,codigo,precio):
        producto = Producto.obtener_producto(codigo)
        producto.precio = precio

class Cajero(Trabajador):
    def __init__(self, nombre, correo, nivel):
        super().__init__(nombre, correo, nivel)


class Producto:
    def __init__(self,codigo,precio,nombre):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__precio = precio

    def __eq__(self,codigo):
        return self.__codigo == codigo

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self,nombre):
        conector = Conector()
        conector.actualizar("producto",
            "nombre=%s",
            "codigo=%s",
            (nombre,self.__codigo))
        self.__nombre = nombre

    @property
    def precio(self):
        return self.__precio

    @precio.setter
    def precio(self,precio):
        conector = Conector()
        conector.actualizar("producto",
            "precio=%s",
            "codigo=%s",
            (precio,self.__codigo))
        self.__precio = precio

    @staticmethod
    def agregar_producto(codigo,precio,nombre):
        """ guarda productos en la base de datos
        """
        conector = Conector()
        conector.insertar("producto",
            "codigo,precio,nombre",
            (codigo,precio,nombre))
        print("Se agrego el producto correctamente")

    @staticmethod
    def eliminar_producto(codigo):
        """eliminar productos de la base de datos
        """
        conector = Conector()
        conector.eliminar("producto",
            "codigo=%s",
            (codigo,))

        print("Se eliminó el producto correctamente")

    @staticmethod
    def obtener_producto(codigo):
        conector = Conector()
        producto = conector.seleccionar("codigo,precio,nombre",
            "producto",
            "codigo=%s",
            (codigo,))

        return Producto(producto[0],producto[1],producto[2])

    @staticmethod
    def obtener_id_producto(codigo):
        conector = Conector()
        id_producto = conector.seleccionar("id",
            "producto",
            "codigo=%s",
            (codigo,))

        return id_producto


class Persona:
    def __init__(self,dni,nombre):
        self.__dni = dni
        self.__nombre = nombre
        self.__carrito = []

    @staticmethod
    def obtener_nombre_id(id_persona):
        conector = Conector()
        dni = conector.seleccionar("dni",
        "cliente",
        "id=%s",
        (id_persona,)
        )
        return dni[0]


    def agregar_producto_carrito(self,codigo):
        if codigo in self.__carrito:
            print("El producto ya ha sido agregado")
        else:    
            producto = Producto.obtener_producto(codigo)
            self.__carrito.append(producto)
            print("Se agregó el producto al carrito")

    def eliminar_producto_carrito(self,codigo):
        if codigo in self.__carrito:
            self.__carrito.remove(codigo)
        else:
            print("Ese producto no se encuentra en el carrito.")

    @property
    def dni(self):
        return self.__dni

    @property
    def nombre(self):
        return self.__nombre

    @property
    def carrito(self):
        return self.__carrito

    @staticmethod
    def crear_persona(self,dni,nombre):
        conector = Conector()
        conector.insertar("cliente",
            "dni=%s,cliente=%s",
            (dni,nombre),
            )
    
    @staticmethod
    def obtener_id(dni):
        conector = Conector()
        conector.seleccionar("id",
            "cliente",
            "dni=%s",
            (dni,)
            )

class Administrador(Trabajador):
    def __init__(self, nombre, correo, nivel):
        super().__init__(nombre, correo, nivel)

    def obtener_productos(self):
        conector = Conector()
        productos = conector.seleccionar("codigo,precio,nombre",
            "producto",
            todo=True
            )
        return productos

    def crear_trabajador(self,nombre,correo,contrasena,idnivel):
        contrasena_encriptada = generate_password_hash(contrasena,'sha256')
        conector = Conector()
        conector.insertar('trabajador',
            'nombre,correo,contrasena,idnivel',
            (nombre,correo,contrasena_encriptada,idnivel)
            )
        print("el trabajador ha sido registrado con exito")

class Nivel:
    def __init__(self,nombre):
        self.nombre = nombre

    @staticmethod
    def obtener_nombres():
        conector = Conector()
        niveles = conector.seleccionar("nombre",'nivel',todo=True)
        return niveles

class Factura:

    @staticmethod
    def obtener_facturas():
        conector = Conector()
        facturas = conector.seleccionar("*",
        "factura",
        todo=True
        )

        return facturas

    @staticmethod
    def crear_factura(persona):
        """crea la factura en la base de datos
        """
        conector = Conector()
        cliente = conector.seleccionar("id,dni,nombre",
            "cliente",
            "dni=%s",
            (persona.dni,)
            )
        if cliente:
            id_factura = int(cliente[0]) + 1
        else:
            Persona.crear_persona(persona.dni,persona.nombre)
            id_factura = 1

        codigo_factura = f"{persona.dni}-{id_factura}"
        id_cliente = Persona.obtener_id(persona.dni)
        fecha_emision = strftime("%d/%m/%y")
        
        conector.insertar('factura',
            'codigofactura,idcliente,fechaemision',
            (codigo_factura,id_cliente,fecha_emision)
            )

        for i in persona.carrito:
            conector.insertar('factura_producto',
                "idfactura,idproducto",
                (id_factura,Producto.obtener_id_producto(i.codigo))
                )

