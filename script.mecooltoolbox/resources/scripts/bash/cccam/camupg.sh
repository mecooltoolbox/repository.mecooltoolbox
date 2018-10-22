#!/bin/bash

subcarp="cccam"

###### COMUN EN SCRIPTS #####
cd $scripts_fcoaaron/$subcarp
. ../_commonfuncs
#############################

cfgfn="camupg_config.txt"

cfg="/storage/.kodi/userdata/$cfgfn"
cfgt=$cfgfn.template

if [ ! -s "$cfg" ]; then
	[ ! -s $cfgt ] && exit 1
	cp -f $cfgt $cfg
	msg="Se ha creado el archivo $cfgfn en Userdata, por favor editalo para poner tus datos."
	echo $msg
	# kodimsg "INFO" "$msg"
	exit 2
fi

git_usuario=$(readparam $cfg git_usuario)
git_proyecto=$(readparam $cfg git_proyecto)
git_branch=$(readparam $cfg git_branch)

ftp_url=$(readparam $cfg ftp_url)
ftp_user=$(readparam $cfg ftp_usuario)
ftp_pass=$(readparam $cfg ftp_password)
ftp_port=$(readparam $cfg ftp_puerto)

modo_arch=$(readparam $cfg MODO)
key=$(readparam $cfg KEY)

if [ -z "$modo_arch" ] || [ -z "$key" ] || [ -z "$git_usuario" ] || [ -z "$git_proyecto" ] || [ -z "$git_branch" ] || [ -z "$ftp_url" ] || [ -z "$ftp_user" ] || [ -z "$ftp_pass" ] || [ -z "$ftp_port" ]; then
	# error "Falta algún parámetro en $cfg"
	exit 3
fi

case $modo_arch in
	"GIT") modo="git" ;;
	"FTP") modo="ftp" ;;
	*) exit 4 ;;
esac

zip_pass=$key

arch="cccam.zip" # archivo zip temporal
subcarpeta="cam" # carpeta en el servidor donde se encuentran las subcarpetas nombradas con la MAC ethernet

function get_git {
	URL="https://raw.githubusercontent.com/$git_usuario/$git_proyecto/$git_branch/$subcarpeta/$mac_eth/$mac_eth.zip"
	#URL="https://github.com/$git_usuario/$git_proyecto/blob/$git_branch/$subcarpeta/$mac_eth/$mac_eth.zip?raw=true"
	wget -qO $arch $URL &> /dev/null
}
function get_ftp {
	ftpget -u $ftp_user -p $ftp_pass -P $ftp_port $ftp_url $arch /$subcarpeta/$mac_eth/$mac_eth.zip &> /dev/null
}

mac_eth=$(getmacaddr eth0 true)
mac_wifi=$(getmacaddr wlan0 true)

[ "$zip_pass" = "<wifimac>" ] && password=$mac_wifi || password=$zip_pass

rm -f $arch
case $modo in
	"ftp") get_ftp ;;
	"git") get_git ;;
esac
[ ! -s $arch ] && exit 5

unzip -qqP $password $arch
fn="$mac_eth.cam" # archivo que deberia existir si todo sale bien...
[ ! -s $fn ] && rm -f $arch && exit 6
rm -f $arch
mv -f $fn cccam.cfg

sum_nuevo=$(sumonly cccam.cfg)
sum_viejo=$(cat cccam.sum)

if [ "$sum_nuevo" = "$sum_viejo" ]; then
	# error "No hay clines nuevas..."
	exit 7
else
	sh cccam-oscam.sh import # deberia controlar si falla algo aqui jaja
	echo $sum_nuevo > cccam.sum

	msg="Clines actualizadas correctamente :)" # o eso espero xD
	echo "$msg"
	# kodimsg "Listo!" "$msg"
	exit 0
fi

rm -f cccam.cfg
