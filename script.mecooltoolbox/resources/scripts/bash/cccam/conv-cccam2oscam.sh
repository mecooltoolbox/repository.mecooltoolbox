#!/bin/bash

# Cambio 18/12/17 : Mejorado con strings multi-lineas gracias a lo descrito aqui:
# https://stackoverflow.com/questions/23929235/multi-line-string-with-extra-space-preserved-indentation

cccam=$(find . -iname cccam.cfg -type f | head -1) # asi no tenemos que preocuparnos por las mayusculas jeje
if [ ! -s "$cccam" ]
then
  echo "No se encontro el archivo cccam.cfg a convertir..."
  exit
fi

oscamfn="oscam.server"
oscamparams="/storage/.kodi/userdata/oscam_params.txt"

if [ ! -s "$oscamparams" ]
then
	echo "Creando oscam_params.txt con parametros por defecto..." 
#	cat > $oscamparams <<- EOM
#		inactivitytimeout             = 30
#		group                         = 1
#		emmcache                      = 1,3,2,0
#		blockemm-unknown              = 1
#		blockemm-u                    = 1
#		blockemm-s                    = 1
#		blockemm-g                    = 1
#		cccversion                    = 2.3.0
#		cccmaxhops                    = 4
#		ccckeepalive                  = 1
#	EOM
	# el addon tiene un oscam_params.txt con unos parametros por defecto,
	# si el usuario no ha creado sus propios parametros en /storage/.kodi/userdata/,
	# copiamos los del addon.
	cp -f oscam_params.txt $oscamparams
fi

delim=" "
c=0

rm -f $oscamfn
echo "Generando "$oscamfn"..."

grep -i "^C:.*" $cccam > tmpclines
while read cline
do
	servidor=$(echo $cline|cut -d"$delim" -f2)
	puerto=$(echo $cline|cut -d"$delim" -f3)
	usuario=$(echo $cline|cut -d"$delim" -f4)
	pass=$(echo $cline|cut -d"$delim" -f5)

	c=$(($c+1))
	cat >> $oscamfn <<- EOM
		[reader]
		label = CCCAM_$c
		protocol = cccam
		device = $servidor,$puerto
		user = $usuario
		password = $pass
		$(cat $oscamparams)

	EOM
done < tmpclines
rm -f tmpclines

echo "Listo!"
