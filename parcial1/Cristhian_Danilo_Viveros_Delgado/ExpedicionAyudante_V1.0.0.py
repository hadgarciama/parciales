# ExpedicionAyudante v1.0.0
# Programa que mediante una base de datos analiza la informacion de minerales encontrados en cada luna de Urano
# y muestra las lunas viables para una futura expedicion

# Desarrollado por Cristhian Danilo Viveros Delgado
# Septiembre 17 de 2015

# Informacion de las Lunas mas importantes de Urano obtenidas de http://www.astromia.com/solar/urano.htm

# Importar libreria sys para manejo de argumentos de linea de comandos

import sys

# Importar libreria para manejo del sistema de archivos del sistema operativo.

import os

# --------------------------------Inicio de definicion parametros-------------------------------- #

# Nombre archivo de errores
nombre_errores = "errores.txt"

# Nombre archivo de registro del programa
nombre_reg = "reg.txt"

# Nombre archivo que contendra las lunas viables para la expedicion
nombre_expedicion = "expedicion.txt"

#Nombre archivo que contendra totales, promedios e informacion de las lunas de Urano
nombre_informe = "informe.txt"

#Numero minimo de lineas de archivo minimos
num_min=4

# -------------------------------------------------- Fin de definicion de parametros -------------------------------------------------- #

# Funcion 1 -> Validar existencia, nombre valido de archivo y extension .txt
def validar_archivo(nombre_archivo):
	archivo_valido = True
	
	# El archivo.txt debe existir.
	if(os.path.isfile(nombre_archivo) == False):
		guardar_reg("Error en existencia de archivo" + nombre_archivo)
		guardar_error("No existe archivo " + nombre_archivo)		
	else:
		guardar_reg("Archivo " + nombre_archivo + " Existe")
	# Validar que el nombre no contenga espacios.
	cantidad_palabras = len(nombre_archivo.split(" "))
	
	# Validando que no contenga espacios en su nombre.	
	if(cantidad_palabras > 1):
		archivo_valido = False
		guardar_reg("Error en nombre de archivo" + nombre_archivo)
		guardar_error("Nombre de archivo " + nombre_archivo+ " tiene mas de una palabra.")
	else:
		guardar_reg("Nombre de archivo " + nombre_archivo + " es valido")
	# Validando que la extension sea .txt
	if(not nombre_archivo.endswith(".txt")):
		archivo_valido = False
		guardar_reg("Error en extension de archivo" + nombre_archivo)
		guardar_error("Archivo " +nombre_archivo+ " no tiene extension .txt  ")
	else:
		guardar_reg("Extension de archivo " +nombre_archivo+ " es correcto")
	return archivo_valido
	
#  -------------------------------------------------- Fin de definicion de parametros  -------------------------------------------------- #

#  -------------------------------------------------- Inicio de definicion de funciones  -------------------------------------------------- #

# Funcion de revision de directorio.
def directory(path,extension):
  list_dir = []
  list_dir = os.listdir(path)
  count = 0
  for file in list_dir:
    if file.endswith(extension):
      count += 1
  return count


# Funcion que crear un archivo con el nombre especificado. Devuelve True si fue exitoso o False en caso de error.
def crear_archivo(nombre_archivo):
	try:
		archivo = open(nombre_archivo, 'w')
		archivo.close()
		guardar_reg("Archivo " + nombre_archivo + " creado exitosamente")
	except:
		guardar_error("Error creando archivo: " + nombre_archivo);
		return False
		
	return True


# Funcion que guarda un mensaje de error en el archivo errores.txt
def guardar_error(mensaje_error):
	escribir_linea_archivo(nombre_errores, "\n" + mensaje_error + "\n")
	
# Funcion que guarda un registro de operacion en el archivo reg.txt
def guardar_reg(mensaje_registro):
	escribir_linea_archivo(nombre_reg, "\n" + mensaje_registro + "\n")

# Funcion que termina el programa en caso de un error.
def terminar_programa(mensaje_terminacion):
	guardar_error(mensaje_terminacion)
	guardar_reg("Programa terminado por error... Verificar archivo errores.txt para mas detalles.")
	
	# Terminar el programa
	sys.exit()

#Funcion que escribe en una linea de el archivo especificado.
def escribir_linea_archivo(nombre_archivo, linea_a_escribir):	
	try:
		archivo = open(nombre_archivo, 'a')
		archivo.write(linea_a_escribir)
		archivo.close()
	except IOError:
		guardar_error("Error escribiendo linea " + linea_a_escribir + " en archivo " + nombre_archivo )
		return False
		
	return True

#Funcion que lee las lineas de un archivo especificado.
def leer_lineas_archivo(nombre_archivo):
	lineas = ()
	try:
		archivo = open(nombre_archivo, 'r')
		lineas = archivo.readlines()
		archivo.close()
	except IOError:
		guardar_error("Error leyendo archivo " + nombre_archivo)
		
	return lineas 

#Funcion para validar la estructura de la linea de archivo especificado.
def validar_linea(linea_por_validar, numero_linea):	
	array_respuesta = [0 for x in range(2)]
	
	# Separar la linea por el simbolo (igual) =
	arreglo_campos = linea_por_validar.split("=")	
	array_respuesta[0]=arreglo_campos[0]
	# Validar que el campo sea de tipo numerico
	try:
		minerales_minimos = int(arreglo_campos[1])								
		array_respuesta[1] = minerales_minimos
	except ValueError:
		guardar_error(arreglo_campos[1] + " no puede convertirse a entero!")
		return array_respuesta
	return array_respuesta

# ---------------------------------------- Fin de definicion de funciones empleadas ----------------------------------------------- #

#Inicializacion De Archivos

# Crear el archivo errores.txt para almacenar los errores que se presenten.
crear_archivo("errores.txt")

# Crear el archivo log.txt para almacenar el registro de operacion del programa.
crear_archivo("reg.txt")

#Verificando existencia de archivos de error y registro.

guardar_reg("Verificar existencia y validar nombres de archivos de error y de registro")

validar_archivo(nombre_errores)
validar_archivo(nombre_reg)

guardar_reg("Creados archivos errores.txt y reg.txt")

#Introduciendo argumentos de la linea de comandos

program_path = os.getcwd()

directorio = sys.argv[1]
nombre_minerales = sys.argv[2]
nombre_minimos = sys.argv[3]

#Validando Argumentos
validar_archivo(nombre_minerales)
validar_archivo(nombre_minimos)

#Leyendo Minimos Y Minerales
lineas_minerales=tuple(leer_lineas_archivo(nombre_minerales))
numero_lineas_minerales=len(lineas_minerales)

lineas_minimos=tuple(leer_lineas_archivo(nombre_minimos))
numero_lineas_minimos=len(lineas_minimos)

#Verificando que los archivos de Minimos y Minerales contengan la misma cantidad de minerales y lineas
if(numero_lineas_minimos!=numero_lineas_minerales and numero_lineas_minimos==num_min):
	terminar_programa("Los archivos Minerales.txt y Minimos.txt no tienen igual numero de lineas o no tienen igual cantidad de minerales")
else:
	guardar_reg("Archivos Minerales.txt y Minimos.txt compatibles")
# ------------------------------------------------ Inicio de logica de programa --------------------------------------------------- #
	
# Despues de realizar las lecturas y validaciones de los argumentos o variables del problema,
# se procede a realizar los calculos y procesamientos.

#Creando Array De Minimos

minimos = [[columnas for columnas in range(2)] for filas in range(numero_lineas_minimos)]

guardar_reg("Cargando Minimos en memoria");
for x in range(0,numero_lineas_minerales):
	linea_validada = validar_linea(lineas_minimos[x], x+1)
	guardar_reg("Procesando linea " + str(x+1));
	minimos[x][0] = linea_validada[0]
	minimos[x][1] = linea_validada[1]

guardar_reg("Minimos cargados en memoria!");

# Accediendo al directorio y procesando informacion presente

count=directory(sys.argv[1],'.txt')
if(count==0):
	terminar_programa("no hay archivos validos en el directorio")
i=0
mal=[[columnas for columnas in range(1)] for filas in range(100)]
lunas = [[columnas for columnas in range(1)] for filas in range(count)]
rootDir = directorio
for dirName, subdirList, fileList in os.walk(rootDir):
    guardar_reg("Directorio valido, Contando archivos validos en directorio");
    for fname in fileList:

		if(fname.endswith('.txt')):
			lunas[i][0] = fname
		else:
			mal[i][0]=fname
			i=i-1
		if(i!=(count-1)):
			i=i+1


guardar_reg("archivos contados y listados")
guardar_reg("procesando informacion del directorio")
os.chdir(directorio)


#Creando Arrays
array_array = [[columnas for columnas in range(6)] for filas in range(count)]
for x in range(0,count):
	array_array[x]=tuple(leer_lineas_archivo(lunas[x][0]))


array_validado = [[columnas for columnas in range(4)] for filas in range(count+1)]

i=0
j=1
while (j<count+1):
	for x in range(0, 4):
		linea_validada = validar_linea(array_array[i][x+2], x+3)
		array_validado[0][x] = linea_validada[0]
		array_validado[j][x] = linea_validada[1]
	i=i+1
	j=j+1

#Suministrando directorio para no insertar en linea de comandos una direccion completa
os.chdir(program_path)
guardar_reg("informacion del directorio procesada");
guardar_reg("creando array Suma");

#Creando Array De Suma

suma = [[columnas for columnas in range(1)] for filas in range(4)]

guardar_reg("Sumando minerales")
k=0	
while (k<4):
	for x in range(1,count+1):
		suma[k][0]+=int(array_validado[x][k])
	k=k+1

guardar_reg("Minerales sumados")

#Creando Array de promedios de Minerales

array_prom = [[columnas for columnas in range(1)] for filas in range(4)]

for x in range (0,4):
	array_prom[x][0]=suma[x][0]/count
	
guardar_reg("Minerales promediados")

#Creando arrays de comparacion para determinar las lunas para una futura expedicion.

array_comparacion = [[columnas for columnas in range(4)] for filas in range(count)]

guardar_reg("comparando datos de minimos de los archivos de lunas")
k=1
i=0
while (k<count+1):
	for x in range (0,4):
		array_comparacion[i][x]=array_validado[k][x]-minimos[x][1]
	k=k+1
	i=i+1
guardar_reg("Comparacion Completada")

# Creando  y escribiendo archivos de expedicion y registro.

guardar_reg("Creando Archivo de Expedicion")
crear_archivo("expedicion.txt")
i=0
while (i<count-1):
	for x in range(0, 1):
		if(array_comparacion[i][x]>0 and array_comparacion[i][x+1]>0 and array_comparacion[i][x+2]>0 and array_comparacion[i][x+3]):
			
			escribir_linea_archivo(nombre_expedicion, lunas[i][0] + "\n")	
		i=i+1

guardar_reg("Creando Archivo Informe.txt")
crear_archivo("informe.txt")

totales=str('TOTALES')
fortotales="%s\n\n"
escribir_linea_archivo(nombre_informe, fortotales % (totales))
for x in range (0,4):
	contenido_linea1 = ( 
		minimos[x][0], suma[x][0],
	)
	formato_linea1 = "\t%s %d\n\n"
	escribir_linea_archivo(nombre_informe, formato_linea1 % (contenido_linea1))

promedio=str('PROMEDIO'),
forprom="%s\n\n"
escribir_linea_archivo(nombre_informe, forprom % (promedio))		
for x in range (0,4):
	contenido_linea1 = (	
		minimos[x][0], array_prom[x][0],
	)
	formato_linea1 = "\t%s %d\n\n"
	escribir_linea_archivo(nombre_informe, formato_linea1 % (contenido_linea1))
	
datlun=str('DATOS BARRIOS'),
fordatlun="%s\n\n"
escribir_linea_archivo(nombre_informe, fordatlun % (datlun))
for x in range(0, count):
	contenido_linea2 = (
		lunas[x][0],array_array[x][0],array_array[x][1],	
	)
	formato_linea2 = "\t%s %s \t%s\n "
	escribir_linea_archivo(nombre_informe, formato_linea2 % (contenido_linea2))

#Verificacion de existencia y validacion de archivos de informe y expedicion.

guardar_reg("Archivo Informes.txt escrito exitosamente")
guardar_reg("Verificando que existan los archivos de informe y expedicion.")
validar_archivo(nombre_expedicion)
validar_archivo(nombre_informe)
guardar_reg("Verificaciones Completadas")

#Programa completado

guardar_reg("Programa Finalizado con exito, ver archivos ")

#-----------------------------------------Fin Del Programa----------------------------------------------------------------



