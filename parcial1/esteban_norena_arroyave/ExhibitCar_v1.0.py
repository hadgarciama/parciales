# ExhibitCar v1.0
# El programa debe leer una serie de archivos que contiene la descripcion de diferentes modelos de carros, y 
# basado en otro archivo, seleccionar que modelos son suficientemente potentes para estar en una exhibicion,
# ademas de entregar un reporte donde liste todos los modelos analizados y el promedio y total de cada componente

# Desarrollado por Esteban Norena Arroyave
# Septiembre 13 de 2015

# Importar libreria os y os.path para el manejo de los directorios
import os
import os.path

# Importar libreria sys para manejo de argumentos en la linea de comandos
import sys

# Importar listdir desde os para listar los archivos que hay en un directorio
from os import listdir



# ------------------ Inicio de definicion de variables constantes ------------------ #

# Salidas

# Nombre archivo errores
nombre_archivo_errores = "errores.txt"

# Nombre archivo registro
nombre_archivo_registro = "log.txt"

# Nombre archivo de reporte
nombre_archivo_reporte = "reporte.txt"

# Nombre archivo para modelos potentes
nombre_archivo_potentes = "potentes.txt"

# Entradas

# Nombre archivo que tendra los elementos
nombre_archivo_elementos = "elementos.txt"

# Nombre archivo de exhibicion que tendra los minimos
nombre_archivo_exhibicion = "exhibicion.txt"

# ------------------ Fin de definicion de constantes y parametros ------------------ #

# ------------------ Inicio de definicion de funciones empleadas ------------------ #

# Funcion que crear un archivo con el nombre especificado. Devuelve True si fue exitoso o False en caso de error.
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
	escribir_linea_archivo(nombre_archivo_errores, mensaje_error + "\n")
	
# Funcion que guarda un registro de operacion en el archivo log.txt
def guardar_log(mensaje_registro):
	escribir_linea_archivo(nombre_archivo_registro, mensaje_registro + "\n")


# Funcion para validar la estructura de las lineas del archivo elementos 
# Recibe la linea a validar y el numero de linea correspondiente en el archivo
# Devuelve un array de dos posiciones, en la primera posicion devuelve una variable booleana que determina si es valida, y en la segunda
# devuelve el string de esa linea
def validar_linea_elementos(linea_a_validar, numero_de_linea):
	array_respuesta = [0 for x in range(2)]
	
	# Validar la estructura de cada linea, que cada linea contenga una cadena de texto (Va8)
	try:
		linea_validada = int(linea_a_validar)
		array_respuesta[0] = False
		guardar_error("La linea" + str(numero_de_linea) + "del archivo 'elementos.txt' no es una palabra valida")
		return array_respuesta
	
	# Si no fue capaz de convertirlo a entero, signfica que si se tiene una cadena de texto 
	except ValueError:
		array_respuesta[0] = True
		
		# Elimina el "\n" si contiene, esto para evitar problemas en el momento de escribir en los archivos.
		if linea_a_validar[len(linea_a_validar)-1] == "\n":
			array_respuesta[1] = linea_a_validar[0:len(linea_a_validar)-1]
		else:
			array_respuesta[1] = linea_a_validar
	return array_respuesta


# Funcion para la validar la estructura de las lineas de los archivos de exhibicion y de los archivos de los modelos
# Recibe la linea a validar, el numero de linea del correspondiente archivo y el nombre del archivo para especificar en cual
# hubo un error, si asi fue.
# Devuelve un array de tres posiciones, en la primera una variable booleana que determina si la linea es valida o no, en la segunda
# devuelve la cadena de texto correspondiente al elemento y en la tercera el valor numerico que corresponde al elemento anterior
def validar_lineas(linea_a_validar, numero_de_linea, nombre_archivo):
	array_respuesta = [0 for x in range(3)]
	
	# Se separa por el signo "="
	arreglo_campos = linea_a_validar.split("=")
	
	# Se valida si cumple la estructura 'palabra=numero' respecto a que debe quedar un arreglo de dos posiciones asegurando de 
	# no sea de tipo "algo=algo=algo..." o solo "algo" (Va8)
	if len(arreglo_campos) != 2:
		array_respuesta[0] = False
		guardar_error("La linea " + str(numero_de_linea) + " del archivo " + nombre_archivo + " no cumple con la estructura 'palabra=numero'")
		return array_respuesta
	
	# Se valida si la primera posicion es una cadena de texto, correspondiente al elemento (Va8)
	if isinstance(arreglo_campos[0],str):
		array_respuesta[1] = arreglo_campos[0]
	else:
		array_respuesta[0] = False
		guardar_error("En la linea " + str(numero_de_linea) + " del archivo " + nombre_archivo + " una palabra no antecede al '='")
		return array_respuesta
	
	# Se valida si la segunda posicion es un numero, y si es un numero, que sea positivo, correspondiente al valor para dicho elemento (Va8)
	try:
		arreglo_campos[1] = int(arreglo_campos[1])
		if arreglo_campos[1] < 0:
			array_respuesta[0] = False
			guardar_error("El valor de la linea " + str(numero_de_linea) + " del archivo " + nombre_archivo + " no puede ser negativo")
			return array_respuesta
		
		array_respuesta[2] = arreglo_campos[1]
	except ValueError:
		array_respuesta[0] = False
		guardar_error("En la linea " + str(numero_de_linea) + " del archivo " + nombre_archivo + " no hay un numero despues del '='")
		return array_respuesta
	
	array_respuesta[0] = True
	return array_respuesta


# Funcion especifica para validar las propiedades y las descripciones de cada archivo de modelo, que cumpla con la estructura estricta
# de precio=numero y velocidad=numero.
# Recibe el nombre del archivo del modelo a validar
# Devuelve un booleano que determina si las propiedades son validas o no
def validar_descripcion(nombre_archivo):
	# Se lee el archivo del modelo y se guarda sus lineas en la variable lineas_modelo
	lineas_modelo = tuple(leer_lineas_archivo(nombre_archivo))
	
	# Se separa la linea 1 que corresponde a la primera propiedad "precio=numero"
	arreglo_prop1 = lineas_modelo[0].split("=")
	
	# Se separa la linea 2 que corresponde a la segunda propiedad "velocidad=numero"
	arreglo_prop2 = lineas_modelo[1].split("=")
	
	# Se valida que ambas propiedades cumplan con la estructura algo=algo (Va8)
	if not(len(arreglo_prop1) == 2 and len(arreglo_prop2) == 2):
		guardar_error("Las propiedades del archivo " + nombre_archivo + " no cumplen la estructura 'palabra=numero'") 
		return False
	
	# Se valida que los primeros argumentos de los arreglos de las propiedades sean respectivamente "precio" y "velocidad", 
	# las mayusculas no seran relevantes. (Va8)
	if (arreglo_prop1[0].lower() == "precio" and arreglo_prop2[0].lower() == "velocidad") == False :
		guardar_error("Las propiedades del archivo " + str(nombre_archivo) + " no son validas, debe ser precio y velocidad")
		return False
	
	# Se valida que el valor del precio sea de tipo numerico (Va8)
	try:
		arreglo_prop1[1] = int(arreglo_prop1[1])
		if arreglo_prop1[1] <= 0:
			guardar_error("El valor para el precio del modelo debe ser positivo")
			return False
	except ValueError:
		guardar_error("No hay un valor valido para el precio del modelo del archivo " + str(nombre_archivo))
		return False
	
	# Se valida que el valor de la velocidad sea de tipo numerico (Va8)
	try:
		arreglo_prop2[1] = int(arreglo_prop2[1])
		if arreglo_prop2[1] <= 0:
			guardar_error("El valor para la velocidad del modelo debe ser positivo")
			return False
	except ValueError:
		guardar_error("No hay un valor valido para la velocidad del modelo" + str(nombre_archivo))
		return False
	return True

# Funcion que finaliza el programa y guarda el respectivo mensaje de terminacion en el archivo errores.txt
def terminar_programa(mensaje_terminacion):
	guardar_error(mensaje_terminacion)
	guardar_log("Programa terminado por error... Verificar archivo errores.txt para mas detalles.")
	
	# Terminar el programa
	sys.exit()
	

# ------------------ Fin de definicion de funciones empleadas ------------------ #

# Se crea el archivo errores.txt para almacenar los errores que se presenten
crear_archivo(nombre_archivo_errores)

# Se crea el archivo log.txt para almacenar el registro de lo que se va presentando en el programa
crear_archivo(nombre_archivo_registro)

guardar_log("Creados archivos log.txt y errores.txt")

# Validaciones

# Se obtiene la cantidad de argumentos en la linea de comandos
cantidad_argumentos = len(sys.argv)

# Se valida que haya almenos un argumento que corresponde al directorio (Va1)
if cantidad_argumentos != 2:
	terminar_programa("Numero de argumentos incorrecto. Debe suministrar un argumento con la direccion del directorio donde estan los modelos")

guardar_log("Numero de argumentos OK")

# Se almacena la direccion del directorio que corresponde al segundo argumento de la linea de comandos
direccion_directorio = sys.argv[1]

# Se valida que exista el archivo elementos.txt, en la misma direccion donde esta ExhibitCar (Va2)
if os.path.isfile(nombre_archivo_elementos) == False:
	terminar_programa("El archivo 'elementos' no existe, y si existe, no tiene la extension .txt valida")

guardar_log("Archivo 'elementos' si existe y su extension es correcta")

# Se valida que exista el archivo exhibicion.txt, en la misma direccion donde esta ExhibitCar (Va2) y (Va7)
if os.path.isfile(nombre_archivo_exhibicion) == False:
	terminar_programa("El archivo 'exhibicion' no existe, y si existe, no tiene la extension .txt valida")

guardar_log("Archivo 'exhibicion' si existe y su extension es correcta")

# Se valida que exista el directorio suministrado en la linea de comandos (Va2)
if os.path.exists(direccion_directorio) == False:
	terminar_programa("El directorio no existe, ingrese uno valido")

guardar_log("Directorio OK, existente")

# Se almacena la lista con los nombres de los archivos que hay en el directorio suministrado
lista_archivos_modelos = [f for f in listdir(direccion_directorio)]

# Se almacena la cantidad de archivos que hay en el directorio
numero_archivos_modelos = len(lista_archivos_modelos)

# Se valida que almenos haya un archivo en el directorio (Va3)
if len(lista_archivos_modelos) == 0:
	terminar_programa("Debe haber al menos un archivo en el directorio")

guardar_log("Al menos un archivo en el directorio OK")

# Se leen las lineas del archivo elementos y se almacenan en lineas_archivo_elementos
lineas_archivo_elementos = tuple(leer_lineas_archivo(nombre_archivo_elementos))

# Se almacena el numero de lineas que hay en este archivo, este valor es crucial para saber cuantos elementos se deben comparar.
numero_lineas_elementos = len(lineas_archivo_elementos)

# Se valida que almenos hayan 4 elementos para analizar (Va4)
if numero_lineas_elementos < 4:
	terminar_programa("Deben haber almenos 4 criterios en el archivo elementos")

guardar_log("Numero de criterios en elementos OK")
guardar_log("Archivo de elementos leido")

# Se leen las lineas del archivo exhibicion y se almacenan en la variable lineas_archivo_exhibicion
lineas_archivo_exhibicion = tuple(leer_lineas_archivo(nombre_archivo_exhibicion))

# Se almacena el numero de lineas de este archivo
numero_lineas_exhibicion = len(lineas_archivo_exhibicion)

# Se valida que en exhibicion hayan el mismo numero de elementos que en dicho archivo. (Va5)
if numero_lineas_exhibicion != numero_lineas_elementos :
	terminar_programa("El numero de criterios de elementos no coincide con el numero de criterios de exhibicion")


guardar_log("El numero de criterios en elementos y exhibicion OK")
guardar_log("Archivo de exhibicion leido")

'''
 Inicio de carga de toda la informacion en un arreglo

 Inicializacion del arreglo que contendra toda la informacion, el numero de columnas se da por la cantidad de archivos de modelo 
 + 2, ya que las dos primeras columnas tendra los nombres de los elementos y el valor de los minimos respectivamente. Mientras que 
 el numero de filas se da por la cantidad de elementos + 1, ya que la primera fila estara el nombre de los modelos, teniendo por
 ejemplo:
 
 [ 'Elementos'      'minimos'        'modelo1'       '....'       'modelo n' ]
 [ 'elemento1'      'minimo1'        'valor 11'      '....'       'valor 1n' ]
 [      .               .                .           '....'            .     ]
 [      .               .                .           '....'            .     ]
 [      .               .                .           '....'            .     ]
 ['elemento n'      'minimon'        'valor n1'      '....'       'valor nn' ]
 
'''

tabla_total = [[0 for columnas in range(numero_archivos_modelos+2)] for filas in range(numero_lineas_elementos+1)]

# Encabezado para elementos y para minimos
tabla_total[0][0] = "Elementos"
tabla_total[0][1] = "Minimos"

guardar_log("Cargando elementos y exhibicion en memoria")

# Inicio ciclo 1 -> x, en este ciclo se aniaden al arreglo tabla_total las 2 primeras columnas que corresponden a los elementos
# del archivo elementos y a los minimos del archivo exhibicion, asi como al mismo tiempo se va validando las lineas de cada 
# archivo.
for x in range(0,numero_lineas_elementos):
	guardar_log("	Procesando linea " + str(x+1) + " de elementos")
	
	# Se usa la funcion de validar_linea_elementos para validar la estructura de cada linea de este archivo. (Va8)
	linea_validada_elementos = validar_linea_elementos(lineas_archivo_elementos[x], x+1)
	
	if linea_validada_elementos[0] == False:
		terminar_programa("Error en archivo 'elementos.txt'")
	
	# Si se da la validacion, se aniade el elemento al arreglo
	tabla_total[x+1][0] = linea_validada_elementos[1]
	
	guardar_log("	Procesando linea " + str(x+1) + " de exhibicion")
	
	# Se valida la estructura de las lineas del archivo exhibicion con la funcion validar_lineas (Va8)
	linea_validada_exhibicion = validar_lineas(lineas_archivo_exhibicion[x], x+1, nombre_archivo_exhibicion)
	if linea_validada_exhibicion[0] == False:
		terminar_programa("Error en archivo 'exhibicion.txt'")
	
	# Se valida que el elemento de la misma linea de exhibicion.txt coincida con el elemento de la misma linea de elementos.txt
	# debido a que esto esta dentro de un ciclo, de esta manera se valida cada elemento de cada uno de los archivos. (Va9)
	if (linea_validada_exhibicion[1] == linea_validada_elementos[1]):
		tabla_total[x+1][1] = linea_validada_exhibicion[2]
	else:
		terminar_programa("El elemento de la linea " + str(x+1) + " del archivo 'elementos' no coincide con la linea " + str(x+1) + " del archivo 'exhibicion'")
 
 
guardar_log("Elementos y exhibicio cargados correctamente en memoria")

# Se crea el archivo correspondiente al reporte para ir aniadiendo los modelos analizados exitosamente
crear_archivo(nombre_archivo_reporte)

guardar_log("Creado archivo de reporte para aniadir listado de modelos analizados exitosamente")

# Se escribe el encabezado para el archivo de reporte
escribir_linea_archivo(nombre_archivo_reporte, "--------- LISTADO MODELOS ANALIZADOS EXITOSAMENTE ---------")
'''
 Se inicializa esta variable que regira la columna en la que se ira poniendo los valores de cada modelo, el 
 motivo por el cual no se usa la variable del ciclo correspondiente es que si en dado caso que un archivo del
 modelo no sea valido, se debe seguir analizando los otros archivos y no se debe terminar el programa, por lo
 tanto esta variable cambiara dependiendo si un modelo fue valido. Por ejemplo, si un modelo no lo es, el siguiente
 modelo debera sobreescribir lo que iba en la columna del modelo que no fue valido, esto para que al momento de 
 hacer los calculos y las comparaciones no hayan conflictos. (no fue inicializada en el comienzo del programa 
 debido a que hubiera sido mas dificl la explicacion del por que se necesita.
'''
columna_efectiva = 1

guardar_log("Cargando archivos de modelos en memoria...")


# Inicio ciclo 2 -> t, este ciclo permitira recorrer el arreglo donde esta la lista de los archivos, para despues, en un
# ciclo anidado, recorrer las del archivo que el ciclo 2 suministre dependiendo de su variable y.
for y in range(0,numero_archivos_modelos):
	# Se suma uno a columna_efectiva como motivo a que se empieza un nuevo ciclo.
	columna_efectiva = columna_efectiva + 1
	guardar_log("	Procesando y cargando archivo " + lista_archivos_modelos[y] + " en memoria")
	
	# Se leen las lineas  del archivo correspondiente a la variable "y" del ciclo, y se guarda en la variable 
	# lineas_archivo_modelo que va a cambiar para cada ciclo, ya que cada ciclo cambia el archivo.
	lineas_archivo_modelo = tuple(leer_lineas_archivo(direccion_directorio + "\\" + lista_archivos_modelos[y]))
	
	# Se valida que el archivo correspondiente al ciclo 2 tenga extension .txt (Va7)
	if not(lista_archivos_modelos[y].endswith(".txt")):
		# Cuando no se valida correctamente un archivo, se resta uno a columna_efectiva con motivo a que sobre esta columna_efectiva
		# se debe sobreescribir con el siguiente archivo, de esta manera, la columna quedara igual y se sobreescribira
		
		columna_efectiva = columna_efectiva - 1
		guardar_error("El archivo " + lista_archivos_modelos[y] + "no tiene extension valida")
		guardar_log("		Error analizando el archivo " + lista_archivos_modelos[y])
		
		# continue es una herramienta que hace que el ciclo en el que se ejecute, avance al siguiente ciclo sin considerar las demas
		# instrucciones que esten abajo de el.
		continue
	
	# Se valida que el nombre del archivo no haya ningun espacio
	if (' ' in lista_archivos_modelos[y]):
		columna_efectiva = columna_efectiva - 1
		guardar_error("El archivo " + lista_archivos_modelos[y] + " no tiene un nombre valido")
		guardar_log("		Error analizando el archivo" + lista_archivos_modelos[y])
		continue
	
	
	# En la variable modelo se guarda en una cadena de texto el nombre del modelo, sin tener en cuenta la parte de la extension
	arreglo_modelo = lista_archivos_modelos[y].split(".")
	modelo = arreglo_modelo[0]
	
	# Se valida que las propiedades del archivo correspondiente al ciclo 2 sean correctas (Va8)
	if validar_descripcion(direccion_directorio + "\\" + lista_archivos_modelos[y]) == False:
		columna_efectiva = columna_efectiva - 1
		guardar_error("La descripcion del modelo " + modelo + " tiene un error, este modelo no se analizara")
		guardar_log("		Error analizando el archivo del modelo " + modelo) 
		continue
	
	# Se asigna a la variable numero_lineas_modelo la longitud del arreglo que contiene la lineas del archivo del modelo correspondiente 
	numero_lineas_modelo = len(lineas_archivo_modelo)
	
	# Se valida que el numero de lineas del archivo modelo menos 2 sea igual al numero de linea de elemento, esto es para asegurar de que
	# ambos tengan la misma cantidad de elementos. (Va6)
	if numero_lineas_elementos != (numero_lineas_modelo - 2):
		columna_efectiva = columna_efectiva - 1
		guardar_error("El modelo " + modelo + " no cumple con la cantidad de elementos en 'elementos.txt' ")
		guardar_log("		Error analizando el archivo del modelo " + modelo) 
		continue
	
	# En la columna_efectiva pero en la fila 0, se asigna el nombre del modelo en cuestion que esta siendo analizado
	tabla_total[0][columna_efectiva] = modelo
	
	# Inicio Ciclo 3 anidado -> z, ciclo que permitira recorrer las lineas del archivo correspondiente al ciclo 2, y al mismo tiempo, si el archivo
	# es valido, se va aniadiendo los valores correspondiente a cada elemento de su respectivo modelo
	for z in range(0,numero_lineas_elementos):
		
		# Se va validando cada linea del archivo con la funcion validar_lineas. (Va8)
		linea_validada_modelo = validar_lineas(lineas_archivo_modelo[z+2], z+3, lista_archivos_modelos[y])
		if linea_validada_modelo[0] == False:
			columna_efectiva = columna_efectiva - 1
			guardar_error("Error en el archivo " + lista_archivos_modelos[y] + " este modelo no se analizara")
			guardar_log("		Error analizando el archivo del modelo " + modelo)
			# Si no se da la validacion, se ejecuta un break para que se salga del ciclo anidado, es decir despues de que 
			# no se cumpla una validacion, no se debe tener en cuenta ya este archivo y sobre la columna que iba este, se 
			# debe sobreescribir el siguiente archivo a validar.
			break
		
		# Se valida que el nombre del elemento del archivo, coincida en el mismo orden al nombre del elemento en 'elementos.txt'. (Va9)
		if linea_validada_modelo[1] == tabla_total[z+1][0]:
			
			# Si esta validacion se da, se almacen el valor correspondiente al elemento en la posicion que corresponde en la fila al 
			# elemento y en la columna al modelo en ejecucion
			tabla_total[z+1][columna_efectiva] = linea_validada_modelo[2]
			
			# Si se han analizado todas las lineas y no se ha encontrado ningun error, entonces es en la ultima linea en la que 
			# se sabe si el modelo esta correcto y fue analizado exitosamente.
			if z == numero_lineas_elementos - 1:
				# Al entrar en esta condicion, se aniade el archivo en ejecucion al listado en el archivo reporte.txt, ya que si entro a 
				# esta condicion, se esta seguro de que no hubo ningun error
				escribir_linea_archivo(nombre_archivo_reporte, "\n ------ \n %s \n %s \n %s ------" % (modelo, lineas_archivo_modelo[0][0:len(lineas_archivo_modelo[0])-1], lineas_archivo_modelo[1]))
				guardar_log("		Modelo " + modelo + " cargado satisfactoriamente")
		
		# Si los elementos no coinciden, tal como en todos los errores, se resta uno a columna_efectiva y se ejecuta el break para que continue
		# al siguiente archivo
		else:
			columna_efectiva = columna_efectiva - 1
			guardar_log("		Error analizando el archivo del modelo " + modelo) 
			guardar_error("El elemento " + linea_validada_modelo[1] + " del archivo " + lista_archivos_modelos[y] + " no coincide con ninguno de los elementos declarados en el archivo 'elementos.txt', este modelo no se analizara")
			break
# Fin ciclo 2 y ciclo 3


for n in range(0,numero_lineas_elementos+1):
	print tabla_total[n]

# Finalmente, en este momento del programa se tiene toda la informacion correcta en el arreglo tabla_total y se esta seguro que toda la informacion
# en este arreglo esta correcta y validada, asi pues, se puede recorrer este arreglo libremente para hacer las comparaciones y ejecutar los calculos

# Se calcula la cantidad de modelos_analizados, sabiendo que es las columnas efectivas restada 1, esto se calcula para hallar el promedio de
# cada elemento.
modelos_analizados = columna_efectiva - 1
guardar_log("Calculando cantidad de modelos analizados satisfactoriamente")

# Si resulta que si habian archivos en el directorio, pero ninguno de ellos fue valido, entonces no se puede efectuar ningun analisis, y de esta 
# manera se debe terminar el programa.
if modelos_analizados == 0:
	terminar_programa("GRAVE ERROR: Ningun modelo ha sido valido, por favor revise cada uno de ellos")

# ----- INICIO DE CALCULOS Y COMPARACIONES ------

# Creacion del archivo potentes.txt que contendra los modelos que satisfagan las condiciones de minimos
crear_archivo(nombre_archivo_potentes)
guardar_log("Creado archivo potentes.txt para empezar a aniadir los modelos que cumplan")

# Se escribe el encabezado para el archivo de potentes.txt
escribir_linea_archivo(nombre_archivo_potentes,"-------------------- MODELOS PARA EXHIBICION -------------------- \n \n")
guardar_log("Analizando cada modelo y comparando...")

# Inicio ciclo 4 -> p, en este ciclo, usado para hacer las comparaciones, se recorren las columnas ya que en cada columna se encuentra
# cada modelo, notese que empieza en 2, porque desde la columna 2 empiezan los modelos y recordemos que en las primeras dos columnas
# se encuentran los elementos y los minimos respectivamente
for p in range (2, columna_efectiva+1):
	
	guardar_log("	Comparando modelo %s..." % tabla_total[0][p])
	
	# Inicio ciclo anidado 5 -> n, en este ciclo se recorre cada valor correspondiente a cada elemento y cada modelo, esto con el fin
	# de comparar con el valor minimo que se encuentra en la columna 1.
	for n in range(1, numero_lineas_elementos+1):
		
		# Se compara el valor correspondiente al modelo en la fila n y la columna p con el valor minimo que se encuentra en la fila n
		# y la columna n, notese que como se esta dentro de un ciclo, se va analizando cada elemento, si se da la condicion, entonces
		# en la variable potente habra un booleano que determinara esto. 
		if tabla_total[n][p] >= tabla_total[n][1]:
			potente = True
			
		else:
			# En el momento en que una condicion no se de, es inoficioso seguir comparando el resto de elementos, debido a esto, se ejecuta el
			# break al final y se asigna False a la variable, potente para que este modelo no se aniada al archivo potentes.txt
			potente = False
			guardar_log("		Modelo %s no cumple en %s" % (tabla_total[0][p], tabla_total[n][0]))
			break
	
	# Fin del ciclo anidado 5
	
	# Fuera del ciclo 5, se compara el booleano que tiene potente, si es True, entonces ese modelo se aniade a potentes.txt
	if  potente:
		escribir_linea_archivo(nombre_archivo_potentes, "El modelo %s, cumple para estar en exhibicion \n" % (tabla_total[0][p]))
		guardar_log("		Modelo %s cumple y es cargado satisfactoriamente en potentes"% (tabla_total[0][p]))

# Fin ciclo 4

# Se escribe el encabzado de los TOTALES Y PROMEDIOS para reporte.txt
escribir_linea_archivo(nombre_archivo_reporte, "\n------------------- TOTALES Y PROMEDIOS --------------------- \n\n")

guardar_log("Calulando promedios y totales...")

# Ciclo 6 -> l, que recorrera las filas de cada elemento y acumulura cada valor respectivo a cada fila. En el ciclo 4 y 5 no se pudo
# calcular los totales y promedios ya que en el momento en que tenga que haber un break, entonces quedarian faltando valores por sumar,
# por este motivo se implementa otros 2 ciclos.
for l in range(1, numero_lineas_elementos+1):
	
	# Variable que contiene la suma de cada elemento, esta variable va ser 0 cada vez que se cambie de fila ya que en cada fila 
	# hay un elemento diferente al cual se le debe hallar el acumulado total
	suma = 0
	
	# Inicio Ciclo 7 anidado -> b, que recorrera cada valor de cada elemento y permitira ir sumando cada uno de ellos
	for b in range(2, columna_efectiva+1):
		
		# Se acumula el valor de cada elemento en la variable suma y se le va sumando el valor que hay en tabla_total en la fila l
		# y la columna b, que corresponde a cada valor del elemento.
		suma = suma + tabla_total[l][b]
	
	# Fin ciclo 7
	
	# Al final del ciclo 7, se tiene en la variable suma el valor total del acumulado del elemento que suministra el ciclo 6, por lo tanto
	# en este momento se escribe en reporte.txt el total y en la misma linea se halla el promedio que seria la suma total dividida entre
	# modelos_analizados
	escribir_linea_archivo(nombre_archivo_reporte, " Total para %s = %.2f \n Promedio para %s = %.2f \n\n" % (tabla_total[l][0], suma, tabla_total[l][0], (float(suma)/float(modelos_analizados))))
	guardar_log("	Calculado promedio y totales de %s" % tabla_total[l][0])

# Fin ciclo 6. en este punto se puede estar seguro de que el programa se ejecuto correcta y exitosamente y que se pudieron analizar al menos
# un modelo.
guardar_log("Fin del programa, terminado exitosamente, revisar archivos de salida.")

#Fin del programa