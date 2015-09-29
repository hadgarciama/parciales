# Importar libreria sys para manejo de argumentos de linea de comandos
import sys, multiprocessing, time



# Importar libreria para manejo del sistema de archivos del sistema operativo.
import os, os.path

# ------------------ Inicio de definicion de constantes y parametros ------------------ #
# Crear el archivo errores.txt para almacenar los errores que se presenten.


minimo_archivos_en_directorio = 1

# Extension por defecto
extension_por_defecto = ".txt"

# Nombre archivo de errores
nombre_archivo_errores = "errores" + extension_por_defecto 

# Nombre archivo de registro de operacion del programa
nombre_archivo_registro = "log" + extension_por_defecto 

# Nombre por defecto archivo de electrodomesticos
nombre_defecto_archivo_electrodomesticos = "electrodomesticos" + extension_por_defecto 

# Nombre por defecto archivo de maximos
nombre_defecto_archivo_maximos = "maximos" + extension_por_defecto 

# Funcion que crear un archivo con el nombre especificado. Devuelve True si fue exitoso o False en caso de error.
def crear_archivo(nombre_archivo):
	try:
		archivo = open(nombre_archivo, 'w')
		archivo.close()
	except:
		guardar_error("Error creando archivo " + nombre_archivo + "!");
		return False
		
	return True
	
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
	
def validar_archivo(nombre_archivo):
	archivo_valido = True
	
	# Validacion 10 -> El archivo.txt debe existir.
	if(not os.path.isfile(nombre_archivo)):
		#print "No existe archivo " + nombre_archivo
		archivo_valido = False		
		guardar_error("Archivo suministrado no existe.")			
		return archivo_valido

	# Validar que el nombre no contenga espacios.
	cantidad_palabras = len(nombre_archivo.split(" "))
	
	# Validar que no contenga espacios.	
	if(cantidad_palabras > 1):
		archivo_valido = False
		guardar_error("Nombre de archivo tiene mas de una palabra.")
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
	
	
	
# Funcion que valida si el valor string puede ser convertido a numerico.
def validar_tipo_numerico(valor_string):	
	try:
		numerico = int(valor_string)
		return True		
	except ValueError:	
		guardar_error("Valor" + valor_string + " no puede convertirse a tipo numerico!")		
		return False

# Funcion que valida si una linea tiene la estructura key=value, siendo value de tipo numerico.
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
	
# Funcion 1 -> Validar archivo maximos.txt
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
		#print "Linea " + str(x) + ": " + lineas_archivo_maximos[x]
		
		if(validar_linea_key_value(lineas_archivo_maximos[x])):
			cantidad_lineas_buenas += 1
			#print "Linea " + str(x) + ": Valida!"
		else:
			guardar_error("Linea " + str(x) + ": Invalida!")
			
	if(cantidad_lineas_buenas < numero_lineas_maximos):
		guardar_error("No todas las lineas del archivo " + nombre_archivo_maximos + " son validas! Revisar " + nombre_archivo_errores + "!")
		archivo_maximos_valido = False
		return archivo_maximos_valido
		
	return archivo_maximos_valido
		
def hacer_prueba(nombre_archivo):
	resultado_validacion = validar_archivo(nombre_archivo)
	'''
	if(resultado_validacion):
		#print "El archivo " + nombre_archivo + " es valido!"
	else:
		#print "El archivo " + nombre_archivo + " no es valido. Revisar " + nombre_archivo_errores
	'''
		
	return resultado_validacion
	
for i in range(1, 10):
	
	estension_por_defecto = ".txt"
	numero_casas= ("casa", i + estension_por_defecto)

leer_lineas_archivo(numero_casas)
lineas_numero_casas = ()
	
leer_lineas_archivo(maximos.txt)
lineas_maximos = ()
	


try: 	
	leer_lineas_archivo(numero_casas)
	lineas_numero_casas = ()
	leer_lineas_archivo(maximos.txt)
	lineas_maximos = ()
	
	n=0
	
	if (lineas_numero_casas[2].startswith("nevera")):
		n +1
		
	else:
		print ("error de clasificacion de electrodomesticos")	
	
	if (lineas_numero_casas[3].startswith("estufa")):
		n +1
	else :
		print ("error de clasificacion de electrodomesticos")
		
	if(lineas_numero_casas[4].startswith("lavadora")):
		n +1
	else :
		print ("error de clasificacion de electrodomesticos")
			
	if(lineas_numero_casas[5].startswith("microhondas")):
		n +1
	else: 
		print ("error de clasificacion de electrodomesticos")
			
	if(lineas_numero_casas[6].startswith("televisor")):
		n +1
	else: 
		print ("error de clasificacion de electrodomesticos")
				
	if(lineas_numero_casas[7].startswith("ducha")):
		n +1
	else: 
		print ("error de clasificacion de electrodomesticos")
					
	if(lineas_numero_casas[8].startswith("ducha")):
		n +1
	else: 
		print ("error de clasificacion de electrodomesticos")
	
	
	if (n == len(lineas_maximos)):
		print ("El archivo tiene una estructura correcta")
		

	if (n != len(lineas_maximos)):
		guardar_error("El archivo tiene una estructura DEFECTUOSA")
		return numero_casas
	
	for [i] in range(2, 10) :

		lineas_numero_casas[i] <= lineas_maximos[i]
	
		if (lineas_numero_casas[i] > lineas_maximos[i]):
	
			crear_archivo (exceso_de_electrodomesticos, lineas_numero_casas[i])
		
		else: 
			guardar_error ("Se encuentra un exceso de electrodomesticos en: " + lineas_numero_casas[i])
	



	



#	nombre_prueba = "maximos.txt"
#	if(hacer_prueba(nombre_prueba)):
#		if(validar_archivo_maximos(nombre_prueba)):
#			print "Archivo " + nombre_prueba1 + " COMPLETAMENTE VALIDO!"
#		else:
#			print "Archivo " + nombre_prueba1 + " INVALIDO!"
#			
#	nombre_prueba2 = "maximosdias.txt"
#	if(hacer_prueba(nombre_prueba2)):
#		if(validar_archivo_maximos(nombre_prueba2)):
#			print "Archivo " + nombre_prueba2 + " COMPLETAMENTE VALIDO!"
#		else:
#			print "Archivo " + nombre_prueba2 + " INVALIDO!"
#			
#	nombre_prueba3 = "maximos.txtp"
#	if(hacer_prueba(nombre_prueba3)):
#		if(validar_archivo_maximos(nombre_prueba3)):
#		print "Archivo " + nombre_prueba3 + " COMPLETAMENTE VALIDO!"
#		else:
#			print "Archivo " + nombre_prueba3 + " INVALIDO!"
#			
#	nombre_prueba4 = "maximus.txt"
#		if(hacer_prueba(nombre_prueba4)):
#			if(validar_archivo_maximos(nombre_prueba4)):
#				print "Archivo " + nombre_prueba4 + " COMPLETAMENTE VALIDO!"
#			else:
#				print "Archivo " + nombre_prueba4 + " INVALIDO!"



# Validar que el numero de argumentos sea igual a 2, garantizando que se haya el nombre del archivo de nomina.
# Validacion 1 (Va1)

try:
	crear_archivo (nombre_archivo_errores)

	# Obtener numero de argumentos de linea de comandos
	cantidad_argumentos = len(sys.argv)

	directorio_a_revisar = sys.argv[1]

	if (cantidad_argumentos != 2):	
		terminar_programa("Numero de argumentos incorrecto. Debe suministrar un argumento con el directorio a buscar.")



	if (os.path.exists(directorio_a_revisar) and os.access(os.path.dirname(directorio_a_revisar), os.R_OK)):
		print "Directorio " + directorio_a_revisar + " VALIDO!" 	
			cantidad_archivos_directorio = len([name for name in os.listdir(directorio_a_revisar) if os.path.isfile(name)])
	
		if(cantidad_archivos_directorio >= 1):
			print "Directorio contiene cantidad minima de archivos!"
			for name in os.listdir(directorio_a_revisar):
				if os.path.isfile(name):
					nombre_archivo = name
					print 'Leyendo archivo ' + nombre_archivo
				
			print "Directorio contiene " + str() + " archivos!"
	
	else: guardar_error "direccion de ubicacion de los archivos incorrecta"

print "Directorio " + directorio_a_revisar + " INVALIDO!" 
	




