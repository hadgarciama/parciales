#careasy_droid v1.0
#desarrollado por Carlos Manuel Montoya
#SEPTIEMBRE 17 DE 2015
'''
este programa lo que hace es verificar un directorio donde esta el numero de animales por especie en cada barrio 
y si el numero de animales por especie sobrepasa a el numero especificado se genera un archivo de ayuda donde dice 
el nombre de los barrios a los cuales se enviara la ayuda de droids para los animales
'''
import os
import sys
nombre_archivo_errores = "errores.txt"
nombre_archivo_registro = "procedimiento_realizado_por_programa.txt"
nombre_archivo_ayuda = "ayuda.txt"
nombre_archivo_reporte = "reporte.txt"
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
# Funcion que guarda un registro de operacion en el archivo procedimiento_realizado_por_programa.txt
def guardar_procedimiento_realizado_por_programa(mensaje_registro):
	escribir_linea_archivo(nombre_archivo_registro, "\n" + mensaje_registro + "\n")
def terminar_programa(mensaje_terminacion):
	guardar_error(mensaje_terminacion)
	guardar_procedimiento_realizado_por_programa("el programa se finalizo por un error para mas detalles mire en errores.")
	
	# Terminar el programa
	sys.exit()
def escribir_linea_archivo(nombre_archivo, linea_a_escribir):	
	try:
		archivo = open(nombre_archivo, 'a')
		archivo.write(linea_a_escribir)
		archivo.close()
	except IOError:
		guardar_error("Tiene Un Error Escribiendo Linea " + linea_a_escribir + " en archivo " + nombre_archivo + "!")
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
	array_resultado = [0 for x in range(2)]
	
	# Separar la linea por el simbolo (tREALIZADOen) *
	arreglo_campos = linea_por_validar.split("*")	
	array_resultado[0]=arreglo_campos[0]
	# Validar que el campo sea de tipo numerico
	try:
		animales_condiciones = int(arreglo_campos[1])								
		array_resultado[1] = animales_condiciones
	except ValueError:
		guardar_error(arreglo_campos[1] + " no se puede convertir a entero!")
		return array_resultado
	return array_resultado
# Crear el archivo errores.txt para almacenar los errores que se presenten.
crear_archivo("errores.txt")
# Crear el archivo procedimiento_realizado_por_programa.txt para almacenar el registro de operacion del programa.
crear_archivo("procedimiento_realizado_por_programa.txt")
guardar_procedimiento_realizado_por_programa("se crearon los archivos errore.txt y procedimiento_realizado_por_programa.txt")
program_path = os.getcwd()
revision = sys.argv[1]
especies_analizar = sys.argv[2]
condiciones = sys.argv[3]
if (sys.argv[2].endswith(".txt") == False):
	terminar_programa("El archivo especies_analizar no tiene extension .txt que es la requerida!")
else:
	guardar_procedimiento_realizado_por_programa("Extension de archivo de especies_analizar REALIZADO")
	
if (sys.argv[3].endswith(".txt") == False):
	terminar_programa("El archivo condiciones no tiene extension .txt que es la requerida!")
else:
	guardar_procedimiento_realizado_por_programa("Extension de archivo de condiciones REALIZADO")
leido_especies_analizar=tuple(leer_lineas_archivo(especies_analizar))
num_rec=len(leido_especies_analizar)
guardar_procedimiento_realizado_por_programa("archivo especies_analizar leido REALIZADO")
leido_condiciones=tuple(leer_lineas_archivo(condiciones))
num_condiciones=len(leido_condiciones)
guardar_procedimiento_realizado_por_programa("archivo condiciones leido REALIZADO")
if(num_condiciones!=num_rec and num_condiciones==num_min):
	terminar_programa("Los archivos condiciones y especies_analizar no tienen el mismo numero de lineas o igual al numero de animales")
else:
	guardar_procedimiento_realizado_por_programa("archivos con igual numero de lineas e igual al numero de animales")
array_condiciones = [[columnas for columnas in range(2)] for filas in range(num_condiciones)]
guardar_procedimiento_realizado_por_programa("......Cargando condiciones en procesador....");
for x in range(0, num_condiciones):
	linea_validada = validar_linea(leido_condiciones[x], x+1)
	guardar_procedimiento_realizado_por_programa("Procesando linea " + str(x+1));
	array_condiciones[x][0] = linea_validada[0]
	array_condiciones[x][1] = linea_validada[1]
guardar_procedimiento_realizado_por_programa("condiciones cargada en procesador!");
count=directory(sys.argv[1],'.txt')
if(count==0):
	terminar_programa("no hay archivos validos en el directorio")
i=0
mal=[[columnas for columnas in range(1)] for filas in range(100)]
array_barrios = [[columnas for columnas in range(1)] for filas in range(count)]
rootDir = revision
for dirName, subdirList, fileList in os.walk(rootDir):
 
    for fname in fileList:
		if(fname.endswith('.txt')):
			array_barrios[i][0] = fname
		else:
			mal[i][0]=fname
			i=i-1
		if(i!=(count-1)):
			i=i+1
guardar_procedimiento_realizado_por_programa("se encontro el directorio");
guardar_procedimiento_realizado_por_programa("contanto archivos con extension '.txt' en el directorio")
guardar_procedimiento_realizado_por_programa("archivos REALIZADO contados y listados")
guardar_procedimiento_realizado_por_programa("procesando informacion del directorio")
guardar_procedimiento_realizado_por_programa("si no se continua el texto leer archivo errores.txt y procedimiento_realizado_por_programa.txt en el directorio")
os.chdir(revision)
array_array = [[columnas for columnas in range(6)] for filas in range(count)]
for x in range(0,count):
	array_array[x]=tuple(leer_lineas_archivo(array_barrios[x][0]))
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
guardar_procedimiento_realizado_por_programa("informacion del directorio procesada");
guardar_procedimiento_realizado_por_programa("creando array array_suma");
array_suma = [[columnas for columnas in range(1)] for filas in range(4)]
guardar_procedimiento_realizado_por_programa("sumando animales")
k=0	
while (k<4):
	for x in range(1,count+1):
		array_suma[k][0]+=int(array_validado[x][k])
	k=k+1
guardar_procedimiento_realizado_por_programa("animales sumados guardados y listados")
array_prom = [[columnas for columnas in range(1)] for filas in range(4)]
for x in range (0,4):
	array_prom[x][0]=array_suma[x][0]/count
guardar_procedimiento_realizado_por_programa("animales guardados y listados")
array_comparacion = [[columnas for columnas in range(4)] for filas in range(count)]
guardar_procedimiento_realizado_por_programa("comparando datos de animales de los archivos con la condiciones")
k=1
i=0
while (k<count+1):
	for x in range (0,4):
		array_comparacion[i][x]=array_validado[k][x]-array_condiciones[x][1]
	k=k+1
	i=i+1
guardar_procedimiento_realizado_por_programa("datos comparados guardados y listados")
guardar_procedimiento_realizado_por_programa("archivo ayuda.txt creado y en ejecucion")
crear_archivo("ayuda.txt")
i=0
while (i<count-1):
	for x in range(0, 1):
		if(array_comparacion[i][x]>0 and array_comparacion[i][x+1]>0 and array_comparacion[i][x+2]>0 and array_comparacion[i][x+3]):
			escribir_linea_archivo(nombre_archivo_ayuda, array_barrios[i][0] + "\n")	
		i=i+1
guardar_procedimiento_realizado_por_programa("archivo ayuda.txt cerrado")
crear_archivo("reporte.txt")
guardar_procedimiento_realizado_por_programa("archivo reporte.txt creado y en ejecucion")
totales=str('TOTALES')
fortotales="%s\n\n"
escribir_linea_archivo(nombre_archivo_reporte, fortotales % (totales))
for x in range (0,4):
	contenido_linea1 = ( 
		array_condiciones[x][0], array_suma[x][0],
	)
	formato_linea1 = "\t%s %d\n\n"
	escribir_linea_archivo(nombre_archivo_reporte, formato_linea1 % (contenido_linea1))
promedio=str('PROMEDIO'),
forprom="%s\n\n"
escribir_linea_archivo(nombre_archivo_reporte, forprom % (promedio))		
for x in range (0,4):
	contenido_linea1 = (	
		array_condiciones[x][0], array_prom[x][0],
	)
	formato_linea1 = "\t%s %d\n\n"
	escribir_linea_archivo(nombre_archivo_reporte, formato_linea1 % (contenido_linea1))
datlun=str('DATOS barrios'),
fordatlun="%s\n\n"
escribir_linea_archivo(nombre_archivo_reporte, fordatlun % (datlun))
for x in range(0, count):
	contenido_linea2 = (
		array_barrios[x][0],array_array[x][0],array_array[x][1],	
	)
	formato_linea2 = "\t%s %s \t%s\n "
	escribir_linea_archivo(nombre_archivo_reporte, formato_linea2 % (contenido_linea2))
guardar_procedimiento_realizado_por_programa("archivo reporte.txt cerrado")
guardar_procedimiento_realizado_por_programa("programa terminado, abrir archivo reporte.txt y ayuda.txt")