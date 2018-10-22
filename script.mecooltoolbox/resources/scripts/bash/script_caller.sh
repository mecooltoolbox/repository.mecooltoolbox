#!/bin/sh

# Esto es ab-sur-do, pero no me quedaba otra si queria que corriera desde el addon...
# Más de media hora intentando averigüar por qué no se ejecutaba este script xD
. /storage/.kodi/addons/script.mecooltoolbox/resources/scripts/bash/_commonfuncs

cd $scripts_fcoaaron

case $1 in
	"android2oscam")
		cd cccam
			sh cccam-android.sh import
			sh cccam-oscam.sh import
		rm -f oscam.server cccam.cfg &> /dev/null
	;;
	"oscam2android")
		cd cccam
			sh cccam-oscam.sh export
			sh cccam-android.sh export
		rm -f oscam.server cccam.cfg &> /dev/null
	;;
	"file2oscam")
		cd cccam
			cp /tmp/cccam.cfg ./
			sh cccam-oscam.sh import
		rm -f /tmp/cccam.cfg oscam.server cccam.cfg &> /dev/null
	;;
	"oscam2file")
		cd cccam
			rm -f /tmp/cccam.cfg
			sh cccam-oscam.sh export
			cp -f cccam.cfg /tmp
		rm -f oscam.server cccam.cfg &> /dev/null
	;;
	"borrarclines-android") sh cccam/cccam-android.sh delete ;;
	"borrarclines-oscam") sh cccam/cccam-oscam.sh delete ;;
	"updatefromnet") sh cccam/camupg.sh ;;
	"reiniciar-oscam")
		reiniciar oscam
		#kodimsg "Hecho!" "Servidor OSCam reiniciado."
	;;
esac
