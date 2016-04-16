#!/usr/bin/env python
"""
"""
import glob, os, sys
import subprocess
import logging
from os.path import expanduser
home = expanduser("~")

#dir = os.path.join(home,'Musik')
dir = '/media/menelou/2CA28991A2896066/Music'

log_file = 'log.log'
if(os.path.isfile(log_file)):
    os.remove(log_file)
logger = logging.getLogger('launch.py')
hdlr = logging.FileHandler('log.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

logging.info('Removing files detected by mp3val')
logging.info('log to ' + log_file)


logging.info('mp3val Call')
mp3_files = glob.glob(dir+'/**/*.mp3')
for file in mp3_files:
    subprocess.call(["mp3val",'-f','-llog.log',file])

bad_files = glob.glob(dir+'/**/*.bak')

for file in bad_files:
    os.remove(file)
    os.remove(file[:-4])
    logging.info('removing %s' %(file))

logging.info('%d files removed' %(len(bad_files)))

logging.info('Renaming conforming to Windows')

for file in mp3_files:
    os.rename(file,file.replace('?',''))
