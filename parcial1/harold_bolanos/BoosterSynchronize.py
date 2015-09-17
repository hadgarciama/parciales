# BoosterSynchronize v1.0
# Programa disenado para seleccionar las sucursarles de la empresa que son aptas para participar en la capacitacion, 
# internacional. Lee los cargos y el numero de personas por cargo desde un archivo de texto
# que se suministra como argumento de linea de comandos, por ejemplo, nombres.txt. Al final guarda el archivo de las sucursales
# seleccionadas en el archivo revision.txt, el registro de errores en errores.txt y el registro de operacion en log.txt.

# Desarrollado por Harold Esteban Bolanos Serna
# Septiembre 17 de 2015

#------------------------------------------------------------------------------------------


# Importar libreria sys para manejo de argumentos de linea de comandos
import sys

# Importar libreria para manejo del sistema de archivos del sistema operativo.
import os, os.path

# ------------------ Inicio de definicion de constantes y parametros ------------------ #
minimo_archivos_en_directorio = 1

# Extension por defecto
extension_por_defecto = ".txt"

# Nombre archivo de errores
nombre_archivo_errores = "errores" + extension_por_defecto 

# Nombre archivo de registro de operacion del programa
nombre_archivo_registro = "log" + extension_por_defecto 

# Nombre por defecto archivo de sucursales validas
nombre_defecto_archivo_sucursales = "revision" + extension_por_defecto 

# Nombre por defecto archivo de topes
nombre_defecto_archivo_topes = "topes" + extension_por_defecto 

#------------------------------------------FUNCIONES--------------------------------

# 1) un archivo con el nombre especificado. Devuelve True si fue exitoso o False en caso de error.
def crear_archivo(nombre_archivo):
	try:
		archivo = open(nombre_archivo, 'w')
		archivo.close()
	except:
		guardar_error("Error creando archivo " + nombre_archivo + "!");
		return False
		
	return True
	
# 2) Funcion que guarda un registro de operacion en el archivo log.txt
def guardar_log(mensaje_registro):
	escribir_linea_archivo(nombre_archivo_registro, "\n" + mensaje_registro + "\n")
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
	
# 3) Funcion que guarda un mensaje de error en el archivo errores.txt
def guardar_error(mensaje_error):
	escribir_linea_archivo(nombre_archivo_errores, "\n" + mensaje_error + "\n")
	
def validar_archivo(nombre_archivo):
	archivo_valido = True
	
	if(not os.path.isfile(nombre_archivo)):
		#print "No existe archivo " + nombre_archivo
		archivo_valido = False		
		guardar_error("Archivo suministrado no existe.")			
		return archivo_valido

	#El nombre no contenga espacios.
	cantidad_palabras = len(nombre_archivo.split(" "))
		
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
	
# 4) Leer las lineas de un archivo de texto y devolver en una lista.
def leer_lineas_archivo(nombre_archivo):
	lineas = ()
	try:
		archivo = open(nombre_archivo, 'r')
		lineas = archivo.readlines()
		archivo.close()
	except IOError:
		guardar_error("Error leyendo archivo " + nombre_archivo + "!")
		
	return lineas 
	
# 5) validar si un valor string puede ser convertido a numerico.
def validar_tipo_numerico(valor_string):	
	try:
		numerico = int(valor_string)
		return True		
	except ValueError:	
		guardar_error("Valor" + valor_string + " no puede convertirse a tipo numerico!")		
		return False
# Funcion que finaliza el programa y guarda el respectivo mensaje de terminacion en el archivo errores.txt
def terminar_programa(mensaje_terminacion):
	guardar_error(mensaje_terminacion)
	guardar_log("Programa terminado por error... Verificar archivo errores.txt para mas detalles.")
	
	# Terminar el programa
	sys.exit()
	
# 6) valida si una linea tiene la estructura key=value, siendo value de tipo numerico.
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
	
# 7) Validar archivo topes.txt
def validar_archivo_topes(nombre_archivo_topes):
	archivo_topes_valido = True
	
	# Validar la existencia del archivo y su nombre valido
	if(not validar_archivo(nombre_archivo_topes)):
		archivo_topes_valido = False
		return archivo_topes_valido
	
	# Validar el contenido del archivo de topes, solo debe contener lineas de la estructura 
	# key=value
	# Variable que almacena las lineas del archivo de topes, su contenido como tal.
	lineas_archivo_topes = tuple(leer_lineas_archivo(nombre_archivo_topes))
	
	# Variable que almacena el numero de lineas del archivo de topes
	numero_lineas_topes = len(lineas_archivo_topes)
	#print numero_lineas_topes
	# Variable que almacena el numero de lineas validas del archivo de topes
	cantidad_lineas_buenas = 0
	
	for x in range(0, numero_lineas_topes):
		#print "Linea " + str(x) + ": " + lineas_archivo_topes[x]
		
		if(validar_linea_key_value(lineas_archivo_topes[x])):
			cantidad_lineas_buenas += 1
			#print "Linea " + str(x) + ": Valida!"
		else:
			guardar_error("Linea " + str(x) + ": Invalida!")
			
	if(cantidad_lineas_buenas < numero_lineas_topes):
		guardar_error("No todas las lineas del archivo " + nombre_archivo_topes + " son validas! Revisar " + nombre_archivo_errores + "!")
		archivo_topes_valido = False
		return archivo_topes_valido
		
	return archivo_topes_valido

# 8) funcion prueba para la ejecucion del programa.	
def hacer_prueba(nombre_archivo):
	resultado_validacion = validar_archivo(nombre_archivo)
	'''
	if(resultado_validacion):
		#print "El archivo " + nombre_archivo + " es valido!"
	else:
		#print "El archivo " + nombre_archivo + " no es valido. Revisar " + nombre_archivo_errores
	'''
		
	return resultado_validacion
	
# 9) Crear el archivo errores.txt para almacenar los errores que se presenten.
crear_archivo(nombre_archivo_errores)

crear_archivo(nombre_archivo_registro)


guardar_log('Inicio del programa..... iniciando validaciones y verificando los archivos!')

archivos=os.listdir(sys.argv[1])

nombre_prueba1 = sys.argv[1]+"\\"+archivos[0]
nombre_prueba2 = sys.argv[1]+"\\"+archivos[1]
nombre_prueba3 = sys.argv[1]+"\\"+archivos[2]
nombre_prueba4 = sys.argv[1]+"\\"+archivos[3]
nombre_prueba5 = sys.argv[1]+"\\"+archivos[4]

if(hacer_prueba(nombre_prueba1)):
	if(validar_archivo_topes(nombre_prueba1)):
		guardar_log("Archivo " + nombre_prueba1 + " COMPLETAMENTE VALIDO!")
	else:
		guardar_error("Archivo " + nombre_prueba1 + " INVALIDO!")
		
if(hacer_prueba(nombre_prueba2)):
	if(validar_archivo_topes(nombre_prueba2)):
		guardar_log("Archivo " + nombre_prueba2 + " COMPLETAMENTE VALIDO!")
	else:
		guardar_error("Archivo " + nombre_prueba2 + " INVALIDO!")
		
if(hacer_prueba(nombre_prueba3)):
	if(validar_archivo_topes(nombre_prueba3)):
		guardar_log("Archivo " + nombre_prueba3 + " COMPLETAMENTE VALIDO!")
	else:
		guardar_error("Archivo " + nombre_prueba3 + " INVALIDO!")
		
if(hacer_prueba(nombre_prueba4)):
	if(validar_archivo_topes(nombre_prueba4)):
		guardar_log("Archivo " + nombre_prueba4 + " COMPLETAMENTE VALIDO!")
	else:
		guardar_error("Archivo " + nombre_prueba4 + " INVALIDO!")
		
if(hacer_prueba(nombre_prueba5)):
	if(validar_archivo_topes(nombre_prueba5)):
		guardar_log("Archivo " + nombre_prueba5 + " COMPLETAMENTE VALIDO!")
	else:	
		guardar_error("Archivo " + nombre_prueba5 + " INVALIDO!")

# Obtener numero de argumentos de linea de comandos
cantidad_argumentos = len(sys.argv)


# Validar que el numero de argumentos sea igual a 2, garantizando que se haya el nombre del archivo de nomina.
if (cantidad_argumentos != 2):	
	terminar_programa("Numero de argumentos incorrecto. Debe suministrar un argumento con el directorio a buscar.")
	guardar_error("Numero de argumentos incorrecto. Debe suministrar un argumento (directorio del programa) valido.")
directorio_a_revisar = sys.argv[1]


if (os.path.exists(directorio_a_revisar) and os.access(os.path.dirname(directorio_a_revisar), os.R_OK)):
	guardar_log("Directorio " + directorio_a_revisar + " VALIDO!")	
	cantidad_archivos_directorio = len(os.listdir(directorio_a_revisar))
	
	
	if(cantidad_archivos_directorio >= 1):
		guardar_log("Directorio contiene cantidad minima de archivos!")
		guardar_log("validando directorio........ Directorio contiene cantidad minima de archivos!")
		for name in os.listdir(directorio_a_revisar):
			if os.path.isfile(name):
				nombre_archivo = name
				guardar_log('Leyendo archivo ' + nombre_archivo)
		guardar_log("Directorio contiene " + str(cantidad_archivos_directorio) + " archivos!")
	
else:
	guardar_error("Directorio " + directorio_a_revisar + " INVALIDO!")
	
crear_archivo(nombre_defecto_archivo_sucursales)




archivos=os.listdir(sys.argv[1])



archivos_sucursal1=leer_lineas_archivo(sys.argv[1]+"\\"+archivos[0])

archivos_sucursal2=leer_lineas_archivo(sys.argv[1]+"\\"+archivos[1])

archivos_sucursal3=leer_lineas_archivo(sys.argv[1]+"\\"+archivos[2])

archivos_sucursal4=leer_lineas_archivo(sys.argv[1]+"\\"+archivos[3])

archivos_sucursal5=leer_lineas_archivo(sys.argv[1]+"\\"+archivos[4])

topes_=leer_lineas_archivo(nombre_defecto_archivo_topes)



Gerentes=[archivos_sucursal1[0],archivos_sucursal2[0],archivos_sucursal3[0],archivos_sucursal4[0],archivos_sucursal5[0]]
IE=[archivos_sucursal1[1],archivos_sucursal2[1],archivos_sucursal3[1],archivos_sucursal4[1],archivos_sucursal5[1]]
IH=[archivos_sucursal1[2],archivos_sucursal2[2],archivos_sucursal3[2],archivos_sucursal4[2],archivos_sucursal5[2]]
IS=[archivos_sucursal1[3],archivos_sucursal2[3],archivos_sucursal3[3],archivos_sucursal4[3],archivos_sucursal5[3]]
IC=[archivos_sucursal1[4],archivos_sucursal2[4],archivos_sucursal3[4],archivos_sucursal4[4],archivos_sucursal5[4]]
TT=[archivos_sucursal1[6],archivos_sucursal2[6],archivos_sucursal3[6],archivos_sucursal4[6],archivos_sucursal5[6]]

#----------------

listaIE=[]
for i in IE:
	ensayo=i.split('IE=')
	a="".join(ensayo)
	listaIE.append(a)
	
#print listaIE

#------------


listaIH=[]
for i in IH:
	ensayo=i.split('IH=')
	b="".join(ensayo)
	listaIH.append(b)
	
#print listaIH

#-----------


listaIS=[]
for i in IS:
	ensayo=i.split('IS=')
	c="".join(ensayo)
	listaIS.append(c)
	
#print listaIS

#--------------


listaIC=[]
for i in IC:
	ensayo=i.split('IC=')
	d="".join(ensayo)
	listaIC.append(d)
	
#print listaIC

#----------------
#---------------


listaTT=[]
for i in TT:
	ensayo=i.split('TT=')
	f="".join(ensayo)
	listaTT.append(f)
	
#print listaTT

#----------------

listatopes1=[]
for i in topes_:
	ensayo=i.split('=')
	ensayo[0]=""
	g="".join(ensayo)
	listatopes1.append(g)
	
listatopes_=listatopes1[1:6]	
#print listatopes_
guardar_log(".....Analizando los archivos del directorio.....")

#-------------Programa interno-------
#----------------
print 'Detalles de cada sucursal debido a los cargos'
print ' '
for i in range(0,5):
	if listaIE[i]>=listatopes_[0] :
		print i,archivos[i]
		print 'IE VALIDOS'
	else :
		print 'IE NO VALIDOS'
	if listaIH[i]>=listatopes_[1]:
		print 'IH VALIDOS'
	else:
		print 'IH NO VALIDOS'
	if listaIS[i]>=listatopes_[2]:
		print 'IS VALIDOS'
	else:
		print 'IS NO VALIDOS'
	if listaIC[i]>=listatopes_[3]:
		print 'IC VALIDOS'
	else:
		print 'IC NO VALIDOS'

guardar_log('Comparando numero de empleados con el minimo requerido en topes.txt.....')

if listaIE[0]>=listatopes_[0] and listaIH[0]>=listatopes_[1] and listaIS[0]>=listatopes_[2] and listaIC[0]>=listatopes_[3]:
		escribir_linea_archivo(nombre_defecto_archivo_sucursales,'Bogota - SUCURSAL VALIDA\n')
else:
		escribir_linea_archivo(nombre_defecto_archivo_sucursales,'Bogota - SUCURSAL INVALIDA\n')
		
if listaIE[1]>=listatopes_[0] and listaIH[1]>=listatopes_[1] and listaIS[1]>=listatopes_[2] and listaIC[1]>=listatopes_[3]:
		escribir_linea_archivo(nombre_defecto_archivo_sucursales,'Buenos Aires - SUCURSAL VALIDA\n')
else:
		escribir_linea_archivo(nombre_defecto_archivo_sucursales,'Buenos Aires - SUCURSAL INVALIDA\n')
		
if listaIE[2]>=listatopes_[0] and listaIH[2]>=listatopes_[1] and listaIS[2]>=listatopes_[2] and listaIC[2]>=listatopes_[3]:
		escribir_linea_archivo(nombre_defecto_archivo_sucursales,'Lima - SUCURSAL VALIDA\n')
else:
		escribir_linea_archivo(nombre_defecto_archivo_sucursales,'Lima - SUCURSAL INVALIDA\n')
		
if listaIE[3]>=listatopes_[0] and listaIH[3]>=listatopes_[1] and listaIS[3]>=listatopes_[2] and listaIC[3]>=listatopes_[3]:
		escribir_linea_archivo(nombre_defecto_archivo_sucursales,'Rio de Janeiro - SUCURSAL VALIDA\n')
else:
		escribir_linea_archivo(nombre_defecto_archivo_sucursales,'Rio de Janeiro - SUCURSAL INVALIDA\n')
		
if listaIE[4]>=listatopes_[0] and listaIH[4]>=listatopes_[1] and listaIS[4]>=listatopes_[2] and listaIC[4]>=listatopes_[3]:
		escribir_linea_archivo(nombre_defecto_archivo_sucursales,'Santiago - SUCURSAL VALIDA\n')
else:
		escribir_linea_archivo(nombre_defecto_archivo_sucursales,'Santiago - SUCURSAL INVALIDA\n')
		
guardar_log("Programa terminado!! por favor revisar el archivo revision.txt")
print "Programa terminado!! por favor revisar el archivo revision.txt"

guardar_log("Programa realizado por Harold Esteban Bolanos Serna")
print "Programa realizado por Harold Esteban Bolanos Serna"
guardar_log("Tecnicas de programacion 2015-03")
print "Tecnicas de programacion 2015-03"







		
		