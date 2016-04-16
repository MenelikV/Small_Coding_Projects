#!/bin/bash 

DIR=~/Musik
printf "Scanned Directory\n"
echo $DIR
if [[ -f flac-erros.txt ]]; then
	#statements
	rm flac-erros.txt
fi
touch flac-erros.txt
shopt -s globstar
#cd DIR
{
	for file in $DIR/**/*.flac; do
	flac -wst "$file" || (rm "$file" && printf "Bad flac file found, $file\n" >> flac-erros.txt)
done; 
} ||
{
	echo "finished"
}
