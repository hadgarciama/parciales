# RobotCare V1.0
# Programa que analiza si en una comunidad se puede brindar ayuda robotica para el cuidado y apoyo de diferentes 
# poblaciones mediante una base de datos dada por un directorio donde se encuentran todos los documentos de apoyo
# Luego de analizar los datos guarda cuales comunidades se vieron beneficiadas con el programa de apoyo que guarda
# en un archivo robots.txt, tambien guarda los totales y promedios de las poblaciones y los barrios analizados en analisis.txt y 
# el registro de errores en errores.txt y el registro de operacion en log.txt.

# Desarrollado por Jacobo Posada Hoyos
# Septiembre 17 de 2015

# Importar libreria sys para manejo de argumentos de linea de comandos
import sys
# Importar libreria os para acceder a funcionalidades dependientes del Sistema Operativo
import os

import os.path

from os import listdir 

# ------------------ Inicio de definicion de constantes y parametros ------------------ #

# Nombre archivo de errores
nombre_archivo_errores = "errores.txt"

# Nombre archivo de registro de operacion del programa
nombre_archivo_registro = "log.txt"

# Nombre archivo que contiene los minimos de poblacion
nombre_archivo_minimos = "minimos.txt"

# Nombre archivo que contiene las poblaciones
nombre_archivo_cuidado = "cuidado.txt"

# Numero minimo de lineas
numero_minimo_lineas = 4

# Extension por defecto
extension_por_defecto = ".txt"


# ------------------ Fin de definicion de constantes y parametros ------------------ #

# ------------------ Inicio de definicion de funciones empleadas ------------------ #

#Funcion que crea un archivo dado su nombre
def crear_archivo(nombre_archivo):
	try:
		archivo = open(nombre_archivo, 'w')
		archivo.close()
	except:
		guardar_error("Error creando archivo " + nombre_archivo + "!");
		return False
		
	return True


# Funcion que lee las lineas de un archivo de texto y las devuelve en una lista.
def leer_lineas_archivo(nombre_archivo):
	lineas = ()
	try:
		archivo = open(nombre_archivo, 'r')
		lineas = archivo.readlines()
		archivo.close()
	except IOError:
		guardar_error("Error leyendo archivo " + nombre_archivo + "!")
		
	return lineas 


# Funcion que guarda al final del archivo definido la linea especificada. Devuelve True si fue exitoso o False en caso de error.
def escribir_linea_archivo(nombre_archivo, linea_a_escribir):	
	try:
		archivo = open(nombre_archivo, 'a')
		archivo.write(linea_a_escribir)
		archivo.close()
	except IOError:
		guardar_error("Error escribiendo linea " + linea_a_escribir + " en archivo " + nombre_archivo + "!")
		return False
		
	return True

# Funcion que guarda un mensaje de error en el archivo errores.txt
def guardar_error(mensaje_error):
	escribir_linea_archivo(nombre_archivo_errores, "\n" + mensaje_error + "\n")

# Funcion que guarda un registro de operacion en el archivo log.txt
def guardar_log(mensaje_registro):
	escribir_linea_archivo(nombre_archivo_registro, "\n" + mensaje_registro + "\n")

# Funcion que finaliza el programa y guarda el respectivo mensaje de terminacion en el archivo errores.txt
def terminar_programa(mensaje_terminacion):
	guardar_error(mensaje_terminacion)
	guardar_log("Programa terminado por error... Verificar archivo errores.txt para mas detalles.")
	
	# Terminar el programa
	sys.exit()

# Funcion que valida si un archivo determinado es correcto
def validar_archivo(nombre_archivo):
	archivo_valido = True
	
	# El archivo.txt debe existir.
	if(os.path.isfile(nombre_archivo) == False):
		guardar_error("Archivo suministrado no existe.")			

	# Validar que el nombre no contenga espacios.
	cantidad_palabras = len(nombre_archivo.split(" "))
	
	# Validar que no contenga espacios.	
	if(cantidad_palabras > 1):
		archivo_valido = False
		guardar_error("Nombre de archivo tiene mas de una palabra.")
	
	# Validar que la extension sea .txt
	if(not nombre_archivo.endswith(extension_por_defecto)):
		archivo_valido = False
		guardar_error("Archivo no tiene extension  " + extension_por_defecto)
	
	return archivo_valido

# Funcion que valida el archivo cuidado 
def validar_cuidado(linea_por_validar, numero_de_linea):
	array_respuesta = [0 for x in range(2)]
	cuidado = linea_por_validar
	if isinstance(cuidado, str) == False:
		guardar_error("El tipo de poblacion de la linea "+str(numero_de_linea)+" no es valido")
		array_respuesta[0] = False
		return array_respuesta
	if cuidado[len(cuidado)-1] == "\n":
		array_respuesta[1] = cuidado[0:len(cuidado)-1]
	else:
		array_respuesta[1] = cuidado
	array_respuesta[0] = True 
	return array_respuesta

# Funcion que valida la estructura key=value para los archivos de minimos y barrios.
def validar_linea_minimos_barrios (linea_por_validar, numero_de_linea):
	array_respuesta = [0 for x in range(3)]

	# Separar la linea por el simbolo (token) =
	arreglo_minimos= linea_por_validar.split("=")
	
	if len(arreglo_minimos) != 2 :
		array_respuesta[0] = False
		guardar_error("La linea no cumple la estructura")
		return array_respuesta
	try:
		tipo_poblacion_comuna_estrato= int(arreglo_minimos[0])
		guardar_error("La linea " + str(numero_de_linea) + " en el archivo "+nombre_barrio+" no cumple con la estructura requerida")
		array_respuesta[0]= False
		return array_respuesta
	except ValueError:
		array_respuesta[0]= True
		array_respuesta[1]=arreglo_minimos[0]


	try:
		numero_poblacion_comuna_estrato= int(arreglo_minimos[1])
		if arreglo_minimos[1] <0 :
			array_respuesta[0] = False
			guardar_error("El valor debe ser positivo")
			return array_respuesta
		array_respuesta[2]=numero_poblacion_comuna_estrato
		array_respuesta[0] = True
	except ValueError:
			guardar_error("La linea " +str(numero_de_linea) + " en el archivo "+nombre_barrio+" no cumple con la estructura requerida")
			array_respuesta[0]= False
			return array_respuesta

	return array_respuesta

# Funcion que valida que la informacion de estrato y comuna sea correcta
def validar_estrato_comuna(nombre_archivo):
	lineas_archivo_barrios = leer_lineas_archivo(nombre_archivo)
	array_estrato = lineas_archivo_barrios[0].split("=")
	array_comuna = lineas_archivo_barrios[1].split("=")
	if len(array_estrato) != 2 or len(array_comuna) != 2 :
		guardar_error("La estructura de la descripcion del archivo "+nombre_archivo+" es invalida")
		return False 
	
	if not (array_estrato[0].lower() == "estrato" and array_comuna[0].lower() == "comuna"):
		guardar_error("Los criterios no coinciden con las estructura requerida")
		return False
	
	try:
		array_estrato[1] = int(array_estrato[1])
		if array_estrato[1]<=0:
			guardar_error("El valor para el estrato debe ser positivo")
			return False
	except ValueError:
		guardar_error("Para el estrato no hay un valor valido")
		return False
	
	try:
		array_comuna[1] = int(array_comuna[1])
		if array_comuna[1]<=0:
			guardar_error("El valor para la comuna debe ser positivo y valido")
	except ValueError:
		guardar_error("Para la comuna no hay un valor valido")
		return False
	return True

# ------------------ Fin de definicion de funciones empleadas ------------------ #

#----------------------------Inicializacion de archivos----------------------------#

# Crear el archivo errores.txt para almacenar los errores que se presenten.
crear_archivo("errores.txt")

# Crear el archivo log.txt para almacenar el registro de operacion del programa.
crear_archivo("log.txt")

guardar_log("Creados archivos errores.txt y log.txt")

#---------------------------------Validaciones----------------------------------#

# Obtener numero de argumentos de linea de comandos
cantidad_argumentos = len(sys.argv)

# Validar que el numero de argumentos sea igual a 2, garantizando que se haya el nombre del archivo de nomina.
# Validacion 1 (Va1)
if (cantidad_argumentos != 2):	
	terminar_programa("Numero de argumentos incorrecto. Debe suministrar un argumento con la direccion del fichero de los barrios")

guardar_log("Numero de argumentos OK")

# Validar la existencia del directorio y de los archivos
# Validacion 2 (Va2)

# Para el directorio
directorio_barrios = sys.argv[1]
arreglo_directorio = directorio_barrios.split(" ")
if len(arreglo_directorio)>1:
	terminar_programa("La ruta del directorio contiene un espacio")
if  os.path.exists(directorio_barrios) == False:
	terminar_programa("El directorio valido OK")

guardar_log("Existencia del directorio OK")

# Para el archivo minimos
archivo_valido = validar_archivo(nombre_archivo_minimos)
if archivo_valido == False:
	terminar_programa("El archivo minimos no cumple con los requerimientos.")
guardar_log("Extension, existencia y nombre del archivo minimos OK")


# Para el archivo cuidado
archivo_valido = validar_archivo(nombre_archivo_cuidado)
if archivo_valido == False:
	terminar_programa("El archivo de cuidado no cumple con los requerimientos.")
guardar_log("Extension, existencia y nombre del archivo cuidado OK")

# Validar que el directorio contenga minimo un archivo
# Validacion 3 (Va3)

array_directorio = os.listdir(sys.argv[1])
cantidad_archivos_directorio = len(array_directorio)
if cantidad_archivos_directorio == 0 :
	terminar_programa("Numero de archivos del directorio incorrecto")

guardar_log("Numero de archivos del directorio OK")

# Validar que el numero de poblaciones sean minimo 4 
# Validacion 4 (Va4)

numero_lineas_cuidado = len(tuple(leer_lineas_archivo(nombre_archivo_cuidado)))
if numero_lineas_cuidado < 4 :
	terminar_programa("El numero de poblaciones es erroneo")

guardar_log("Numero de poblaciones OK")

# Variable que almacena el contenido de las lineas del archivo de cuidado.
lineas_archivo_cuidado = tuple(leer_lineas_archivo(nombre_archivo_cuidado))

# Variable que almacena el contenido de las lineas del archivo de minimos.
lineas_archivo_minimos = tuple(leer_lineas_archivo(nombre_archivo_minimos))

# Variable que almacena el numero de lineas del archivo de minimos
numero_lineas_minimos = len(lineas_archivo_minimos)

# Validar que el numero de lineas y el orden de los archivos cuidado y minimos sea el mismo.
# Validacion 5 (Va5)

if numero_lineas_cuidado != numero_lineas_minimos :
	terminar_programa("El numero de lineas de los archivos minimos y cuidado no es el mismo")
	

# ------------------------ Inicio de logica de programa --------------------- #

# Se inicializa array_minimos, el cual contendra la informacion del archivo minimos.
array_minimos = [0 for t in range(numero_lineas_minimos)]

# Se inicializa array_cuidado, el cual contendra la informacion del archivo cuidado.
array_cuidado = [0 for s in range(numero_lineas_cuidado)]

# Ciclo que almacena el tipo y el minimo de poblacion cada uno en un array. 
# Inicio del ciclo 1 

# Validacion 5 (Va5)

for w in range(0, numero_lineas_cuidado):
	linea_validada1 = validar_cuidado(lineas_archivo_cuidado[w], w+1)
	linea_validada2 = validar_linea_minimos_barrios(lineas_archivo_minimos[w], w+1)

	if linea_validada1[1] != linea_validada2[1]:
		terminar_programa("El tipo de poblacion de la linea "+str(w+1)+" no coincide")
	
	if(linea_validada1[0] == False):
		terminar_programa("Error en archivo cuidado")
	
	# Se almacena el tipo de poblacion
	array_cuidado[w] = linea_validada1[1]
	
	if(linea_validada2[0] == False):
		terminar_programa("Error en archivo minimos")

	#Se almacena el valor minimo de poblacion
	array_minimos[w] = linea_validada2[2]

guardar_log("Datos de archivos minimos y cuidado guardados en array_minimos y array_cuidado respectivamente")

# Fin del ciclo 1 

# Se crean los archivos .txt donde se guardaran los barrios que cumplen con los requerimientos.

# Se crea archivo robots.txt
crear_archivo("robots.txt")
escribir_linea_archivo("robots.txt", "*******BARRIOS A LOS CUALES SE LES PRESTARA LA AYUDA ROBOTICA*******\n\n")
guardar_log("Se crea archivo robots.txt")

# Se crea archivo analisis.txt
crear_archivo("analisis.txt")
escribir_linea_archivo("analisis.txt", "*******BARRIOS ANALIZADOS*******\n\n")
guardar_log("Se crea archivo analisis.txt")

# Se inicializa el array_acumuladores para almacenar el valor de cada tipo de poblacion.
array_acumuladores = [0 for u in range(numero_lineas_cuidado)]
contador = 0


# Ciclo que recorre cada archivo del directorio y si el archivo es valido lo almacena en los archivos
# que cumplen los requerimientos

# Inicio del ciclo 2

for x in range (0, cantidad_archivos_directorio):
	archivo_a_validar = array_directorio[x]
	nombre_barrio = array_directorio[x].split(".")[0]
	lineas_archivo_barrios = tuple(leer_lineas_archivo(directorio_barrios +"\\"+archivo_a_validar))
	linea_validada = validar_estrato_comuna(directorio_barrios +"\\"+array_directorio[x])
	# Valida cada archivo del directorio.
	if validar_archivo(directorio_barrios +"\\"+array_directorio[x]) == False:
		guardar_error("Error al validar el archivo  "+nombre_barrio+" ")
		continue 
	guardar_log("El nombre del archivo "+nombre_barrio+" es valido")
	# Aqui se valida que la informacion de cada barrio sea correcta.
	if linea_validada == False:
		guardar_error("El archivo "+nombre_barrio+ " no cumple con los requerimientos")
		continue
	# Valida que la cantidad de poblaciones en cada archivo sea la misma que en el archivo cuidado.
	if (not len(lineas_archivo_barrios)-2 == len(lineas_archivo_cuidado)):
		guardar_error("El numero de lineas del archivo "+nombre_barrio+" no corresponde a la estructura")
		continue 
	# Variable booleana analisis que indica si el archivo es valido y se puede analizar.
	analisis = True
	# Se inicializa array_posible que sirve de apoyo para almacenar el valor de cada tipo de poblacion.
	array_posible = [0 for v in range(numero_lineas_cuidado)]
	for y in range (2, len(lineas_archivo_barrios)):
		linea_a_validar = validar_linea_minimos_barrios(lineas_archivo_barrios[y], y+1)
		# Se valida que la linea tenga la estructura key=value
		if linea_a_validar[0] == False:
			# Si hay un error se vuelve a inicializar el array ya que estos datos no los debe guardar.
			array_posible = [0 for v in range(numero_lineas_cuidado)]
			#guardar_error("La estructura de la linea "+str(y+1)+" en el archivo "+nombre_barrio+" es incorrecta")
			analisis = False
			break
		# Valida que el tipo de poblacion sea el correcto.
		if array_cuidado[y-2] != linea_a_validar[1]:
			array_posible = [0 for v in range(numero_lineas_cuidado)]
			guardar_error("El tipo de poblacion "+array_cuidado[y-2]+" en el archivo "+nombre_barrio+" es incorrecto ")
			analisis = False
			break
		guardar_log("El tipo de poblacion "+array_cuidado[y-2]+" en el archivo "+nombre_barrio+" es correcto ")
		array_posible[y-2] = linea_a_validar[2]
		# Aqui se puede saber que todo fue analizado y se procede a escribir en el archivo analisis.txt
		if y == len(lineas_archivo_barrios)-1:
			escribir_linea_archivo("analisis.txt", "*********\n%s\n%s%s\n" %(nombre_barrio, lineas_archivo_barrios[0], lineas_archivo_barrios[1]))
			contador = contador + 1
		# Se valida que el tipo de poblacion cumpla con el valor minimo.
		if linea_a_validar[2] < array_minimos[y-2]:
			guardar_log("El numero de poblacion "+array_cuidado[y-2]+" del archivo "+nombre_barrio+" no cumple con el valor minimo.")
			analisis = False
			continue
		guardar_log("El numero de poblacion "+array_cuidado[y-2]+" del archivo "+nombre_barrio+" cumple con el valor minimo, se puede brindar la ayuda")
	# Se suman los array_acumuladores y array_posible.
	array_acumuladores = [a + b for a, b in zip(array_acumuladores, array_posible)]
	# Si todos las validaciones fueron exitosas se procede a guardar el barrio en el archivo robots.txt
	if analisis == True: 
		escribir_linea_archivo("robots.txt", "El barrio "+ nombre_barrio +" cumple con los requerimientos, se le puede brindar la ayuda\n" )
		
# Fin del ciclo 2

# Se valida que al menos se haya analizado un barrio para que no se produzca un error matematico. 
if contador == 0:
	terminar_programa("Ningun archivo del directorio fue valido, por tanto no hay archivos para analizar.")

# Ciclo que guarda en el archivo analisis los totales y promedios.

# Inicio del ciclo 3

escribir_linea_archivo("analisis.txt", "\n *******TOTALES Y PROMEDIOS*******\n\n")
for z in range(0, len(array_acumuladores)):
	escribir_linea_archivo("analisis.txt", "Total para %s = %.2f \nPromedio para %s = %.2f\n\n" %(array_cuidado[z], array_acumuladores[z], array_cuidado[z], float(array_acumuladores[z])/float(contador)))

# Fin del ciclo 3
guardar_log("Fin del programa")

print ''' ______     ______     ______     ______     ______   ______     ______     ______     ______    
/\  == \   /\  __ \   /\  == \   /\  __ \   /\__  _\ /\  ___\   /\  __ \   /\  == \   /\  ___\   
\ \  __<   \ \ \/\ \  \ \  __<   \ \ \/\ \  \/_/\ \/ \ \ \____  \ \  __ \  \ \  __<   \ \  __\   
 \ \_\ \_\  \ \_____\  \ \_____\  \ \_____\    \ \_\  \ \_____\  \ \_\ \_\  \ \_\ \_\  \ \_____\ 
  \/_/ /_/   \/_____/   \/_____/   \/_____/     \/_/   \/_____/   \/_/\/_/   \/_/ /_/   \/_____/ 
                                                                                                 
                                                                                                 
'''
# Fin del programa

