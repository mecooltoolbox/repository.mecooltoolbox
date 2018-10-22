#!/bin/bash

subcarp="cccam"

###### COMUN EN SCRIPTS ##### 
cd $scripts_fcoaaron/$subcarp
. ../_commonfuncs
#############################

oscamcfg="/storage/.kodi/userdata/addon_data/service.softcam.oscam/config/"

function importar {
        fn=$(find . -iname cccam.cfg)
        if [ ! -r "$fn" ] || [ ! -s "$fn" ] || [ -d "$fn" ]
        then
          # error "No se pudo abrir el archivo CCCam.cfg o bien esta vacio"
          return 1
        fi

	echo "Convirtiendo..."
	sh conv-cccam2oscam.sh
	rm -f cccam.cfg &> /dev/null

	fn="oscam.server"
	if [ ! -r "$fn" ] || [ ! -s "$fn" ]
	then
		  # error "Hubo algun problema en la conversion a formato OSCam..."
		  return 2
	fi

	echo "Copiando oscam.server al addon OSCam..."

	  mv -f oscam.server $oscamcfg"oscam.server.gen" &> /dev/null
	  cd $oscamcfg
	    mv -f oscam.server oscam.server.bak &> /dev/null
	    mv oscam.server.gen oscam.server
	    chmod 644 oscam.server
	    chown 1023:1023 oscam.server

	echo "Reiniciando OSCam..."
	  reiniciar oscam
	echo "Listo!"
	# kodimsg "Listo!" "Las clines se han importado correctamente."
	return 0
}

function exportar {
        fn=$oscamcfg"oscam.server"
        if [ ! -r "$fn" ] || [ ! -s "$fn" ] || [ -d "$fn" ]
        then
          # error "No hay clines en OSCam..."
          return 1
        fi

	echo "Convirtiendo..."
	
	cp -f $fn ./
	python conv-oscam2cccam.py
	rm -f oscam.server &> /dev/null

	fn="cccam.cfg"
	if [ ! -r "$fn" ] || [ ! -s "$fn" ]
	then
		 # error "Hubo algun problema en la conversion a formato CCcam..."
		  return 2
	fi

	echo "Listo!"
	# kodimsg "Listo!" "Las clines se han exportado correctamente."
	return 0
}

function borrar {
        fn=$oscamcfg"oscam.server"
        if [ ! -r "$fn" ] || [ ! -s "$fn" ] || [ -d "$fn" ]
        then
          # error "No hay clines en OSCam..."
          return 1
        fi

	rm -f $fn &> /dev/null
	rm -f $fn".bak" &> /dev/null
	reiniciar oscam

        if [ ! -r "$fn" ] || [ ! -s "$fn" ] || [ -d "$fn" ]
        then
          # kodimsg "Listo!" "Clines del OSCam borradas correctamente."
          return 0
	else
          # error "No se pudieron borrar las clines del OSCam..."
          return 2
        fi
}

case $1 in
	"import") res=importar ;;
	"export") res=exportar ;;
	"delete") res=borrar ;;
esac

exit $res