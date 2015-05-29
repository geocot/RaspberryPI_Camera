#!/bin/bash

#Contantes
N=0

echo "Efface le répertoire"
./Dropbox-Uploader/dropbox_uploader.sh delete /raspimage
./Dropbox-Uploader/dropbox_uploader.sh mkdir /raspimage

while true;do

	echo "Prend une image"

	raspistill -rot 180 -o capture.jpg 

	echo "resize image"
	convert capture.jpg -resize 1280x1024 capture_resize.jpg

	echo "script Python"
	python TemperatureActuelle.py

	echo "Lit le fichier"
	read temperature < Temperature.txt	

	echo "Ajout de la date"
	convert capture_resize.jpg -font /usr/share/fonts/truetype/droid/DroidSans.ttf \
	   -fill white -stroke black \
	   -pointsize 30 -gravity NorthWest -annotate 0 "Date: %[EXIF:DateTime] \n$temperature" image$N.jpg

	echo "Efface les images sur le bureau"
	rm capture.jpg
	rm capture_resize.jpg

	echo "Met sur dropbox"
	
	./Dropbox-Uploader/dropbox_uploader.sh upload image$N.jpg /raspimage
	echo "Efface image"

	rm image$N.jpg 
	N=$(($N+1))
	echo "Je dors"
	sleep $1
	
	if [ $N -eq $2 ]
	 then
	 	echo "Efface le répertoire"
		./Dropbox-Uploader/dropbox_uploader.sh delete /raspimage
		./Dropbox-Uploader/dropbox_uploader.sh mkdir /raspimage
		N=0
	fi

done