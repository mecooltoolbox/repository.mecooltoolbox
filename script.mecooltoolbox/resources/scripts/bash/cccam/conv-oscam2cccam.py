#!/usr/bin/python
# -*- coding:utf-8 -*-

def leer(archivo):
    return open(archivo,'r').read()
def escribir(archivo,datos):
    open(archivo,'w').write(datos)
    
def oscam2cccam(archivo):
    estruct_cccam = "C: {} {} {} {}"
    cccam=''
    c = 0
    with open(archivo) as f:
        for line in f:
            linea = line.strip().split("=")
            if linea[0].strip() == "device":
                device = linea[1].strip()
                c=c+1
            if linea[0].strip() == "user":
                usuario = linea[1].strip()
                c=c+1
            if linea[0].strip() == "password":
                contr = linea[1].strip()
                c=c+1
        
            if c == 3:
                device = device.split(",")
                if len(device) == 2:
                    servidor = device[0]
                    puerto = device[1]
                #print( 'Servidor: '+servidor+'\nPuerto: '+puerto+'\nUsuario: '+usuario+'\nContraseña: '+contr+'\n' ) # debug
                cccam = cccam + estruct_cccam.format( servidor,puerto,usuario,contr ) + '\n'
                c=0
    return cccam.strip()

escribir( "cccam.cfg",oscam2cccam("oscam.server") )
