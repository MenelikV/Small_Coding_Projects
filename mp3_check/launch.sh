#!/bin/bash
DIR=~/Musik
printf "Scanned Directory\n"
echo $DIR
#Maybe a bt useless
if [[ -f log.log ]]; then
  rm log.log
  #statements
fi
touch log.log
#Recurisive and global search
shopt -s globstar
for file in $DIR/**/*.mp3; do
  #echo -e $file
  mp3val -f -llog.log $file
done;
for file in $DIR/**/*.bak; do
  echo -e ${file%.*}
  rm $file
  rm ${file%.*}
  printf "Incorrect mp3 found, $file \n" >> log.log
done;
