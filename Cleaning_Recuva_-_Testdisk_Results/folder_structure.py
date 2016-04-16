"""
"""
import os, glob
from purrifying import filter_lower_case
import win32api, ctypes

print("Changing current directions")
print("Searching for `TEMP_SAVE` drive")

#List drives letters
drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\000')[:-1]

#Search the correct drive letter
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

#Change CWD
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

#Filters for the new folder structure
audio_filter_lower = [
    'ogg',
    'mp3',
    'flac',
    'wav',
    'wma',
    'ape',
    'cue',
    'm4a',
    'Mp3',
    'Ogg',
]
video_filter_lower = [
    'mpeg',
    'mpg',
    'mkv',
    'mp4',
    'avi'
]
pic_filter_lower = [
    'psd',
    'jpeg',
    'jpg',
    'tif',
    'tiff',
    'png',
    'pgf',
    'svg',
    'bmp',

]
doc_filter_lower = [
    'doc',
    'docx',
    'xls',
    'xlsx',
    'pdf',
    'eml',
    'ppt',
    'pptx'
    'odp',
    'odt',
    'eps',
    'ods',
    ]

other_filter_lower = [x for x in exts if x not in (pic_filter_lower + video_filter_lower + doc_filter_lower + audio_filter_lower)]

audio_filter = audio_filter_lower + [x.upper() for x in audio_filter_lower]
video_filter = video_filter_lower + [x.upper() for x in video_filter_lower]
pic_filter = pic_filter_lower + [x.upper() for x in pic_filter_lower]
doc_filter = doc_filter_lower + [x.upper() for x in doc_filter_lower]
other_filter = other_filter_lower + [x.upper() for x in other_filter_lower]

filters = [audio_filter, video_filter, pic_filter, doc_filter, other_filter]

#Modifying folder structure to a flat, simpler structure (5 big folders only)
folder_structure = ['audio\\', 'video\\', 'pictures\\','documents\\','other\\']

#Creating folders
for dir in folder_structure:
    if not os.path.exists(path+dir):
        os.makedirs(path+dir)  

print("Restructering the drive")

for i, filter in enumerate(filters):
    files = [x for x in files_list if x.split('.')[-1] in filter]
    for file in files:
        filename = file.split('\\')[-1]#Windows Only
        try:
            os.rename(file, path + folder_structure[i] + filename)
        except Exception as e:
            try:
                print(e)
                os.remove(file)
            except Exception as ex:
                print(ex)


#Cleaning empty directories (not recursively)
print("Cleaning empty folders")

def find_empty_dirs(root_dir='.'):
    for dirpath, dirs, files in os.walk(root_dir):
        if not dirs and not files:
            yield dirpath

empty_dir = list(find_empty_dirs(path))
for dir in empty_dir:
    os.rmdir(dir)
