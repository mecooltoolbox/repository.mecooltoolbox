#!/usr/bin/env python
# -*- coding:utf-8 -*-

import xbmcaddon
ADDON = xbmcaddon.Addon()
addon_name = ADDON.getAddonInfo('name')

from modulos.funcionescomunes import *
from modulos.oscam_toolbox_funcs import *

import modulos.gestor_servicios

def menu(): # Super-menú xD

	opts = [
	"*** Gestor clines OSCam ***", # 0
	"Importar clines", #1
	"Exportar clines", #2
	"Borrar clines", #3
	"Editor de clines", #4
	"", #5
	"*** Lista M3U ***", #6
	"Configurar parámetros de lista remota",#7
	"Generar lista M3U local",#8
	"Generar lista M3U remota",#9
	"",#10
	"Gestor de servicios", #11
	"Información del sistema", #12
	"", #13
	"Añadir reinicio Android a Aeon Nox"] #14

	return sel(addon_name,opts)

# Esto ejecutará el menú en bucle hasta que el usuario decida salir dando a Cancelar o al botón atrás, momento en que se cumplirá que res es -1
res=0
while res != -1:
	res = menu()

	if res == 1:
		dlgimp_opts = ["Desde Archivo","Desde Android"]
		dlgimp_res = 0
		while dlgimp_res != -1:
			dlgimp_res = sel("Importar clines",dlgimp_opts)
			if dlgimp_res == 0: file2oscam() # Importar de Archivo a OSCam
			if dlgimp_res == 1: android2oscam()  # Importar desde Android

	if res == 2:
		dlgexp_opts = ["Hacia Archivo","Hacia Android"]
		dlgexp_res = 0
		while dlgexp_res != -1:
			dlgexp_res = sel("Exportar clines",dlgexp_opts)
			if dlgexp_res == 0: oscam2file() # Exportar de OSCam a Archivo
			if dlgexp_res == 1: oscam2android() # Exportar hacia Android

	if res == 3:
		dlgborr_opts = ["Clines de OSCam","Clines de Android"]
		dlgborr_res = 0
		while dlgborr_res != -1:
			dlgborr_res = sel("Borrar clines",dlgborr_opts)
			if dlgborr_res == 0: borrar_clines_oscam() # Borrar clines de OSCam
			if dlgborr_res == 1: borrar_clines_android() # Borrar clines de Android

	if res == 4: editor_clines()

	if res == 7: config_m3u_params()
	if res == 8: generar_m3u_local()
	if res == 9: generar_m3u_remoto()

	if res == 11: modulos.gestor_servicios.main() # Llamamos directamente al otro script, en el que englobé todo su código en la función main :)
	if res == 12: info()

	if res == 14: aeon_androidopts()
else:
	exit()
