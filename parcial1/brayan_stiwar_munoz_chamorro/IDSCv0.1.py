# IDSCv0.1
# Desarrollado Brayan Stiwar Munoz
# Septiembre 16 de 2015
'''
Programa que recorre los departamentos de colombia identificando las industrias que en estos se encuentran 
analizando con esto si se encuentran las industrias necesarias para que un departamento sea desarrollado y 
asi generar un listado de departamentos subdesarrollados en colombia 
'''
import sys
import os, os.path
import re
cantidad_minima_de_archivos=1
directorio_a_revisar=os.getcwd()+"\\departamentos"
extension_por_defecto=".txt"
industria="industria" + extension_por_defecto


def guardar_error(mensaje_error):
	escribir_linea_archivo(nombre_archivo_errores, "\n" + mensaje_error + "\n")

def crear(nombre_archivo):
	try: 
		archivo=open(nombre_archivo,'w')
		archivo.close
	except: 
		error("Error creando archivo" + nombre_archivo + "!")
		return False
	return True

def escribir_linea_archivo(nombre_archivo, linea_a_escribir):	
	try:
		archivo = open(nombre_archivo, 'a')
		archivo.write(linea_a_escribir)
		archivo.close()
	except IOError:
		guardar_error("Error escribiendo linea " + linea_a_escribir + " en archivo " + nombre_archivo + "!")
		return False
		
	return True

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
	
def leer_lineas_archivo(nombre_archivo):
	lineas = ()
	try:
		archivo = open(nombre_archivo, 'r')
		lineas = archivo.readlines()
		archivo.close()
	except IOError:
		guardar_error("Error leyendo archivo " + nombre_archivo + "!")
	return lineas 
	
def validar_tipo_numerico(valor_string):	
	try:
		numerico = int(valor_string)
		return True		
	except ValueError:	
		guardar_error("Valor" + valor_string + " no puede convertirse a tipo numerico!")		
		return False



crear("revision.txt")
crear("subdesarrollado.txt")
m=[]
if validar_archivo(industria) and validar_archivo("obligatorias.txt"):
        industria=leer_lineas_archivo(industria)
        obligatorias=leer_lineas_archivo("obligatorias.txt")
        sub=[]
        r=[]
        pob=[]
        nombres=[]
        capital=[]
        for i in range(len(obligatorias)):
                numeros=""
                for i in obligatorias[i]:
                        if re.match("\d",i):
                                numeros += i
                sub.append(numeros)
        if (os.path.exists(directorio_a_revisar) and os.access(os.path.dirname(directorio_a_revisar), os.R_OK)):
                print ("Directorio " + directorio_a_revisar + " VALIDO!" )	
                cantidad_archivos_directorio = len([name for name in os.listdir(directorio_a_revisar)])
                
                if(cantidad_archivos_directorio >= cantidad_minima_de_archivos):
                        print ("Directorio contiene cantidad minima de archivos!")
                        dir_actual=os.getcwd()
                        os.chdir(directorio_a_revisar)
                        
                        for name in os.listdir(directorio_a_revisar):
                                        nombre_archivo = name
                                        a=leer_lineas_archivo(nombre_archivo)
                                        y=[]
                                        nombres.append(name[0:len(name)-4])
                                        capital.append(a[0])
                                        pob.append(a[1])
                                        q=[]
                                        for i in range(2,len(industria)+2):
                                            numeros=""
                                            z=i
                                            for i in a[i]:
                                                if re.match("\d",i):
                                                        numeros += i
                                                k=numeros
                                            q.append(int(numeros))
                                            if int(k)<int(sub[z-2]) and y!=name[0:len(name)-4]:
                                                    os.chdir(dir_actual)
                                                    escribir_linea_archivo("subdesarrollado.txt",name[0:len(name)-4]+"\n")
                                                    y=name[0:len(name)-4]
                                                    os.chdir(directorio_a_revisar)  
                                        if not m:
                                                m=q;
                                        else:
                                                for i in range(len(q)):
                                                       m[i]=int(q[i])+int(m[i])
                        os.chdir(dir_actual)
                        prom=[]
                        escribir_linea_archivo("revision.txt","PROMEDIOS" + "\n") 
                        for i in range(len(m)-1):
                                p=float(m[i])/len(os.listdir(directorio_a_revisar))
                                prom.append(p)
                                escribir_linea_archivo("revision.txt",industria[i][0:len(industria[i])-1] + "   " +str(p) + "\n")
                        p=float(m[len(m)-1])/len(os.listdir(directorio_a_revisar))
                        escribir_linea_archivo("revision.txt",industria[len(m)-1] + "   " +str(p) + "\n") 
                        escribir_linea_archivo("revision.txt","\n" + "DEPARTAMENTOS REVISADOS \n" )
                        for i in range(len(nombres)):
                                escribir_linea_archivo("revision.txt","Departamento: " +nombres[i]+"  Cap:  " + capital[i][0:len(capital[i])-1]+ "   Pob:" + pob[i])
        else:
                print("El directorio no existe")




                                        
                                                
                                        
else:
        print("El archivo industria no se encuentra")

print("El directorio de archivos esta directamente asociado a la carpeta departamentos")
os.system("pause")
raw_input("Press enter to continue")




		




