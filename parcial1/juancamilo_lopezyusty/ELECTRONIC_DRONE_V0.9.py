# Electrodomestic Drone V-0.9.9
# Desarrollado por Juan Camilo Lopez Yusty
# Septiembre 17 de 2015
'''
Software para la obtencion y procesamiento de datos para el sector electrico,
con este software se facilitaran los calculos de cargas en un edificio, ademas
si hay o no exceso de cargas.
'''
import sys
import os.path
import time

#Definimos parametros constantes.
minimo_archivos_en_directorio = 4
# Extension por defecto
extension_por_defecto = ".txt"
# Nombre archivo de errores
nombre_archivo_errores = "errores" + extension_por_defecto
# Nombre archivo de registro de operacion del programa
nombre_archivo_registro = "log" + extension_por_defecto
# Nombre por defecto archivo de electrodomesticos
nombre_defecto_archivo_electrodomesticos = "electrodomesticos" + extension_por_defecto
nombre_archivo_electrodomesticos = "electrodomesticos"
# Nombre por defecto archivo de maximos
nombre_defecto_archivo_maximos = "maximos" + extension_por_defecto
#Hora. Para saber a que hora ocurrio el error.
hora_error = time.strftime("%c")

def crear_archivo(nombre_archivo):
	try:
		archivo = open(nombre_archivo, 'w')
		archivo.close()
	except:
		guardar_error("Error creando archivo " + nombre_archivo + "!" + "	Hora del error: " + hora_error);
		return False
		
	return True

crear_archivo(nombre_archivo_errores)
crear_archivo(nombre_archivo_registro)



def guardar_log(mensaje_registro):
	escribir_linea_archivo(nombre_archivo_registro, "\n" + mensaje_registro + "\n")

	# Funcion que guarda al final del archivo definido la linea especificada. Devuelve True si fue exitoso o False en caso de error.

def escribir_linea_archivo(nombre_archivo, linea_a_escribir):	
	try:
		archivo = open(nombre_archivo, 'a')
		archivo.write(linea_a_escribir)
		archivo.close()
	except IOError:
		guardar_error("Error escribiendo linea " + linea_a_escribir + " en archivo " + nombre_archivo + "!" + "	Hora del error: " + hora_error)
		return False
		
	return True

# Funcion que guarda un mensaje de error en el archivo errores.txt
def guardar_error(mensaje_error):
	escribir_linea_archivo(nombre_archivo_errores, mensaje_error + "\n")

def terminar_programa(mensaje_terminacion):
	guardar_error(mensaje_terminacion)
	guardar_log("Programa terminado por error.	 Verificar archivo errores.txt para mas detalles. 	Hora del error: " + hora_error)
	# Terminar el programa
	sys.exit()

def validar_archivo(nombre_archivo):
	archivo_valido = True
	
	# Validacion 10 -> El archivo.txt debe existir.
	if(not os.path.isfile(nombre_archivo)):
		print ("No existe archivo " + nombre_archivo)
		archivo_valido = False		
		guardar_error("Archivo " + nombre_archivo +" no existe."+ "	Hora del error: " + hora_error)	
		return archivo_valido

	# Validar que el nombre no contenga espacios.
	cantidad_palabras = len(nombre_archivo.split(" "))
	
	# Validar que no contenga espacios.	
	if(cantidad_palabras > 1):
		archivo_valido = False
		guardar_error("Nombre de archivo tiene mas de una palabra."+ "	Hora del error: " + hora_error)
		return archivo_valido
	
	# Validar que la extension sea .txt
	if(not nombre_archivo.endswith(extension_por_defecto)):
		archivo_valido = False
		guardar_error("Archivo no tiene extension  " + extension_por_defecto)
		return archivo_valido
	
	return archivo_valido	
	
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
guardar_log("Creados archivos " + nombre_archivo_errores + " y " + nombre_archivo_registro)
def existencia_archivo(archivo):
	try:
		fichero = open(archivo)
		fichero.close()
		print "El fichero existe"
	except:
		print ("El fichero no existe o no tiene extension *"+extension_por_defecto)
		guardar_error("Error, no existe archivo "+archivo+" o no tiene extension *"+ extension_por_defecto + "! 	 Hora error: " + hora_error)


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




def validar_archivo_maximos(nombre_archivo_maximos):
	archivo_maximos_valido = True
	# Validar la existencia del archivo y su nombre valido
	if(not validar_archivo(nombre_archivo_maximos)):
		archivo_maximos_valido = False
		return archivo_maximos_valido
	# Validar el contenido del archivo de maximos, solo debe contener lineas de la estructura 
	# key=value
	# Variable que almacena las lineas del archivo de maximos, su contenido como tal.
	lineas_archivo_maximos = tuple(leer_lineas_archivo(nombre_archivo_maximos))
	# Variable que almacena el numero de lineas del archivo de maximos
	numero_lineas_maximos = len(lineas_archivo_maximos)
	# Variable que almacena el numero de lineas validas del archivo de maximos
	cantidad_lineas_buenas = 0
	for x in range(0, numero_lineas_maximos):
		print "Linea " + str(x) + ": " + lineas_archivo_maximos[x]
		if(validar_linea_key_value(lineas_archivo_maximos[x])):
			cantidad_lineas_buenas += 1
			print "Linea " + str(x) + ": Valida!"
		else:
			guardar_error("Linea " + str(x) + ": Invalida!")
	if(cantidad_lineas_buenas < numero_lineas_maximos):
		guardar_error("No todas las lineas del archivo " + nombre_archivo_maximos + " son validas! Revisar " + nombre_archivo_errores + "!")
		archivo_maximos_valido = False
		return archivo_maximos_valido
	return archivo_maximos_valido

def validar_tipo_numerico(valor_string):	
	try:
		numerico = int(valor_string)
		return True		
	except ValueError:	
		guardar_error("Valor" + valor_string + " no puede convertirse a tipo numerico!")		
		return False


def hacer_prueba(nombre_archivo):
	resultado_validacion = validar_archivo(nombre_archivo)
	if(resultado_validacion):
		print "El archivo " + nombre_archivo + " es valido!"
	else:	
		print "El archivo " + nombre_archivo + " no es valido. Revisar " + nombre_archivo_errores


	return resultado_validacion

def test_max(name):
	if(hacer_prueba(name)):
		if(validar_archivo_maximos(name)):
			print "Archivo " + name + " COMPLETAMENTE VALIDO!"

		else:
			print "Archivo " + name + " INVALIDO!"

def leer_maximos(nombre_archivo_maximos):
	maximos = ()
	lineas_archivo_maximos = leer_lineas_archivo(nombre_archivo_maximos)
	
	for x in range(0, len(lineas_archivo_maximos)):
		campos_linea_maximos = lineas_archivo_maximos[x].split("=")
		try:
			maximos + (int(campos_linea_maximos[1]),)
		except ValueError:
			guardar_error("Error leyendo linea " + str(x) + " del archivo maximos.")
	
	return maximos

def validar_archivo_dispositivo(nombre_archivo_dispositivo):
	#Por definicion siempre es valido, pues si existe
	return True


#test_max(nombre_defecto_archivo_maximos)
#existencia_archivo(nombre_defecto_archivo_electrodomesticos)

cantidad_argumentos = len(sys.argv)

# Validar que el numero de argumentos sea igual a 4, garantizando que se haya el nombre del directorio, archivo de maximos y archivo de componentes
if (cantidad_argumentos != 4):	
	terminar_programa("Numero de argumentos incorrecto. Debe suministrar un argumento con el nombre del directorio, archivo de maximos y archivo de componentes. 	Hora del error: "+ hora_error)

guardar_log("Numero de argumentos OK")

directorio_a_revisar = sys.argv[1]
nombre_archivo_maximos = sys.argv[2]
nombre_archivo_electro = sys.argv[3]

maximos = ()

if(validar_archivo_maximos(nombre_archivo_maximos)):
	guardar_log("Archivo " + nombre_archivo_maximos + " COMPLETAMENTE VALIDO!")
	maximos = leer_maximos(nombre_archivo_maximos)
	
	for x in range(0, len(maximos)):
		print "Detectado maximo: " + str(x)
		
else:
	terminar_programa("Archivo " + nombre_archivo_maximos + " INVALIDO!")
	
print "Leyendo " + directorio_a_revisar + "..."

if (os.path.exists(directorio_a_revisar)):
	print "Directorio " + directorio_a_revisar + " VALIDO!" 	
	cantidad_archivos_directorio = len([name for name in os.listdir(directorio_a_revisar)])
	
	print "Cantidad de archivos = " + str(cantidad_archivos_directorio)
	
	if(cantidad_archivos_directorio >= 1):
			
		archivos_directorio = os.listdir(directorio_a_revisar)
		
		# Se tienen 6 filas en cada archivo, por ende se tendran 6 columnas en el array de dispositivos. Adicionalmente, 
		# se coloca como primera columna el nombre del archivo, por eso son en total 7 columnas.
		dispositivos = [[fila_archivo for fila_archivo in range(7)] for archivos in range(cantidad_archivos_directorio)]
		
		print "Directorio contiene cantidad minima de archivos!"
		contador_archivos_validos = 0
		
		for nombre_archivo in archivos_directorio:
			print "Leyendo archivo " + nombre_archivo + "..."
			nombre_completo_archivo = directorio_a_revisar+"\\"+nombre_archivo
			print "Nombre archivo completo " + nombre_completo_archivo + "..."
			
			if(validar_archivo(nombre_archivo)):		
				if(validar_archivo_dispositivo(nombre_completo_archivo)):
					dispositivos[contador_archivos_validos][0] = nombre_archivo
					lineas_archivo = leer_lineas_archivo(nombre_completo_archivo)
					
					dispositivos[contador_archivos_validos][1] = lineas_archivo[0]
					dispositivos[contador_archivos_validos][2] = lineas_archivo[1]
					dispositivos[contador_archivos_validos][3] = lineas_archivo[2]
					dispositivos[contador_archivos_validos][4] = lineas_archivo[3]
					dispositivos[contador_archivos_validos][5] = lineas_archivo[4]					
					dispositivos[contador_archivos_validos][6] = lineas_archivo[5]
					
					contador_archivos_validos += 1					
			else:
				print "Archivo " + nombre_archivo + " no valido!"
				
		print "Archivos validos cargados en memoria: " + str(contador_archivos_validos)
		for x in range(0, contador_archivos_validos):
			print "nombre archivo: " + dispositivos[x][0]
			print "Dueno Edificio: " + dispositivos[x][1]
			print "Numero de pisos: " + dispositivos[x][2]
			print "Fotocopiadora: " + dispositivos[x][3]
			print "Aire acondicionado: " + dispositivos[x][4]
			print "Calefactor: " + dispositivos[x][5]
			print "Nevera: " + dispositivos[x][6]									
			print "\n"
			if dispositivos[x][3] > 15:
				guardar_error("Numero en de "+ str(x)+ "en exceso.	Hora del error: "+hora_error)
				terminar_programa("Exceso de electrodomestico permitido.	Hora del error: "+ hora_error)
			else:
				guardar_log("Va bien")
			if dispositivos[x][4] > 15:
				guardar_error("Numero en de "+ str(x)+ "en exceso.	Hora del error: "+hora_error)
				terminar_programa("Exceso de electrodomestico permitido.	Hora del error: "+ hora_error)
			else:
				guardar_log("Va bien")
			if dispositivos[x][5] > 15:
				guardar_error("Numero en de "+ str(x)+ "en exceso.	Hora del error: "+hora_error)
				terminar_programa("Exceso de electrodomestico permitido.	Hora del error: "+ hora_error)
			else:
				guardar_log("Va bien")
			if dispositivos[x][6] > 15:
				guardar_error("Numero en de "+ str(x)+ "en exceso.	Hora del error: "+hora_error)
				terminar_programa("Exceso de electrodomestico permitido.	Hora del error: "+ hora_error)
			else:
				guardar_log("Va bien")
			#Se crea archivo informe.txt y ese imprime lo deseado
			crear_archivo('informe.txt')
			escribir_linea_archivo("informe.txt", "Dueno Edificio: " + dispositivos[x][1]+ "\nNumero de pisos: " + dispositivos[x][2]+ "\nFotocopiadora: " + dispositivos[x][3]+ "\nAire acondicionado: " + dispositivos[x][4]+ "\nCalefactor: " + dispositivos[x][5]+"\nNevera: " + dispositivos[x][6])
		print "Directorio contiene " + str() + " archivos!"	
		
else:
	print "Directorio " + directorio_a_revisar + " no valido!" 	











