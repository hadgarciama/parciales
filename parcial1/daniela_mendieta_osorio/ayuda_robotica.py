import os
import sys

nombre_archivo_errores = "errores.txt"
nombre_archivo_registro = "log.txt"
nombre_archivo_ayuda_medica= "ayuda_medica.txt"
nombre_archivo_informe = "informe.txt"
num_min=4


def directory(path,extension):
  list_dir = []
  list_dir = os.listdir(path)
  count = 0
  for file in list_dir:
    if file.endswith(extension): # eg: '.txt'
      count += 1
  return count



# Funcion que crear un archivo con el nombre especificado. Devuelve True si fue exitoso o False en caso de error.
def crear_archivo(nombre_archivo):
	try:
		archivo = open(nombre_archivo, 'w')
		archivo.close()
	except:
		guardar_error("Error creando archivo " + nombre_archivo + "!");
		return False
		
	return True


# Funcion que guarda un mensaje de error en el archivo errores.txt
def guardar_error(mensaje_error):
	escribir_linea_archivo(nombre_archivo_errores, "\n" + mensaje_error + "\n")
	
# Funcion que guarda un registro de operacion en el archivo log.txt
def guardar_log(mensaje_registro):
	escribir_linea_archivo(nombre_archivo_registro, "\n" + mensaje_registro + "\n")


def terminar_programa(mensaje_terminacion):
	guardar_error(mensaje_terminacion)
	guardar_log("Programa terminado por error... Verificar archivo errores.txt para mas detalles.")
	
	# Terminar el programa
	sys.exit()


def escribir_linea_archivo(nombre_archivo, linea_a_escribir):	
	try:
		archivo = open(nombre_archivo, 'a')
		archivo.write(linea_a_escribir)
		archivo.close()
	except IOError:
		guardar_error("Error escribiendo linea " + linea_a_escribir + " en archivo " + nombre_archivo + "!")
		return False
		
	return True

	
def leer_lineas_archivo(nombre_archivo):
	lineas = ()
	try:
		archivo = open(nombre_archivo, 'r')
		lineas = archivo.readlines()
		archivo.close()
	except IOError:
		guardar_error("Error leyendo archivo " + nombre_archivo + "!")
		
	return lineas 

def validar_linea(linea_por_validar, numero_linea):	
	array_respuesta = [0 for x in range(2)]
	
	# Separar la linea por el simbolo (token) *
	arreglo_campos = linea_por_validar.split("*")	
	array_respuesta[0]=arreglo_campos[0]
	# Validar que el campo sea de tipo numerico
	try:
		personas_restricciones = int(arreglo_campos[1])								
		array_respuesta[1] = personas_restricciones
	except ValueError:
		guardar_error(arreglo_campos[1] + " no puede convertirse a entero!")
		return array_respuesta
	return array_respuesta
	


# Crear el archivo errores.txt para almacenar los errores que se presenten.
crear_archivo("errores.txt")

# Crear el archivo log.txt para almacenar el registro de operacion del programa.
crear_archivo("log.txt")

guardar_log("Creados archivos errores.txt y log.txt")
	
	
	

program_path = os.getcwd()

ruta = sys.argv[1]
rangos_de_edad = sys.argv[2]
restricciones = sys.argv[3]

if (sys.argv[2].endswith(".txt") == False):
	terminar_programa("El archivo rangos_de_edad no tiene extension .txt!")
else:
	guardar_log("Extension de archivo de rangos_de_edad es bueno")
	
if (sys.argv[3].endswith(".txt") == False):
	terminar_programa("El archivo restricciones no tiene extension .txt!")
else:
	guardar_log("Extension de archivo de restricciones es bueno")

leido_rangos_de_edad=tuple(leer_lineas_archivo(rangos_de_edad))
num_rec=len(leido_rangos_de_edad)

guardar_log("archivo rangos_de_edad leido es bueno ")

leido_restricciones=tuple(leer_lineas_archivo(restricciones))
num_restricciones=len(leido_restricciones)

guardar_log("archivo restricciones leido OK")

if(num_restricciones!=num_rec and num_restricciones==num_min):
	terminar_programa("Los archivos restricciones y rangos_de_edad no tienen igual numero de lineas ")
else:
	guardar_log("archivos con igual numero de lineas ")
	
array_restricciones = [[columnas for columnas in range(2)] for filas in range(num_restricciones)]

guardar_log("Cargando restricciones en memoria...");
for x in range(0, num_restricciones):
	linea_validada = validar_linea(leido_restricciones[x], x+1)
	guardar_log("Procesando linea " + str(x+1));
	array_restricciones[x][0] = linea_validada[0]
	array_restricciones[x][1] = linea_validada[1]

guardar_log("restricciones cargada en memoria!");

count=directory(sys.argv[1],'.txt')
if(count==0):
	terminar_programa("no hay archivos validos en el directorio")
i=0
mal=[[columnas for columnas in range(1)] for filas in range(100)]
array_BARRIOS = [[columnas for columnas in range(1)] for filas in range(count)]
rootDir = ruta
for dirName, subdirList, fileList in os.walk(rootDir):
   
    for fname in fileList:
		if(fname.endswith('.txt')):
			array_BARRIOS[i][0] = fname
		else:
			mal[i][0]=fname
			i=i-1
		if(i!=(count-1)):
			i=i+1
guardar_log("directorio encontrado");
 

guardar_log("contanto archivos con extension '.txt' en el directorio")
guardar_log("archivos okay contados y listados")
guardar_log("procesando informacion del directorio")
guardar_log("si no se continua el texto leer archivo errores.txt y log.txt en directorio dado")
os.chdir(ruta)

array_array = [[columnas for columnas in range(6)] for filas in range(count)]
for x in range(0,count):
	array_array[x]=tuple(leer_lineas_archivo(array_BARRIOS[x][0]))



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

guardar_log("sumando personas")
k=0	
while (k<4):
	for x in range(1,count+1):
		array_suma[k][0]+=int(array_validado[x][k])
	k=k+1

guardar_log("personas sumados y guardados")

array_prom = [[columnas for columnas in range(1)] for filas in range(4)]

for x in range (0,4):
	array_prom[x][0]=array_suma[x][0]/count
	
guardar_log("personas promediados y guardados")

array_comparacion = [[columnas for columnas in range(4)] for filas in range(count)]

guardar_log("comparando datos de personas de los archivos con la restricciones")
k=1
i=0
while (k<count+1):
	for x in range (0,4):
		array_comparacion[i][x]=array_validado[k][x]-array_restricciones[x][1]
	k=k+1
	i=i+1
guardar_log("datos comparados y guardados")

guardar_log("archivo ayuda_medica.txt creado y en ejecucion")
crear_archivo("ayuda_medica.txt")
i=0
while (i<count-1):
	for x in range(0, 1):
		if(array_comparacion[i][x]>0 and array_comparacion[i][x+1]>0 and array_comparacion[i][x+2]>0 and array_comparacion[i][x+3]):
			
			escribir_linea_archivo(nombre_archivo_ayuda_medica, array_BARRIOS[i][0] + "\n")	
		i=i+1
guardar_log("archivo ayuda_medica.txt cerrado")

crear_archivo("informe.txt")
guardar_log("archivo informe.txt creado y en ejecucion")
totales=str('TOTALES')
fortotales="%s\n\n"
escribir_linea_archivo(nombre_archivo_informe, fortotales % (totales))
for x in range (0,4):
	contenido_linea1 = ( 
		array_restricciones[x][0], array_suma[x][0],
	)
	formato_linea1 = "\t%s %d\n\n"
	escribir_linea_archivo(nombre_archivo_informe, formato_linea1 % (contenido_linea1))

promedio=str('PROMEDIO'),
forprom="%s\n\n"
escribir_linea_archivo(nombre_archivo_informe, forprom % (promedio))		
for x in range (0,4):
	contenido_linea1 = (	
		array_restricciones[x][0], array_prom[x][0],
	)
	formato_linea1 = "\t%s %d\n\n"
	escribir_linea_archivo(nombre_archivo_informe, formato_linea1 % (contenido_linea1))
	
datlun=str('DATOS BARRIOS'),
fordatlun="%s\n\n"
escribir_linea_archivo(nombre_archivo_informe, fordatlun % (datlun))
for x in range(0, count):
	contenido_linea2 = (
		array_BARRIOS[x][0],array_array[x][0],array_array[x][1],	
	)
	formato_linea2 = "\t%s %s \t%s\n "
	escribir_linea_archivo(nombre_archivo_informe, formato_linea2 % (contenido_linea2))

guardar_log("archivo informe.txt cerrado")
guardar_log("programa terminado, abrir archivo informe.txt y ayuda_medica.txt")



