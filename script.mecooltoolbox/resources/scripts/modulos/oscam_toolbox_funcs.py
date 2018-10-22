#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time,os,datetime,xbmcgui
from funcionescomunes import *

scripts_fcoaaron = "/storage/.kodi/addons/script.mecooltoolbox/resources/scripts/bash"
callersh = scripts_fcoaaron+"/script_caller.sh"
#txview("debug",callersh)

def check_lenand():
	# TODO: mejorar la detección de Android, pues con dual-boot aún sería posible que funcionaran las opciones
	return True if comando( "mount | grep /dev/system" ).strip() != "" else False


def android2oscam():
	if check_lenand():
		msg("ERROR","Se está utilizando LibreElec/CoreElec desde la NAND! Esta función no hará nada...")
		return

	if msgyn("Confirmación","Importar las clines desde Android?") == 1: bash( callersh, ['android2oscam'] )

def oscam2android():
	if check_lenand():
		msg("ERROR","Se está utilizando LibreElec/CoreElec desde la NAND! Esta función no hará nada...")
		return

	if msgyn("Confirmación","Exportar las clines hacia Android?") == 1: bash( callersh, ['oscam2android'] )

def borrar_clines_android():
	if check_lenand():
		msg("ERROR","Se está utilizando LibreElec/CoreElec desde la NAND! Esta función no hará nada...")
		return

	if msgyn( "Confirmación","Desea borrar las clines de Android?" ) == 1:
		noti( "Script","Borrando clines de Android..." )
		bash( callersh, ['borrarclines-android'] )

def file2oscam():
	fn = bs( 1, 'Seleccionar archivo de clines', 'files', '.cfg|.txt', False, False )
	if fn:
		Kodi_Copiar( fn,'/tmp/cccam.cfg' )
		bash( callersh,['file2oscam'] )
	else:
		msg( "Error","No ha seleccionado ningún archivo." )
	return

def oscam2file():
	carp = chooseDirectory()
	if carp:
		bash( callersh,['oscam2file'] )
		time.sleep(1)
		fn = input("Nombre del archivo", "CCcam.cfg").strip()
		if fn:
			Kodi_Copiar( '/tmp/cccam.cfg',carp+fn )
			msg( "Hecho!","Clines exportadas a la carpeta destino!" )
		else:
			msg( "ERROR","No ha especificado nombre de archivo..." )
		time.sleep(1)
		Kodi_Borrar( '/tmp/cccam.cfg' )
	else:
		msg( "ERROR","No ha elegido carpeta de destino..." )
	return

def borrar_clines_oscam():
	if msgyn( "Confirmación","Desea borrar las clines de OSCam?" ) == 1:
		noti( "Script","Borrando clines de OSCam..." )
		bash( callersh, ['borrarclines-oscam'] )
	return

def oscam_backup():
	rutaoscam = "/storage/.kodi/userdata/addon_data/service.softcam.oscam"
	if os.path.isdir(rutaoscam):
		carp = chooseDirectory()
		if carp:
			def_fn = "Oscam-%s.tar.gz" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
			fn = input("Nombre del archivo TAR", def_fn).strip()
			if fn:
				tmpfn = "/tmp/oscam.tar"
				comando("systemctl stop service.softcam.oscam")
				comando( "tar -cz %s -f %s" % (rutaoscam,tmpfn) )
				time.sleep(1)
				comando("systemctl restart service.softcam.oscam")
				Kodi_Copiar(tmpfn,carp+fn)
				Kodi_Borrar(tmpfn)
				msg( "Hecho!","Backup de OSCam finalizado!" )
			else:
				msg( "ERROR","No ha especificado nombre de archivo..." )
		else:
			msg( "ERROR","No ha elegido carpeta de destino..." )
	else:
		msg("ERROR","No se encuentra la configuración de OSCam")
	return

def oscam_restore():
	rutaoscam = "/storage/.kodi/userdata/addon_data/service.softcam.oscam"
	fn = bs( 1, 'Seleccionar archivo TAR del backup', 'files', '.tar.gz', False, False )
	if fn:
		tmpfn = "/tmp/oscam.tar"
		Kodi_Copiar( fn,tmpfn )

		comando("systemctl stop service.softcam.oscam")
		comando( "rm -fR "+rutaoscam )
		time.sleep(1)
		comando( "tar -xf %s -C /" % tmpfn )
		time.sleep(1)
		comando("systemctl restart service.softcam.oscam")

		Kodi_Borrar( tmpfn )
		msg( "Hecho!","Restauración del backup de OSCam finalizada!" )
	else:
		msg( "Error","No ha seleccionado ningún archivo." )
	return

def info():
	opts = "Temperatura CPU: {}\n\nIP Local: {}\nIP Externa: {}\nMAC: {}".format( cputemp(),iplocal(),ipexterna(),macaddr() ).split("\n")
	res = 0
	while res != -1: res = sel("Información",opts)

def editor_clines():
	tmpfn = "/tmp/cccam.cfg"
	bash( callersh,['oscam2file'] ) # Generamos el CCcam.cfg desde OSCam en /tmp, para visualizarlo y editarlo

	clines_orig = Kodi_Leer(tmpfn) # Leemos las clines
	clines = clines_orig+"\n\n\n\n\n" # añadimos un par de ellas vacías por si queremos añadir nuevas
	clines = clines.split('\n') # creamos un array (lista) temporal que iremos editando, además de que el menú requiere que sea así y no un string
	
	msg("Info","Se va a abrir el editor de clines. Para cambiar una cline, pulsa sobre ella y haz los cambios en el cuadro. Para salir del editor, pulsa en Cancelar o bien en el botón que usas habitualmente para volver atrás en Kodi, en ese momento se escribirán todos los cambios y se reiniciará OSCam.")
	cn = 0 # Para que el while no salte de entrada

	# Se abrirá el editor de clines en bucle mientras se elija una cline para editar,
	# cuando se termine el selector devolverá -1 y ahí es cuando procesamos los cambios y los guardamos
	while cn != -1:
		cn = sel("Editor de clines",clines)
		if cn != -1: clines[cn] = input("Editar cline",clines[cn]) # si se pinchó en alguna cline, la podemos editar
	
	clinesnuevas = ""
	c = 0
	for i in clines:
		 # Con el IF nos aseguramos que no es una línea vacía, así de paso eliminamos
		# las clines extras vacías que añadimos si finalmente no fueron utilizadas
		if i.strip(): clinesnuevas = clinesnuevas+"\n"+i; c=c+1
	clinesnuevas = clinesnuevas.strip()
	#txview( "debug",clinesnuevas+"\n\nTotal clines: "+str(c) ) # debug

	if clinesnuevas != clines_orig: # Si se hicieron cambios, los escribimos
		Kodi_Escribir( tmpfn,clinesnuevas ) # Escribimos los cambios al fichero temporal
		bash( callersh,['file2oscam'] ) # y el script bash lo convertirá a oscam.server y borrará el temporal
		comando("systemctl restart service.softcam.oscam") # Reiniciamos OSCam, aunque creo que el script ya lo hacía xD
		msg( "Cambios guardados","Se han escrito "+str(c)+" clines en OSCam!" )

	Kodi_Borrar( tmpfn ) # si no hay cambios, no se borraba el temporal, por lo que aquí me aseguro jeje

	return


def config_m3u_params():
	conf = "/storage/.kodi/userdata/IptvConfig.txt"
	if os.path.exists(conf):
		params_orig = Kodi_Leer(conf)
		params = params_orig.split("\n")
	else:
		params = "{}\n{}\n\n".format( ipexterna(),9981 ).split("\n")

	res = 0
	while res != -1:
		opts = """
			Dominio: (dns dinámico, IP conocida o escribe AUTO para autodetectar tu IP pública)
			{}
			Puerto:
			{}
			Usuario:	
			{}
			Contraseña:
			{}""".strip().replace(chr(9),'').format(params[0],params[1],params[2],params[3]).split("\n") # Eliminamos espacios vacíos, tabuladores por poner aquí el string multi-línea y creamos el array para el selector


		res = sel("Configurar parámetros lista M3U externa",opts)
		if res == 1: dom = input("Dominio",params[0]); params[0] = ipexterna() if dom == "AUTO" else dom
		if res == 3: params[1] = xbmcgui.Dialog().input("Puerto",params[1],type=xbmcgui.INPUT_NUMERIC).strip()
		if res == 5: params[2] = input("Usuario",params[2]).strip()
		if res == 7: params[3] = input("Contraseña",params[3]).strip()

	params[0] = params[0].strip()

	if params[0] and params[1] and params[2] and params[3]:
		params_nuevos = "{}\n{}\n{}\n{}".format(params[0],params[1],params[2],params[3]) # generamos los nuevos parámetros
		if params_nuevos != params_orig: # si hay cambios...
			Kodi_Escribir( conf, params_nuevos )
			msg("Hecho!","Parámetros guardados!")
	else:
		msg("ERROR","Falta algún parámetro, por lo que no se guardarán los cambios.")



def generar_m3u_local():
	if not servicio_activo(tvhsrv):
		msg("ERROR","El servicio de TvHeadend está parado")
		return

	carp = chooseDirectory()
	if carp:
		fn = input("Nombre del archivo de lista", "lista_local.m3u").strip()
		if fn:
			url = "http://%s:9981/playlist/channels.m3u" % iplocal()
			listalocal = comando("curl "+url)
			Kodi_Escribir( carp+fn,listalocal )
			msg("Hecho!","Lista M3U local generada!")
		else:
			msg( "ERROR","No ha especificado nombre de archivo..." )
	else:
		msg( "ERROR","No ha elegido carpeta de destino..." )

def generar_m3u_remoto():
	if not servicio_activo(tvhsrv):
		msg("ERROR","El servicio de TvHeadend está parado")
		return

	conf = "/storage/.kodi/userdata/IptvConfig.txt"
	if not os.path.exists(conf):
		msg("ERROR","No se han encontrado los parámetros, por favor configúralos primero.")
		return

	params = Kodi_Leer(conf).split("\n")

	carp = chooseDirectory()
	if carp:
		fn = input("Nombre del archivo de lista", "lista_remoto.m3u").strip()
		if fn:
			txorig = "%s:9981" % iplocal()
			txdest = "{}:{}@{}:{}".format(params[2],params[3],params[0],params[1])

			url = "http://%s/playlist/channels.m3u" % txorig
			listalocal = comando("curl "+url)
			listaremota = listalocal.replace( txorig,txdest )
			#txview("debug",listaremota)
			Kodi_Escribir( carp+fn,listaremota )
			msg("Hecho!","Lista M3U remota generada!")
		else:
			msg( "ERROR","No ha especificado nombre de archivo..." )
	else:
		msg( "ERROR","No ha elegido carpeta de destino..." )

def aeon_androidopts():
	carp = "/storage/.kodi/addons/script.mecooltoolbox/resources/otros/"

	aeoncarp = "/storage/.kodi/addons/skin.aeon.nox.5/"
	aeoncarpres = aeoncarp+"1080i/"

	fnxml_orig = carp+"DialogButtonMenu.xml"
	fnxml_dest = aeoncarpres+"DialogButtonMenu.xml"
	fnxml_destbak = fnxml_dest+".bak"

	fnscript_orig = carp+"rebootfromrecovery"
	fnscript_dest = "/storage/.kodi/userdata/rebootfromrecovery"

	if not os.path.isdir(aeoncarp):
		msg("Error","No se ha encontrado el skin Aeon Nox!")
		return

	sumorig = hashmd5(fnxml_orig)
	sumdest = hashmd5(fnxml_dest)
	if sumorig == sumdest:
		if os.path.exists(fnxml_destbak):
			res = msgyn("Info","Ya se ha modificado el menú anteriormente, pero hay una copia de seguridad de antes de la modificación, desea restaurarla?")
			if res == 1:
				Kodi_Borrar(fnxml_dest)
				Kodi_Copiar(fnxml_destbak,fnxml_dest)
				Kodi_Borrar(fnxml_destbak)
				Kodi_Borrar(fnscript_dest)
				xbmc.executebuiltin("ReloadSkin()")
				msg("Hecho!","Copia de seguridad restaurada!")
		else:
			msg("Error","Ya se ha modificado el menú anteriormente, y no existe copia de seguridad para la restauración... si lo desea, reinstale el skin")

		return

	res = msgyn("Info",'Esta opción añadirá las opciones "Reiniciar en Android" y "Reiniciar en Recovery" al menú de apagado del skin Aeon Nox, se hará un backup del menú actual, desea continuar?')
	if res == 1:
		Kodi_Copiar(fnxml_dest,fnxml_destbak) # Backup

		Kodi_Copiar(fnxml_orig,fnxml_dest)
		Kodi_Copiar(fnscript_orig,fnscript_dest)
		comando("chmod 755 "+fnscript_dest) # damos permisos de ejecución (rwxr-xr-x) por si las moscas jeje

		xbmc.executebuiltin("ReloadSkin()")
		msg("Hecho!","Opciones añadidas al skin!")


