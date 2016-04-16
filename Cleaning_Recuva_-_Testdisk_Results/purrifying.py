"""
"""
import os, glob
import win32api
import ctypes

print("Changing current directions")
print("Searching for `TEMP_SAVE` drive")

#List drives letters
drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\000')[:-1]
kernel32 = ctypes.windll.kernel32
volumeNameBuffer = ctypes.create_unicode_buffer(1024)
fileSystemNameBuffer = ctypes.create_unicode_buffer(1024)
serial_number = None
max_component_length = None
file_system_flags = None

for drive in drives:

	rc = kernel32.GetVolumeInformationW(
	    ctypes.c_wchar_p(drive),
	    volumeNameBuffer,
	    ctypes.sizeof(volumeNameBuffer),
	    serial_number,
	    max_component_length,
	    file_system_flags,
	    fileSystemNameBuffer,
	    ctypes.sizeof(fileSystemNameBuffer)
	)

	if(volumeNameBuffer.value == "TEMP_SAVE"):
		path = drive
#Search the correct drive letter
os.chdir(path)

#List all files
print("Listing all files, could take some time")
glob_list = glob.glob(path+'**\\*.*',recursive = True) #python 3 code
sub_dir_list = [os.path.join(path,o) for o in os.listdir(path) if os.path.isdir(os.path.join(path,o))]
files_list = [x for x in glob_list if x not in sub_dir_list]

#List all extensions
exts = list(set(x.split('.')[-1] for x in files_list))

print("All extensions founds")
print(exts)

#Make a dict {ext:[file_list which have ext as an extensions]}
dict_ext = dict()

for ext in exts:
	dict_ext.update(({ext:[x for x in files_list if x.split('.')[-1] == ext]}))


#Good ones
filter_lower_case= [
			'avi',
			'mp4',
			'pdf',
			'doc',
			'docx',
			'xls',
			'xslx',
			'ppt',
			'pptx',
			'jpg',
			'png',
			'psd',
			'bmp',
			'ogg',
			'Ogg',
			'tiff',
			'tif',
			'csv',
			'flac',
			'wav',
			'ape',
			'ods',
			'odt',
			'tgz',
			'mkv',
			'cue',
			'eps',
			'mp3',
			'pgf',
			'svg',
			'm4a',
			'tgz',
			'odp',
			'Mp3',
			'wma',
			'Wma',
			'mat',
			'eml',
			'jpeg',
			'mpg',
			'mpeg'

		]
filter_upper_case= [x.upper() for x in filter_lower_case]
filter_ = filter_lower_case+filter_upper_case

#Filtered extensions
exts_filtered = [x for x in exts if x not in filter_]


char = ""
while(char.upper()!= 'N' and char.upper()!= 'Y'):
	char = input("\n Confirm Deletions? Y/N \n")
	if(char.upper() == 'Y'):
		for ext in exts_filtered:
			print("filtering the %s files" %ext)
			files = dict_ext[ext]
			for file in files:
				os.remove(file)
	elif(char.upper() == 'N'):
		print("Detetions aborted, exiting")
	else:
		print("Please type only Y or N")
