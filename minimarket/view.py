from msvcrt import kbhit,getch

class MenuView:

    def __init__(self,nombres_menu={},titulo="MENU"):
        """
            nombres_menu(dict): key -> nombres del menu, value -> accion del menu 
            titulo(str): titulo del MENU
        """
        titulo = f'*{" "*8}{titulo}{" "*8}*'
        
        #titulo
        print("*"*len(titulo))
        print(f"*{' '*(len(titulo)-2)}*")
        print(titulo)
        print(f"*{' '*(len(titulo)-2)}*")
        print("*"*len(titulo))
        #titulo

        self.nombres_menu = nombres_menu
        index = 0
        for i in nombres_menu.keys():
            print(f"{index+1}. {i}")
            index += 1


    def ejecutar_accion(self):
        try:
            opcion = int(input("Ingrese opcion: "))
            print()#para separacion
            rpta = tuple(self.nombres_menu.values())[opcion-1]()
            return rpta
        except (IndexError,ValueError) as e:
            print("Elija una opcion valida")
            print(str(e))


class Tabla:

    def __init__(self,datos):
        self.__data = datos

    def __separator(self,data,list_high):
        print()
        for i in data:
            print("-"*(list_high[i]+2),end="")
        print()

    def mostrar_tabla(self):
        list_high = {}
        number_row = 0
        for i in self.__data:
            size_data = len(self.__data[i])
            if number_row < size_data:
                number_row = size_data
            high = len(i) 
            for j in self.__data[i]:
                size_element = len(str(j))
                if high < size_element:
                    high = size_element
            list_high[i] = high
        
        for i in self.__data:#print title
            print(i.title(),end=" "*(list_high[i]-len(i)+1)+"|")
        
        self.__separator(self.__data,list_high)

        index = 0
        while index < number_row:
            for i in self.__data:
                if index >= len(self.__data[i]):
                    self.__data[i].append("")
                element = self.__data[i][index]
                print(element,end = " "*(list_high[i]-len(str(element))+1)+'|')
            self.__separator(self.__data,list_high)
            index += 1

    def elegir_opcion(self):
        try:
            opcion = int(input("Ingrese codigo de producto: "))
            if int(opcion) in self.__data['Codigo']:
                return int(opcion)
            else:
                print("El codigo que ha ingresado no se encuentra en la tabla")
        except ValueError:
            print("Ingrese solo un numero entero.")

 
def pedir_contrasena(indicacion="Ingrese un valor: "):
    """
        indicacion(str): opcional,mensaje que indica que valor ingresar
    """
    print(indicacion,end="",flush=True)
    valor = ""
    while True:
        if kbhit():
            letra = getch().decode()
            if letra == '\r' or letra == '\n':
                break
            elif letra == '\x08':
                valor = valor[:-1]
                print("\b \b",end="",flush=True)
            else:
                valor += letra
                print("*",end="",flush=True)
    
    print()
    return valor