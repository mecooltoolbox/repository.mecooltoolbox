# -*- coding:utf-8 -*-

import xbmc,xbmcgui,xbmcvfs,subprocess

dlg = xbmcgui.Dialog()
sel = dlg.select
noti = dlg.notification
msgyn = dlg.yesno
msg = dlg.ok
txview = dlg.textviewer
bs = dlg.browseSingle
input = dlg.input

# Nombres de los servicios, por si alguna vez cambiaran...
oscamsrv="service.softcam.oscam"
tvhsrv="service.tvheadend42"

def iplocal(): return xbmc.getInfoLabel('Network.IPAddress')
def macaddr(): return xbmc.getInfoLabel('Network.MacAddress')
def cputemp(): return xbmc.getInfoLabel('System.CPUTemperature')

def bash( archivo,args ):
	cmd = "sh '"+archivo+"'"
	for i in args:
		cmd = cmd+" '"+i+"'"
	try:
		res = subprocess.check_output(cmd, shell=True)
		return res
	except subprocess.CalledProcessError as err:
		return str(err.returncode)

def comando( cmd ):
	try:
		res = subprocess.check_output(cmd, shell=True)
		return res
	except subprocess.CalledProcessError as err:
		return str(err.returncode)

# info del método: https://askubuntu.com/questions/95910/command-for-determining-my-public-ip
def ipexterna(): return comando("curl -w '\n' ident.me").strip()

def servicio_activo(srvname): return True if comando("systemctl is-active "+srvname).strip()=="active" else False
def servicio_reiniciar(srvname): comando("systemctl restart "+srvname)
def servicio_parar(srvname): comando("systemctl stop "+srvname)

# adaptación a python de la función getmacaddr del script bash _commonfuncs
# ejemplo de uso: mac_eth = getmacaddr("eth0",1)
def getmacaddr( iface,removecolons ):
	commonfuncs = "/storage/.kodi/addons/script.mecooltoolbox/resources/scripts/bash/_commonfuncs"
	cmd = ". {}; getmacaddr {} {}".format( commonfuncs,iface,"true" if removecolons else "false" )
	return subprocess.check_output(cmd+"; exit 0", shell=True).strip()

def KodiOcupado(estado):
	xbmc.executebuiltin("ActivateWindow(busydialog)") if estado else xbmc.executebuiltin("Dialog.Close(busydialog)")

def chooseDirectory():
	fpath = xbmcgui.Dialog().browseSingle(3,'','files')
	if not fpath: return None
	return fpath

def Kodi_Leer(archivo):
	arch = xbmcvfs.File(archivo)
	tx = arch.read()
	arch.close()
	return tx

def Kodi_Escribir(archivo,datos):
	arch = xbmcvfs.File(archivo,'w')
	res = arch.write(datos)
	arch.close()
	return res

def Kodi_TamanoArchivo(archivo):
	arch = xbmcvfs.File(archivo)
	tam = arch.size()
	arch.close()
	return tam


def Kodi_Copiar(origen,destino):
	xbmcvfs.copy(origen,destino)
def Kodi_Borrar(archivo):
	xbmcvfs.delete(archivo)

def hashmd5(arch):
	return comando("md5sum "+arch).strip().split(" ")[0]