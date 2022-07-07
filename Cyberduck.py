import time
import pyautogui
import os
import gzip
import shutil
from datetime import datetime
import subprocess


def download_files(Credentials):
    # Get screen resolution
    width, height = pyautogui.size()

    # Wake screen
    pyautogui.click(width/2, height/2)
    print('Wake screen')
    time.sleep(2)

    Cyberduck_exe = 'C:\Program Files\Cyberduck\Cyberduck.exe'
    Cyberduck = subprocess.Popen(Cyberduck_exe)
    # os.system('start explorer shell:appsfolder\iterate.Cyberduck')
    print('Cyberduck Open')
    time.sleep(20)

    # Open bned
    pyautogui.doubleClick(125 / 1920 * width, 200 / 1080 * height)
    print('BNED Open')
    time.sleep(7)

    # Open files
    pyautogui.doubleClick(62 / 1920 * width, 208 / 1080 * height)
    print('Files Open')
    time.sleep(5)

    # Open processed
    pyautogui.doubleClick(62 / 1920 * width, 208 / 1080 * height)
    print('Processed Open')
    time.sleep(20)

    pyautogui.click(100 / 1920 * width, 175 / 1080 * height)
    time.sleep(1)
    pyautogui.click(1785 / 1920 * width, 175 / 1080 * height)
    time.sleep(1)
    pyautogui.click(1785 / 1920 * width, 175 / 1080 * height)
    time.sleep(1)
    print('Sorted by Modified')

    # Download enrollment
    pyautogui.doubleClick(62 / 1920 * width, 208 / 1080 * height)
    print('Downloading enrollment')
    time.sleep(2)
    # Download adoption
    pyautogui.doubleClick(62 / 1920 * width, 228 / 1080 * height)
    print('Downloading adoption')
    time.sleep(60 * 1)

    # Close Cyberduck
    # pyautogui.click(1888 / 1920 * width, 22 / 1080 * height)
    # time.sleep(1)
    # pyautogui.click(800 / 1920 * width, 574 / 1080 * height)
    Cyberduck.terminate()
    print('Cyberduck Closed')

    # Check downloaded files
    file_date = datetime.today().date().strftime('%Y%m%d')
    downloads_dir = Credentials['adoption_enrollment_path' ] + 'Cyberduck'
    os.chdir(downloads_dir)
    Downloaded_files = filter(os.path.isfile, os.listdir(downloads_dir))
    Downloaded_files = [os.path.join(downloads_dir, f) for f in Downloaded_files if file_date in f]

    return Downloaded_files


def extract_move_files(Credentials):
    # Get downloaded files
    file_date = datetime.today().date().strftime('%Y%m%d')
    files_dir = Credentials['adoption_enrollment_path']
    downloads_dir = files_dir + 'Cyberduck'
    os.chdir(downloads_dir)
    files = filter(os.path.isfile, os.listdir(downloads_dir))
    files = [os.path.join(downloads_dir, f) for f in files if file_date in f]  # add path to each file
    print('Downloaded files:\n'
          '{}'.format('\n'.join(str(file) for file in files)))

    # Extract gz downloads
    print('Extracting files...')
    for file in files:
        with gzip.open(file, 'rb') as f_in:
            with open(file.split('.gz')[0], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(file)
        print(file)

    # get extracted files
    Extracted_files = filter(os.path.isfile, os.listdir(downloads_dir))
    Extracted_files = [os.path.join(downloads_dir, f) for f in Extracted_files if file_date in f and 'gz' not in f] # add path to each file

    # Move files to adoptions and enrollments folder
    Moved_files = []
    print('Moving files to adoptions and enrollments folder.')
    for file in Extracted_files:
        try:
            shutil.move(file, files_dir)
            Moved_files.append(file)
            print(file)
        except:
            time.sleep(1)
            try:
                shutil.move(file, files_dir)
                Moved_files.append(file)
                print(file)
            except:
                pass

    return Extracted_files, Moved_files, file_date


def get_new_old_files(Credentials):
    Warning = False
    count = 0
    Downloaded_files = []
    Extracted_files = []
    Moved_files = []
    while (len(Downloaded_files) != 2 or len(Extracted_files) != 2 or len(Moved_files) != 2) and count < 5:
        count += 1
        if count > 1:
            print('Could not download and extract files properly. Retrying...')
        try:
            Downloaded_files = download_files(Credentials=Credentials)
            Extracted_files, Moved_files, file_date = extract_move_files(Credentials=Credentials)
            # if len(Downloaded_files) != 2 or len(Extracted_files) != 2 or len(Moved_files) != 2:
            #     Downloaded_files = download_files(Credentials=Credentials)
            #     Extracted_files, Moved_files, file_date = extract_move_files(Credentials=Credentials)
        except:
            continue

    if len(Extracted_files) != 2 or len(Moved_files) != 2:
        Warning = 'WARNING:\n' \
                  'Extracted files:\n' \
                  '{}\n' \
                  'Moved files:\n' \
                  '{}'.format('\n'.join(str(files) for files in Extracted_files), '\n'.join(str(files) for files in Moved_files))

    # get old and new files
    files_dir = Credentials['adoption_enrollment_path']
    os.chdir(files_dir)
    files = filter(os.path.isfile, os.listdir(files_dir))
    files = [os.path.join(files_dir, f) for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    files = files[-4:]

    # Check that the new files are among the files
    new_files_path = [file for file in files if file_date in file]
    adoption_files_path = [file for file in files if 'adoption' in file]
    enrollment_files_path = [file for file in files if 'enrollment' in file]

    if len(new_files_path) != 2 or len(enrollment_files_path) != 2 or len(adoption_files_path) != 2:
        print('Did not get the new files correctly. You are gonna have to do it manually...')
        adoption_files_path, enrollment_files_path = None, None

    return adoption_files_path, enrollment_files_path, Warning