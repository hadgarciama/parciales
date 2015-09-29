# GANAMAX_PCDN v1.0
# Desarrollado por Kevin Leonardo Cerpa Campanella
# Septiembre 17 de 2015
'''
Programa que revisa una serie de municipios, para definir cuales municipios productores de leche son viables a
una modernizacion en teniendo en cuenta algunos minimos, se genera un archivo con los departamentos viables
llamado modernizacion y otro donde estan los informes con los departamentos revisados.
'''
# Importar libreria sys para manejo de argumentos de linea de comandos
import sys
# Importar libreria os para acceder a funcionalidades dependientes del Sistema Operativo
import os
# ------------------ Inicio de definicion de constantes y parametros ------------------ #
nombre_archivo_errores = "errores.txt"
nombre_archivo_registro = "procesos.txt"
nombre_archivo_modernizacion = "modernizacion.txt"
nombre_archivo_informe = "informe.txt"
num_min=4

# ------------------ Fin de definicion de constantes y parametros ------------------ #

# ------------------ Inicio de definicion de funciones empleadas ------------------ #
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
	
# Funcion que guarda un registro de operacion en el archivo procesos.txt
def guardar_procesos(mensaje_registro):
	escribir_linea_archivo(nombre_archivo_registro, "\n" + mensaje_registro + "\n")


def terminar_programa(mensaje_terminacion):
	guardar_error(mensaje_terminacion)
	guardar_procesos("Programa terminado por error... Verificar archivo errores.txt para mayor informacion.")
	
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
		insumos_minimos = int(arreglo_campos[1])
		array_respuesta[1] = insumos_minimos
	except ValueError:
		guardar_error(arreglo_campos[1] + " no puede convertirse a entero!")
		return array_respuesta
	return array_respuesta
	
# ------------------ Fin de definicion de funciones empleadas ------------------ #

# Crear el archivo errores.txt para almacenar los errores que se presenten.
crear_archivo("errores.txt")

# Crear el archivo procesos.txt para almacenar el registro de operacion del programa.
crear_archivo("procesos.txt")

guardar_procesos("Creados archivos errores.txt y procesos.txt")

program_path = os.getcwd()

revision = sys.argv[1]
insumos_herramientas = sys.argv[2]
minimos = sys.argv[3]

if (sys.argv[2].endswith(".txt") == False):
	terminar_programa("El archivo insumos_herramientas no tiene extension exigida por el programa(.txt)!")
else:
	guardar_procesos("Extension de archivo de insumos_herramientas ACEPTADA")

if (sys.argv[3].endswith(".txt") == False):
	terminar_programa("El archivo minimos no tiene extension exigida por el programa(.txt)!")
else:
	guardar_procesos("Extension de archivo de minimos ACEPTADA")

leido_insumos_herramientas=tuple(leer_lineas_archivo(insumos_herramientas))
num_rec=len(leido_insumos_herramientas)
guardar_procesos("archivo insumos_herramientas leido y en excelente estado")
leido_minimos=tuple(leer_lineas_archivo(minimos))
num_minimos=len(leido_minimos)
guardar_procesos("archivo minimos leido y aceptado")
if(num_minimos!=num_rec and num_minimos==num_min):
	terminar_programa("Los archivos minimos y insumos_herramientas no tienen igual numero de lineas o igual al numero de insumos")
else:
	guardar_procesos("archivos con igual numero de lineas e igual al numero de insumos ACEPTADOS")

array_minimos = [[columnas for columnas in range(2)] for filas in range(num_minimos)]

guardar_procesos("Cargando minimos en memoria...");
for x in range(0, num_minimos):
	linea_validada = validar_linea(leido_minimos[x], x+1)
	guardar_procesos("Procesando linea " + str(x+1));
	array_minimos[x][0] = linea_validada[0]
	array_minimos[x][1] = linea_validada[1]

guardar_procesos("minimos cargado en memoria!");

count=directory(sys.argv[1],'.txt')
if(count==0):
	terminar_programa("no hay archivos validos en el directorio")
i=0
mal=[[columnas for columnas in range(1)] for filas in range(100)]
array_departamentos = [[columnas for columnas in range(1)] for filas in range(count)]
rootDir = revision
for dirName, subdirList, fileList in os.walk(rootDir):
   
    for fname in fileList:
		if(fname.endswith('.txt')):
			array_departamentos[i][0] = fname
		else:
			mal[i][0]=fname
			i=i-1
		if(i!=(count-1)):
			i=i+1
guardar_procesos("directorio encontrado");
 
guardar_procesos("contanto archivos con extension '.txt' en el directorio REALIZADO EXITOSAMENTE")
guardar_procesos("archivos contados y listados REALIZADO EXITOSAMENTE")
guardar_procesos("procesando informacion del directorio REALIZADO EXITOSAMENTE")
guardar_procesos("si no se continua el texto leer archivo errores.txt y procesos.txt en directorio dado")
os.chdir(revision)

array_array = [[columnas for columnas in range(6)] for filas in range(count)]
for x in range(0,count):
	array_array[x]=tuple(leer_lineas_archivo(array_departamentos[x][0]))

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
guardar_procesos("informacion del directorio procesada");
guardar_procesos("creando array array_suma");

array_suma = [[columnas for columnas in range(1)] for filas in range(4)]

guardar_procesos("sumando insumos")
k=0	
while (k<4):
	for x in range(1,count+1):
		array_suma[k][0]+=int(array_validado[x][k])
	k=k+1

guardar_procesos("insumos sumados , guardados y ordenados")
array_prom = [[columnas for columnas in range(1)] for filas in range(4)]

for x in range (0,4):
	array_prom[x][0]=array_suma[x][0]/count
	
guardar_procesos("insumos promediados y guardados")
array_comparacion = [[columnas for columnas in range(4)] for filas in range(count)]

guardar_procesos("comparando datos de insumos de los archivos con la de minimos")
k=1
i=0
while (k<count+1):
	for x in range (0,4):
		array_comparacion[i][x]=array_validado[k][x]-array_minimos[x][1]
	k=k+1
	i=i+1
guardar_procesos("datos comparados y guardados")
guardar_procesos("archivo modernizacion.txt creado y en ejecucion")
crear_archivo("modernizacion.txt")
i=0
while (i<count-1):
	for x in range(0, 1):
		if(array_comparacion[i][x]>0 and array_comparacion[i][x+1]>0 and array_comparacion[i][x+2]>0 and array_comparacion[i][x+3]):
			
			escribir_linea_archivo(nombre_archivo_modernizacion, array_departamentos[i][0] + "\n")	
		i=i+1
guardar_procesos("archivo modernizacion.txt cerrado y en ejecucion")

crear_archivo("informe.txt")
guardar_procesos("archivo informe.txt creado y en ejecucion")
totales=str('TOTALES')
fortotales="%s\n\n"
escribir_linea_archivo(nombre_archivo_informe, fortotales % (totales))
for x in range (0,4):
	contenido_linea1 = ( 
		array_minimos[x][0], array_suma[x][0],
	)
	formato_linea1 = "\t%s %d\n\n"
	escribir_linea_archivo(nombre_archivo_informe, formato_linea1 % (contenido_linea1))

promedio=str('PROMEDIO'),
forprom="%s\n\n"
escribir_linea_archivo(nombre_archivo_informe, forprom % (promedio))		
for x in range (0,4):
	contenido_linea1 = (	
		array_minimos[x][0], array_prom[x][0],
	)
	formato_linea1 = "\t%s %d\n\n"
	escribir_linea_archivo(nombre_archivo_informe, formato_linea1 % (contenido_linea1))

datdep=str('DATOS departamentos'),
fordatdep="%s\n\n"
escribir_linea_archivo(nombre_archivo_informe, fordatdep % (datdep))
for x in range(0, count):
	contenido_linea2 = (
		array_departamentos[x][0],array_array[x][0],array_array[x][1],	
	)
	formato_linea2 = "\t%s %s \t%s\n "
	escribir_linea_archivo(nombre_archivo_informe, formato_linea2 % (contenido_linea2))

guardar_procesos("archivo informe.txt cerrado")
guardar_procesos("programa terminado, abrir archivo informe.txt y modernizacion.txt")