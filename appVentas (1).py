
import csv
import os
import string
from tempfile import NamedTemporaryFile
import shutil
import csv
import uuid

#DEFINIMOS LAS CLASES DEL MODELO DE LA APLICACIÓN 

class Productos:
    def __init__(self):
        self.__impuesto  =  1.19  
    
    def get_impuesto(self):
        impuesto  =  self.__impuesto
        return impuesto

class Carro:
    def __init__(self,numerodeP,precio,total):
        self.SKU                      = uuid.uuid4()
        self.numerodeP                = numerodeP
        self.precio                   = precio
        self.total                    = total
        self.dicc_Carro_con_productos = {}

class Pago:
    def __init__(self,nombre,tipoTarjeta,numeroTarjeta):
        self.IDcliente       = uuid.uuid4()
        self.nombre          = nombre
        self.tipoTarjeta     = tipoTarjeta
        self.__numeroTarjeta = numeroTarjeta

class Usuario:
    def __init__(self, nombre):
        self.ID            = uuid.uuid4()
        self.nombre        = nombre
        self.dicc_Productos = {}
    
    def verProducto(self):
        pass

class Admin(Usuario):

    def agregarProducto(self,nombre_archivo):
        opcion = int(input('1---> Agregar | 2---> salir: '))
        while opcion == 1:
            with open(nombre_archivo,'a') as archivo_csv: # ABRO EL ARCHIVO CSV PARA AGREGAR UN PRODUCTO
                escribir    = csv.writer(archivo_csv, delimiter = ',')  # CREO LA VARIABLE ESCRIBIR PARA INGRESAR EL PRODUCTO  
                SKU         = input('Ingrese el código del producto: ') # INGRESO LOS DATOS DEL PRODUCTO 
                nombreP     = 'producto'#input('Ingrese el Nombre del producto: ')
                categoriaP  = 'producto'#input('Ingrese el Categoría del producto: ')
                stockP      = 'producto'#input('Ingrese el Stock del producto: ')
                valor_netoP = 'producto'#input('Ingrese el Valor Neto del producto: ')
                datos       = {} # CREO UN DICCIONARIO VACIO PARA INGRESAR LOS DATOS CON CLAVE Y VALOR
                for variable in ['nombreP','categoriaP','stockP','valor_netoP']: # RECORRO CADA CLAVE PARA ASIGNARLE SU VALOR CORRESPONDIENTE
                    datos[variable]  =  eval(variable) # ASIGNO LOS VALORES AL DICCIONARIO DATOS CON SUS RESPECTIVAS CLAVES
                print(datos)
                self.dicc_Productos[SKU]  =  datos # AL DICCIONARIO DE LA CLASE ADMIN LE AGREGO LOS DATOS DE LOS PRODUCTOS
                print(self.dicc_Productos)
                escribir.writerow([SKU,nombreP,categoriaP,stockP,valor_netoP]) # FINALEMENTE AGREGO AL CSV LOS DATOS DE LOS PRODUCTOS
                os.system('cls') # LIMPIO LA PANTALLA 
                print('Desea Agregar otro producto')
                opcion = int(input('1---> agregar | 2---> salir : '))
        return f'El producto ha sido Agregado exitosamente'

    def eliminarProducto(self,nombre_archivo):
        opcion  =  int(input('1---> Eliminar | 2---> salir: '))
        while opcion ==  1:
            with open(nombre_archivo,"r+") as f: # ABRO EL ARCHIVO PARA BUSCAR LA FILA QUE DESEO ELIMINAR 
                new_f  =  f.readlines() # ASIGNO ESTE LECTURA DE ARCHIVO A LA VARIABLE new_f
                f.seek(0) # CON LA FUNCION SEEK BUSCO POR CADA CARACTER INCIANDO EN EL CARACTER 0
                SKU  = str(input('Ingrese el codigo del producto: ')) # INGRESE EL DATO QUE QUIERO ELIMINAR
                for line in new_f: # RECORRO CADA LINIA DE new_f PARA BUSCAR EL DATO A ELIMINAR
                    if SKU not in line: # SI EL DATO INGRESADO POR CONSOLA NO ESTA EN line ESCRIBE SOBRE EL ARCHIVO f 
                        f.write(line) # ESCRIBO SOBRE EL ARCHIVO f LAS FILAS QUE NO CONTENGAN EL DATO INGRESADO
                f.truncate() # CAMBIO EL TAMAÑO DEL ARCHIVO AL NUMERO DADO DE BYTE SI NO SE ESPECIFICA, SE UTILIZA LA POSICION ACTUAL 
            os.system('cls')
            #Se elimina el dato del diccionario
            del self.dicc_Productos[SKU]
            print('Desea Eliminar otro producto')
            opcion = int(input('1---> Eliminar | 2---> salir : '))
            return f'El producto ha sido eliminado exitosamente'

    def modificarProducto(self,nombre_archivo):
        opcion = int(input('1---> Modificar | 2---> salir: '))
        while opcion == 1:
            filename  =  nombre_archivo # SE ASIGNA EL ARCHIVO A MODIFICAR EN LA VARIABLE FILENAME
            tempfile  =  NamedTemporaryFile(mode='w', delete=True) # SE CREA EL ARCHIVO TEMPORAL, CON LOS ATRIBUTOS MODE = ESCRITURA, Y DELETE = FALSE, QUE SIGNIFICA QUE NO SE ELIMINARA DIRECTAMENTE

            fields = ['SKU','nombreP','categoriaP','stockP','valor_netoP'] # SE GENERA LA LISTA DE CAMPOS QUE SE SOBREESCRIBIRAN PARA LUEGO SER LAS LLAVES DEL DICCIONARIO QUE SE SOBREESCRIBIRA

            with open(filename, 'r', encoding='utf8') as csvfile, tempfile: # SE ABRE EL ARCHIVO QUE DESEAMOS MODIFICAR
                reader = csv.DictReader(csvfile, fieldnames=fields) # PRIMERO LEEMOS EL ARCHIVO CSVFILE CON EL ATRIBUTO FIELDNAME PARA MAPEAR LAS CLAVES ASIGNADAS A FIELDS 
                writer = csv.DictWriter(tempfile, fieldnames=fields) # ESCRIBIMOS EN EL ARCHIVO TEMPFILE LOS DATOS QUE TIENE CADA CLAVE PARA MODIFICARLOS
                SKU =  input('Ingrese el código del producto: ')
                nombreP = input('Ingrese el Nombre del producto: ')
                categoriaP = input('Ingrese el Categoría del producto: ')
                stockP = input('Ingrese el Stock del producto: ')
                valor_netoP = input('Ingrese el Valor Neto del producto: ')
                self.dicc_Productos.update({SKU : {'nombreP': nombreP, 'categoriaP': categoriaP, 'stockP': stockP, 'valor_netoP': valor_netoP}})
                for row in reader: # RECORREMOS CADA FILA DEL ARCHIVO CSVFILE
                    if row['SKU'] == SKU: # SI LA FILA DE SKU ES IGUAL AL INPUT DE SKU MODIFICAMOS SU VALOR
                        print('updating row', row['SKU'])
                        row['nombreP'], row['categoriaP'], row['stockP'], row['valor_netoP'] = nombreP, categoriaP, stockP, valor_netoP # MODIFICAMOS CADA VALOR DE ESA FILA
                    row = {'SKU': row['SKU'], 'nombreP': row['nombreP'], 'categoriaP': row['categoriaP'], 'stockP': row['stockP'], 'valor_netoP': row['valor_netoP']} # INGRESAMOS A LA FILA COMO DICCIONARIO Y AGREGAMOS CADA VALOR MODIFICADO 
                    writer.writerow(row) # ESCRIBIMOS LOS VALORES EN ESTE DICCIONARIO
            shutil.move(tempfile.name, filename)  # FINALEMNTE MOVEMOS ESTOS DATOS AL ARCHIVO ORIGINAL, CON LOS DATOS MODIFICADOS 
            print(self.dicc_Productos)
            print('Desea Modificar otro producto')
            opcion = int(input('1---> Modificar | 2---> salir : '))
            return f'El producto ha sido Modificado exitosamente'         

    def realizarEnvio(self):
        pass

    def confirmarEntrega(self):
        pass

class Cliente(Usuario):
    def __init__(self, nombre,correo, telefono,saldo):
        self.ID = uuid.uuid4()
        self.nombre   = nombre
        self.correo   = correo
        self.telefono = telefono  
        self.saldo    = saldo

    def agregarAcarro(self,archivo_producto,archivo_carro):
        opcion = int(input('1---> Agregar | 2---> salir: '))
        while opcion == 1:
            with open(archivo_producto, "r") as f:
                lines = f.readlines()
                nombreP = str(input('Agregue el producto a carro'))
                for separador in lines:
                    lista = separador.split(',')
                    print(lista)
                    print(lista[1])
                    if nombreP == lista[1]:
                        lines.remove(lista)              
                with open(archivo_carro, "w") as new_f:
                    for line in lines:        
                        new_f.write(line)
            print('Desea Agregar otro producto')
            opcion = int(input('1---> Agregar | 2---> salir : '))
            return f'El producto ha sido Agregado exitosamente'  
            


# PROBANDO METODOS AGREGAR, ELIMINAR Y MODIFICAR PRODUCTO
#producto1 = Productos('zapatos','Ropa',100,20000)
#producto2 = Productos('zapatosdefutnol','Ropa',10,50000)
administrador1 = Admin('neifer')
cliente1 = Cliente('neifer','aaaaa@aaaaa','1234560',200000)
#administrador1.agregarProducto('data/productos.csv')
#print(administrador1.dicc_Productos)
#administrador1.eliminarProducto('data/productos.csv')
#print(administrador1.dicc_Productos)
#administrador1.modificarProducto('data/productos.csv')
#print(administrador1.dicc_Productos)
cliente1.agregarAcarro('data/productos.csv','data/productoCarro.py')
