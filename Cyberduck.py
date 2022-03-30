import time
import pyautogui
import os
import gzip
import shutil

def download_files():
    os.system('start explorer shell:appsfolder\iterate.Cyberduck')
    time.sleep(20)

    # Open bookmarks
    pyautogui.click(54, 150)

    # Open bned
    pyautogui.doubleClick(125, 200)
    time.sleep(10)

    # Open files
    pyautogui.doubleClick(62, 208)
    time.sleep(5)

    # Open processed
    pyautogui.doubleClick(62, 208)
    time.sleep(20)

    # Download enrollment
    pyautogui.doubleClick(62, 208)
    # Download adoption
    pyautogui.doubleClick(62, 228)
    time.sleep(60 * 2.5)


def extract_move_files():
    # Get downloaded files
    downloads_dir = 'C:/Users/joaco/Downloads'
    os.chdir(downloads_dir)
    files = filter(os.path.isfile, os.listdir(downloads_dir))
    files = [os.path.join(downloads_dir, f) for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    files = files[-2:]

    # Extract gz downloads
    for file in files:
        with gzip.open(file, 'rb') as f_in:
            with open(file.split('.gz')[0], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    # get extracted files
    downloads_dir = 'C:/Users/joaco/Downloads'
    os.chdir(downloads_dir)
    files = filter(os.path.isfile, os.listdir(downloads_dir))
    files = [os.path.join(downloads_dir, f) for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    files = files[-2:]

    # Move files to adoptions and enrollments folder
    for file in files:
        shutil.move(file, r'C:\Users\joaco\Desktop\Joac\RSC-VitalSource\BNED DD\Files')

def get_new_old_files():
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

    return adoption_files_path, enrollment_files_path