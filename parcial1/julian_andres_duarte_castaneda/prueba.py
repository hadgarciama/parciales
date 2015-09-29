# recorte de nomina v1.0
# desarrollado por Julian Andres Duarte Castaneda 
# septiembre 17 2015
'''programa realizado para momentos de crisis empresarial, dicho programa se basa eb un estudio
previo , realizado para determinar la maxima cantidad de empleados con la cual se puede mantener  la
linea de produccion de la compania, con base  a esto se puede tomar desiones para abordar medidas en 
recotes de personal.'''

import os
import sys
# ------------------ Inicio de definicion de constantes y parametros ------------------ #
# Nombre archivo de errores
nombre_archivo_errores = "errores.txt"
# Nombre archivo de registro de operacion del programa
nombre_archivo_registro = "log.txt"
# Nombre archivo que contiene los maximos de cargos permitidos 
nombre_archivo_recorte = "recorte.txt"
# nombre del archivo que contiene el reporte del total de empleados 
nombre_archivo_resumen = "resumen.txt"
num_min=4
# ------------------ Fin de definicion de constantes y parametros ------------------ #
# ------------- Inicio de definicion de funciones que se van a emplear  ------------- #

# Funcion 1 -> definir directorio 
def directory(path,extension):
  list_dir = []
  list_dir = os.listdir(path)
  count = 0
  for file in list_dir:
    if file.endswith(extension): # eg: '.txt'
      count += 1
  return count


# Funcion 2 -> crear archivo con el nombre especifico y extension determinada
def crear_archivo(nombre_archivo):
	try:
		archivo = open(nombre_archivo, 'w')
		archivo.close()
	except:
		guardar_error("Error creando archivo " + nombre_archivo + "!");
		return False
		
	return True

# Funcion 3 -> para guardar los errores que se generan el el trascurso del programa
def guardar_error(mensaje_error):
	escribir_linea_archivo(nombre_archivo_errores, "\n" + mensaje_error + "\n")

# Funcion 4 -> guardar los procesos realizados por el programa 
def guardar_log(mensaje_registro):
	escribir_linea_archivo(nombre_archivo_registro, "\n" + mensaje_registro + "\n")

# Funcion 5 -> termina el programa ya sea al finalizar el los procesos o en caso de un error inesperado 
def terminar_programa(mensaje_terminacion):
	guardar_error(mensaje_terminacion)
	guardar_log("Programa terminado por error... Verificar archivo errores.txt para mas detalles.")
	
	# Terminar el programa
	sys.exit()

# Funcion 6 -> escribir una linea de archivo

def escribir_linea_archivo(nombre_archivo, linea_a_escribir):	
	try:
		archivo = open(nombre_archivo, 'a')
		archivo.write(linea_a_escribir)
		archivo.close()
	except IOError:
		guardar_error("Error escribiendo linea " + linea_a_escribir + " en archivo " + nombre_archivo + "!")
		return False
		
	return True


# Funcion 7 -> leer la  linea de un archivos

def leer_lineas_archivo(nombre_archivo):
	lineas = ()
	try:
		archivo = open(nombre_archivo, 'r')
		lineas = archivo.readlines()
		archivo.close()
	except IOError:
		guardar_error("Error leyendo archivo " + nombre_archivo + "!")
		
	return lineas 

# Funcion 8 -> valida que la linea cumpla con la estructura detareminada
def validar_linea(linea_por_validar, numero_linea):	
	array_respuesta = [0 for x in range(2)]
	
	# Separar la linea por el simbolo  *
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


# ------------- Fin de definicion de funciones ------------- #


# Crear el archivo errores.txt para almacenar los errores que se presenten.
crear_archivo("errores.txt")

# Crear el archivo log.txt para almacenar el registro de operacion del programa.
crear_archivo("log.txt")

guardar_log("Creados archivos errores.txt y log.txt")
	
	
	
# ------------- Fin de definicion de funciones ------------- #
# ------------- inicio logica del programa ------------- #

program_path = os.getcwd()

decision = sys.argv[1]
cargos = sys.argv[2]
excesos = sys.argv[3]

if (sys.argv[2].endswith(".txt") == False):
	terminar_programa("El archivo cargos no tiene extension .txt!")
else:
	guardar_log("Extension de archivo de cargos OK")
	
if (sys.argv[3].endswith(".txt") == False):
	terminar_programa("El archivo excesos no tiene extension .txt!")
else:
	guardar_log("Extension de archivo de excesos OK")

leido_cargos=tuple(leer_lineas_archivo(cargos))
num_rec=len(leido_cargos)

guardar_log("archivo cargos leido OK")

leido_excesos=tuple(leer_lineas_archivo(excesos))
num_excesos=len(leido_excesos)

guardar_log("archivo excesos leido OK")

if(num_excesos!=num_rec and num_excesos==num_min):
	terminar_programa("Los archivos excesos y cargos no tienen igual numero de lineas o igual al numero de cargos")
else:
	guardar_log("archivos con igual numero de lineas e igual al numero de cargos")
	
array_excesos = [[columnas for columnas in range(2)] for filas in range(num_excesos)]

guardar_log("Cargando excesos en memoria...");
for x in range(0, num_excesos):
	linea_validada = validar_linea(leido_excesos[x], x+1)
	guardar_log("Procesando linea " + str(x+1));
	array_excesos[x][0] = linea_validada[0]
	array_excesos[x][1] = linea_validada[1]

guardar_log("excesos cargada en memoria!");

count=directory(sys.argv[1],'.txt')
if(count==0):
	terminar_programa("no hay archivos validos en el directorio")
i=0
mal=[[columnas for columnas in range(1)] for filas in range(100)]
array_directorio = [[columnas for columnas in range(1)] for filas in range(count)]
rootDir = decision
for dirName, subdirList, fileList in os.walk(rootDir):
   
    for fname in fileList:
		if(fname.endswith('.txt')):
			array_directorio[i][0] = fname
		else:
			mal[i][0]=fname
			i=i-1
		if(i!=(count-1)):
			i=i+1
guardar_log("directorio encontrado");
 

guardar_log("contanto archivos con extension '.txt' en el directorio")
guardar_log("archivos OK contados y listados")
guardar_log("procesando informacion del directorio")
guardar_log("si no se continua el texto leer archivo errores.txt y log.txt en directorio dado")
os.chdir(decision)

array_array = [[columnas for columnas in range(6)] for filas in range(count)]
for x in range(0,count):
	array_array[x]=tuple(leer_lineas_archivo(array_directorio[x][0]))



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

os.chdir(program_path)
guardar_log("informacion del directorio procesada");
guardar_log("creando array array_suma");

array_suma = [[columnas for columnas in range(1)] for filas in range(4)]

guardar_log("sumando cargos")
k=0	
while (k<4):
	for x in range(1,count+1):
		array_suma[k][0]+=int(array_validado[x][k])
	k=k+1

guardar_log("cargos sumados y guardados")

array_prom = [[columnas for columnas in range(1)] for filas in range(4)]

for x in range (0,4):
	array_prom[x][0]=array_suma[x][0]/count
	
guardar_log("cargos promediados y guardados")

array_comparacion = [[columnas for columnas in range(4)] for filas in range(count)]

guardar_log("comparando datos de cargos de los archivos con la excesos")
k=1
i=0
while (k<count+1):
	for x in range (0,4):
		array_comparacion[i][x]=array_validado[k][x]-array_excesos[x][1]
	k=k+1
	i=i+1
guardar_log("datos comparados y guardados")

guardar_log("archivo recorte.txt creado y en ejecucion")
crear_archivo("recorte.txt")
i=0
while (i<count-1):
	for x in range(0, 1):
		if(array_comparacion[i][x]>0 and array_comparacion[i][x+1]>0 and array_comparacion[i][x+2]>0 and array_comparacion[i][x+3]):
			
			escribir_linea_archivo(nombre_archivo_recorte, array_directorio[i][0] + "\n")	
		i=i+1
guardar_log("archivo recorte.txt cerrado")

crear_archivo("resumen.txt")
guardar_log("archivo resumen.txt creado y en ejecucion")
totales=str('TOTALES')
fortotales="%s\n\n"
escribir_linea_archivo(nombre_archivo_resumen, fortotales % (totales))
for x in range (0,4):
	contenido_linea1 = ( 
		array_excesos[x][0], array_suma[x][0],
	)
	formato_linea1 = "\t%s %d\n\n"
	escribir_linea_archivo(nombre_archivo_resumen, formato_linea1 % (contenido_linea1))

promedio=str('PROMEDIO'),
forprom="%s\n\n"
escribir_linea_archivo(nombre_archivo_resumen, forprom % (promedio))		
for x in range (0,4):
	contenido_linea1 = (	
		array_excesos[x][0], array_prom[x][0],
	)
	formato_linea1 = "\t%s %d\n\n"
	escribir_linea_archivo(nombre_archivo_resumen, formato_linea1 % (contenido_linea1))
	
datlun=str('DATOS directorio'),
fordatlun="%s\n\n"
escribir_linea_archivo(nombre_archivo_resumen, fordatlun % (datlun))
for x in range(0, count):
	contenido_linea2 = (
		array_directorio[x][0],array_array[x][0],array_array[x][1],	
	)
	formato_linea2 = "\t%s %s \t%s\n "
	escribir_linea_archivo(nombre_archivo_resumen, formato_linea2 % (contenido_linea2))

guardar_log("archivo resumen.txt cerrado")
guardar_log("programa terminado, abrir archivo resumen.txt y recorte.txt")
# ------------- fin  logica del programa ------------- #