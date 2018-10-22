#!/bin/bash

subcarp="cccam"

###### COMUN EN SCRIPTS ##### 
cd $scripts_fcoaaron/$subcarp
. ../_commonfuncs
#############################

cartemp="/tmp/datos"

function normalizar {
	# Esta funcion se asegura que cada cline termina con "yes" al final
        grep -i "^C:.*" $1 > tmpclines
        rm -f $1
        while read cline
        do
                srv=$(echo $cline|cut -d" " -f2)
                port=$(echo $cline|cut -d" " -f3)
                usr=$(echo $cline|cut -d" " -f4)
                pass=$(echo $cline|cut -d" " -f5)
                newcline="C: "$srv" "$port" "$usr" "$pass" yes"
                echo $newcline >> $1
        done < tmpclines
        rm -f tmpclines
}

function importar {
    cp $cccamfn ./cccam.cfg &> /dev/null
    echo "Clines importadas!"
    return 0
}

function exportar {
    arch=$(find . -iname cccam.cfg)
    if [ ! -s "$arch" ]
    then
        echo "ERROR: No existe cccam.cfg para exportar"
        return 1
    fi
    normalizar $arch
    cp $arch $cccamfn &> /dev/null
    chown 1000:1000 $cccamfn
    chmod 600 $cccamfn
    echo "Clines exportadas!"
      #kodimsg "Listo!" "Las clines se han exportado correctamente."
    return 0
}

function borrar {
    if [ ! -s "$cccamfn" ]
    then
	#error "No hay clines en Android..."
	return 1
    fi

    echo "Eliminando..."
    rm -f $cccamfn &> /dev/null

    if [ ! -s "$cccamfn" ]
    then
        msg="Clines borradas de Android correctamente."
        echo $msg
        #kodimsg "Listo!" "$msg"
	return 0
    else
        #error "No se pudieron borrar las clines de Android..."
	return 2
    fi
}

mkdir $cartemp &> /dev/null
mount /dev/data $cartemp &> /dev/null

	carpcmp=$cartemp"/data/th.dtv/dtv_user_data"
	if [ -d "$carpcmp" ]
	then
		cccamfn=$cartemp"/data/th.dtv/dtv_user_data/CCCam.cfg" # Mecool Ki Pro
	else
		cccamfn=$cartemp"/data/th.dtv/CCCam.cfg" # Mecool Ki Plus
	fi

	case $1 in
		"import") res=importar ;;
		"export") res=exportar ;;
		"delete") res=borrar ;;
	esac

umount /dev/data
exit $res

# Potencialmente inseguro hasta que haya forma de comprobar que se realizo
# el desmontaje!!!
# 15/10/18: De todas formas, /tmp no deja de ser una carpeta temporal, por lo que carece de importancia borrar la carpeta
# rm -fR $cartemp
