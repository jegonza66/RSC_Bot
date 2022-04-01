import time
import pyautogui
import os
import gzip
import shutil
from datetime import datetime

def download_files():
    os.system('start explorer shell:appsfolder\iterate.Cyberduck')
    print('Cyberduck Open')
    time.sleep(10)

    # Open bned
    pyautogui.doubleClick(125, 200)
    print('BNED Open')
    time.sleep(5)

    # Open files
    pyautogui.doubleClick(62, 208)
    print('Files Open')
    time.sleep(5)

    # Open processed
    pyautogui.doubleClick(62, 208)
    print('Processed Open')
    time.sleep(20)

    # Download enrollment
    pyautogui.doubleClick(62, 208)
    print('Downloading enrollment')
    time.sleep(2)
    # Download adoption
    pyautogui.doubleClick(62, 228)
    print('Downloading adoption')
    time.sleep(60 * 1.5)


def extract_move_files():
    # Get downloaded files

    file_date = datetime.today().date().strftime('%Y%m%d')
    downloads_dir = 'C:/Users/joaco/Downloads'
    os.chdir(downloads_dir)
    files = filter(os.path.isfile, os.listdir(downloads_dir))
    files = [os.path.join(downloads_dir, f) for f in files if file_date in f] # add path to each file
    # files.sort(key=lambda x: os.path.getmtime(x))
    # files = files[-2:]

    # Extract gz downloads
    for file in files:
        with gzip.open(file, 'rb') as f_in:
            with open(file.split('.gz')[0], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    # get extracted files
    downloads_dir = 'C:/Users/joaco/Downloads'
    os.chdir(downloads_dir)
    files = filter(os.path.isfile, os.listdir(downloads_dir))
    files = [os.path.join(downloads_dir, f) for f in files if file_date in f and 'gz' not in f] # add path to each file
    # files.sort(key=lambda x: os.path.getmtime(x))
    # files = files[-2:]

    # Move files to adoptions and enrollments folder
    for file in files:
        shutil.move(file, r'C:\Users\joaco\Desktop\Joac\RSC-VitalSource\BNED DD\Files')

def get_new_old_files():
    try:
        download_files()
        extract_move_files()
        # get old and new files
        Files_dir = r'C:\Users\joaco\Desktop\Joac\RSC-VitalSource\BNED DD\Files'
        os.chdir(Files_dir)
        files = filter(os.path.isfile, os.listdir(Files_dir))
        files = [os.path.join(Files_dir, f) for f in files] # add path to each file
        files.sort(key=lambda x: os.path.getmtime(x))
        files = files[-4:]

        adoption_files_path = [file for file in files if 'adoption' in file]
        enrollment_files_path = [file for file in files if 'enrollment' in file]
    except:
        print('Could not download files. Pleas download them manually.')
        adoption_files_path, enrollment_files_path = None, None

    return adoption_files_path, enrollment_files_path