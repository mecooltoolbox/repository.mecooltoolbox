#!/usr/bin/env python
# -*- coding:utf-8 -*-

from funcionescomunes import *
from oscam_toolbox_funcs import *

def main():

	def menu():

		# La versatilidad de python cada vez me asombra más, se pueden poner IFs hasta para establecer variables! toma ya...
		# Descubierto mientras buscaba cómo demonios hacer el IF en una línea xD
		oscamstat = "Iniciado" if servicio_activo(oscamsrv) else "Parado"
		tvhstat = "Iniciado" if servicio_activo(tvhsrv) else "Parado"

		opts = [
		"*** OSCAM ***", #0
		"Estado : "+oscamstat, #1
		"Reiniciar OSCam", #2
		"Parar OSCam", #3
		"----------------------------", #4
		"Backup", #5
		"Restaurar", #6
		"----------------------------", #7
		"", #8
		"*** TVHEADEND ***", #9
		"Estado : "+tvhstat, #10
		"Reiniciar TvHeadend", #11
		"Parar TvHeadend", #12
		"", #13
		"Reiniciar Kodi"] #14

		return sel("Gestor de servicios",opts)

	# Esto ejecutará el menú en bucle hasta que el usuario decida salir dando a Cancelar o al botón atrás, momento en que se cumplirá que res es -1
	res=0
	while res != -1:

		res = menu()

		if res == 2: servicio_reiniciar(oscamsrv); msg("Hecho!","OSCam reiniciado!")
		if res == 3: servicio_parar(oscamsrv); msg("Hecho!","OSCam parado!")

		if res == 5: oscam_backup() # Backup de OSCam
		if res == 6: oscam_restore() # Restaurar backup de OSCam

		if res == 11: servicio_reiniciar(tvhsrv); msg("Hecho!","TvHeadend reiniciado!")
		if res == 12: servicio_parar(tvhsrv); msg("Hecho!","TvHeadend parado!")

		if res == 14:
			if msgyn("Confirmación","Esto hará un reinicio suave de Kodi, por lo que la pantalla se pondrá en negro por unos segundos, quiere continuar?") == 1:
				servicio_reiniciar("kodi")