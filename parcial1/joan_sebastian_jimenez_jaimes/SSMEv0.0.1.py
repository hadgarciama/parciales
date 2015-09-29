# Sistem Sun Mineral Explorer(SSME)
'''
Programa capaz de recolectar informacion de ciertos minerales de cada planeta del sistema solar.
Este programa es capaz de comparar la informacion obtenida con una informacion "minima" de la cual depende
una futura expedicion y genera un informe basado en los datos anteriores.
'''
# Desarrollado por Joan Sebastian Jimenez Jaimes
# Septiembre 17 de 2015

# Se importa la libreria sys para el manejo de argumentos en la linea de comandos.
import sys

# Se importa libreria os para el manejo del directorio.
import os

# Se importa libreria os path para el manejo del directorio.
import os.path

#--------------------------------------Se definen las constantes y los parametros--------------------------------------

# Cantidad minima de archivos en el directorio.
minimo_archivos_en_directorio = 1

# Nombre archivo de errores.
nombre_archivo_errores = "error.txt"

# Nombre archivo de registro de operacion del programa.
nombre_archivo_registro = "log.txt"

# Nombre archivo de informe.
nombre_archivo_informe = "informe.txt"

# Nombre archivo de expedicion.
nombre_archivo_expedicion = "expedicion.txt"

# Nombre de archvo con recursos.
nombre_archivo_recursos = "recursos.txt"

# Nombre de archivo de minimos.
nombre_archivo_minimos = "minimo.txt"

# Numero minimo de lineas de los archivos de directorio.
minimo_lineas_archivo_directorio = 4



#--------------------------------------Definicion de funciones empleadas--------------------------------------


# Primer Funcion: Crea un archivo con el nombre especificado. Devuelve True si fue exitoso o False en caso de error.

def crear_archivo(nombre_archivo):
	try:
		archivo = open(nombre_archivo, 'w')
		archivo.close()
	except:
		guardar_error("Error creando archivo " + nombre_archivo + "!");
		return False
		
	return True

# Segunda Funcion: Lee las lineas de un archivo de texto y las devuelve en una lista.

def leer_lineas_archivo(nombre_archivo):
	lineas = ()
	try:
		archivo = open(nombre_archivo, 'r')
		lineas = archivo.readlines()
		archivo.close()
	except IOError:
		guardar_error("Error leyendo archivo " + nombre_archivo + "!")
		
	return lineas

# Tercer Funcion: Guarda un mensaje de error en el archivo error.txt.
def guardar_error(mensaje_error):
	escribir_linea_archivo(nombre_archivo_errores, "\n" + mensaje_error + "\n")

# Cuarta Funcion: Guarda un registro de operacion en el archivo log.txt.
def guardar_log(mensaje_registro):
	escribir_linea_archivo(nombre_archivo_registro, "\n" + mensaje_registro + "\n")

# Quinta Funcion: Guarda al final del archivo definido la linea especificada. Devuelve True si fue exitoso o False en caso de error.
def escribir_linea_archivo(nombre_archivo, linea_a_escribir):
	try:
		archivo = open(nombre_archivo, 'a')
		archivo.write(linea_a_escribir)
		archivo.close()
	except IOError:
		guardar_error("Error escribiendo linea " + linea_a_escribir + " en archivo " + nombre_archivo + "!")
		return False
		
	return True

# Sexta Funcion: Finaliza el programa y guarda el respectivo mensaje de terminacion en el archivo error.txt.
def terminar_programa(mensaje_terminacion):
	guardar_error(mensaje_terminacion)
	guardar_log("Programa terminado por error... Verificar archivo error.txt para mas detalles.")
	
	# Terminar el programa
	sys.exit()

# Septima Funcion: Valida archivo minimos.txt
def validar_archivo_minimos(nombre_archivo_minimos):
	archivo_minimos_valido = True

#  Octava Funcion : Valida linea nombre.
def validar_linea(linea_por_validar, numero_linea):	
	array_respuesta = [0 for x in range(3)]
	
	# Separar la linea por el simbolo (token) :
	arreglo_campos = linea_por_validar.split(":")
	
	# Validar la estructura de cada linea.
	# Validacion 4 (Va4)
	if (len(arreglo_campos) != 2):
		guardar_error("La linea " + str(numero_linea) + " no cumple con la estructura requerida! Revisarla!")
		array_respuesta[0] = False
		return array_respuesta
		
	nombre_por_validar = arreglo_campos[0]
	
	arreglo_nombre =  nombre_por_validar.split(" ")
	
	# Validar el numero de palabras del nombre
	# Validacion 5 (Va5)
	if (len(arreglo_nombre) < 2 or len(arreglo_nombre) > 5):
		guardar_error("El nombre " + arreglo_campos[0] + " no cumple con la longitud requerida! Revisar linea numero " + str(numero_linea) + " de archivo de nomina.")
		array_respuesta[0] = False
		return array_respuesta
	
	array_respuesta[1] = arreglo_nombre
	
	# Validar que el salario sea de tipo numerico
	# Validacion 6 (Va6)
	try:
		salario_base = int(arreglo_campos[1])								
		array_respuesta[2] = salario_base
	except ValueError:	
		guardar_error("El valor de salario " + arreglo_campos[1] + " no puede convertirse a entero! Revisar linea numero " + str(numero_linea) + " de archivo de nomina.")
		array_respuesta[0] = False
		return array_respuesta
		
	array_respuesta[0] = True
	return array_respuesta

# Novena.1 Funcion: validar archivos del arreglo_campos.
def validar_archivo2(nombre_archivo):
	archivo_valido = True
	# Validar que el nombre no contenga espacios.
	cantidad_palabras = len(nombre_archivo.split(" "))
	
	# Validar que no contenga espacios.	
	if(cantidad_palabras > 1):
		archivo_valido = False
		guardar_error("Nombre de archivo " + nombre_archivo + " tiene mas de una palabra.")
		print "El archivo "+ nombre_archivo +" no es valido"
	# Validar que la extension sea .txt
	if(not nombre_archivo.endswith(".txt")):
		archivo_valido = False
		guardar_error("Archivo "+nombre_archivo+" no tiene extension " + ".txt")
	return archivo_valido
# Novena Funcion: Valida  la existencia y nombre valido de archivo.
def validar_archivo(nombre_archivo):
	archivo_valido = True
	
	# Validacion -> El archivo.txt debe existir.
	if(os.path.isfile(nombre_archivo) == False):
		print "No existe archivo " + nombre_archivo
		guardar_error("Archivo " + nombre_archivo + " no existe.")
		
	# Validar que el nombre no contenga espacios.
	cantidad_palabras = len(nombre_archivo.split(" "))
	
	# Validar que no contenga espacios.	
	if(cantidad_palabras > 1):
		archivo_valido = False
		guardar_error("Nombre de archivo tiene mas de una palabra.")
	
	# Validar que la extension sea .txt
	if(not nombre_archivo.endswith(".txt")):
		archivo_valido = False
		guardar_error("Archivo no tiene extension  " + ".txt")
	return archivo_valido
'''
# Decima.2 funcion : Valida la existencia del directorio.
def validar_directorio(nombre_archivo):
	if os.path.exists(nombre_archivo):
		guardar_log("El directorio existe")
	else:
		guardar_error("El directorio no existe")
		print "El directorio no existe"

# Decima.3 funcion para validar directorio
def validar_directorio2(archivo):
	try:
		fichero = open(archivo)
		fichero.close()
		print "El fichero existe"
	except:
		print "El fichero no existe"
'''
# Decima.1 funcion: Valida la existencia del directorio.
def validar_directorio(directorio): 
	if os.path.isdir(directorio):
		guardar_log("El directorio existe")
	else: 
		guardar_error("El directorio no existe")
		terminar_programa("Error con el directorio")

# Validar linea y hacer arreglo
def validar_linea(linea_por_validar, numero_linea):	
	array_respuesta = [0 for x in range(2)]
	
	# Separar la linea por el simbolo (token) *
	arreglo_campos = linea_por_validar.split("*")	
	array_respuesta[0]=arreglo_campos[0]
	# Validar que el campo sea de tipo numerico
	try:
		minerales_base = int(arreglo_campos[1])								
		array_respuesta[1] = minerales_base
	except ValueError:	
		guardar_error(arreglo_campos[1] + " no puede convertirse a entero!")
		return array_respuesta
	return array_respuesta

# Treceaba funcion: Lee las lineas de un archivo de texto y las devuelve en una lista.
def leer_lineas_archivo(nombre_archivo):
	lineas = ()
	try:
		archivo = open(nombre_archivo, 'r')
		lineas = archivo.readlines()
		archivo.close()
	except IOError:
		guardar_error("Error leyendo archivo " + nombre_archivo + "!")
		
	return lineas 


# Catorceaba Funcion: Valida si una linea tiene la estructura key=value, siendo value de tipo numerico.
def validar_linea_key_value(linea_a_validar):
	linea_valida = True
	
	campos_linea = linea_a_validar.split("=")
	
	cantidad_campos_linea = len(campos_linea)
	
	if(cantidad_campos_linea != 2):
		linea_valida = False
		return linea_valida
	
	if( (not validar_tipo_numerico(campos_linea[1]) ) or (int(campos_linea[1]) < 0) ) :
		linea_valida = False
		return linea_valida

	return linea_valida
#-------------------------------------- Fin de definicion de funciones empleadas--------------------------------------

#--------------------------------------Iniciacion de archivos--------------------------------------

# Se crea el archivo informe.txt que contendra la informacion requeridad por el usuario.
crear_archivo("informe.txt")

# Se crea el archivo error.txt que contendra los errores que se generen en el programa.
crear_archivo("error.txt")

# Se crea el archivo log,txt que contendra el registro de operaciond el programa.
crear_archivo("log.txt")

guardar_log("Se crean los  archivos 'informe.txt','error.txt' y 'log.txt'")

#--------------------------------------Validaciones--------------------------------------

# Se sumistra el directorio.
directorio = "D:\Desktop\parcial_tecnicas\SSMEv0.0.1\planetas"

# Obtener numero de argumentos de linea de comandos
cantidad_argumentos = len(sys.argv)

# Validar que el numero de argumentos sea igual a 3.
# Validacion 1 (Va1)
if (cantidad_argumentos != 3):	
	terminar_programa("Numero de argumentos incorrecto. Debe sumistrar los archivos con: directorio,minimos y recursos.")

guardar_log("Numero de argumentos OK")

# Validar que los archivos minimo.txt y recursos.txt existan.
validar_archivo(nombre_archivo_minimos)
validar_archivo(nombre_archivo_recursos)

# Validar que exista el directorio.
validar_directorio(directorio)

# Obtenemos una lista con lo archivos dentro del directorio.
lista_planetas = os.listdir (r"D:\Desktop\parcial_tecnicas\SSMEv0.0.1\planetas")

# Obtenemos la cantidad de archivos que hay en el directorio.
c=0
for a in lista_planetas:
	c=c+1

# Validar archivos dentro el directorio.
for n in range(1,c):
	validar_archivo2(lista_planetas[n])

# almacenar el numero de lineas de los archivos del directorio.
lineas_maximas_archivo_directorio = len(open("D:\Desktop\parcial_tecnicas\SSMEv0.0.1\planetas\marte.txt").readlines())

# Validacion de lineas de archivo del directorio.
l=0
for n in range (0,c):
	linea=len(open("D:\Desktop\parcial_tecnicas\SSMEv0.0.1\planetas"+"\\"+lista_planetas[n]).readlines())
	if (linea<lineas_maximas_archivo_directorio):
		guardar_error("Las lineas del archivo "+lista_planetas[n]+" debe ser igual a los del resto.")
		l=l+1
	else:
		if (linea>lineas_maximas_archivo_directorio):
			guardar_error("Las lineas del archivo "+lista_planetas[n]+" debe ser igual a los del resto")
			l=l+1
if (l==0):
	print("Validacion de lineas de archivo exitosa")
	guardar_log("Se han validado satisfactoriamente las lineas de los archivos del directorio")
else:
	print("Validacion de lineas de archivos fallida")
	terminar_programa("Error en la validacion de lineas.")
'''
#prueba de paso para sacar resultado------------------------------------------------------------------------------
for n in range (0,c):
	prueba=open("D:\Desktop\parcial_tecnicas\SSMEv0.0.1\planetas"+"\\"+lista_planetas[n],"r")
	prueba2=prueba.read()
	print "\n"+prueba2+"\n"
'''
# Validacion de las lineas que contienen los minerales de cada planeta.
for n in range(0,c):
	prueba=open("D:\Desktop\parcial_tecnicas\SSMEv0.0.1\planetas"+"\\"+lista_planetas[n],"r")
	for i,linea in enumerate(prueba):
		if i>2 and i<8:
			validar_linea_key_value(linea)
			continue




























