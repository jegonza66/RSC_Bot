import time
import schedule
import os
import sys
import subprocess
import pandas as pd
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
cmd='rundll32.exe user32.dll, LockWorkStation'

import Paths_Credentials
import DD1
import DD2
import Functions
import Chrome_navigator
import Reports_automation
import Cyberduck
import AMS_tracker


def AMS_Track():
    # Get AMS username, passwrod and Tasks.xlsx file path
    Credentials = AMS_tracker.paths()
    # Login AMS
    print('Login to AMS')
    driver = AMS_tracker.login_ams(Credentials['AMS_Username'], Credentials['AMS_Password'])
    # read excel with tasks
    print('Load AMS_tasks.xlsx file')
    excel_tasks = pd.read_excel(Credentials['AMS_Tasks_filepath'], sheet_name="Tasks")
    excel_tasks["note"] = excel_tasks["note"].fillna("N/A")
    days_list = excel_tasks["day"].unique()
    # Track tasks
    print('Tracking hours')
    AMS_tracker.Track(driver=driver, days_list=days_list, excel_tasks=excel_tasks)
    # Close AMS driver
    driver.close()
    print('Hours tracked successfully')


def BNED_DD(driver, Credentials):
    # Download adoption and enrollment files
    adoption_files_path, enrollment_files_path, Warning = Cyberduck.get_new_old_files(Credentials=Credentials)
    # DD1: adoptions and enrollments file comparison
    Old_ad_file, New_ad_file, DD_update, date = DD1.run(adoption_files_path=adoption_files_path,
                                                        enrollment_files_path=enrollment_files_path,
                                                        Credentials=Credentials)
    # Save Report File
    sys.stdout.close()
    # Save console prints to Reports file
    sys.stdout = Functions.Logger(Credentials, date)
    # Ask for schools and catalogs to leave out of online check and get report
    DD_update, schools_catalogs_report, reports_folder_path = Reports_automation.get_reports(driver=driver, DD_update=DD_update)
    # Wait for Slurpee to finish before checking
    Functions.wait_slurpee(DD_update=DD_update)
    # Save Report File
    sys.stdout.close()
    # DD2: Validate changes in Connect
    DD_update = DD2.run(Credentials=Credentials, DD_update=DD_update, driver=driver)
    # Save DD2_update file without report cases
    sys.stdout = Functions.Logger(Credentials, date)
    Functions.save_DD2(DD_update=DD_update, Credentials=Credentials, date=date)
    # If decided to ask reports before
    if schools_catalogs_report != {}:
        # Ask if reports recieved and make files comparison
        DD_update, Reports = Reports_automation.compare_reports(DD_update=DD_update, reports_folder_path=reports_folder_path)
        # Save Report File
        sys.stdout.close()
        # Re run online check on missing report cases and No logical reason
        DD_update = DD2.run(Credentials=Credentials, DD_update=DD_update, driver=driver)
    # Save console prints to Reports file
    sys.stdout = Functions.Logger(Credentials, date)
    # Re check "No logical reason cases"
    Functions.wipe_no_logical_cases(DD_update=DD_update)
    # Save Report File
    sys.stdout.close()
    # Re run online check on missing report cases
    DD_update = DD2.run(Credentials=Credentials, DD_update=DD_update, driver=driver)
    # Save console prints to Reports file
    sys.stdout = Functions.Logger(Credentials, date)
    # Save DD2_update final file (overwrites the first one)
    Functions.save_DD2(DD_update=DD_update, Credentials=Credentials, date=date)
    # print warning about downloaded files if necessary
    if Warning:
        print(Warning)
    # Save Report File
    sys.stdout.close()
    # Change dir to main path
    os.chdir(Credentials['main_path'])


# Log in to connect first to solve captcha
# Get DD_update file save path Verba Connect username and password and Cyberduck download paths
Credentials = Paths_Credentials.get()
# Open Chrome and log in to Verba Connect
driver = Chrome_navigator.verba_connect_login(Credentials=Credentials)

# Define run days and times
schedule.every().monday.at("00:01").do(AMS_Track)
schedule.every().monday.at("00:05").do(BNED_DD, driver, Credentials)
schedule.every().tuesday.at("00:05").do(BNED_DD, driver, Credentials)
schedule.every().wednesday.at("00:05").do(BNED_DD, driver, Credentials)
schedule.every().thursday.at("00:05").do(BNED_DD, driver, Credentials)
schedule.every().friday.at("00:05").do(BNED_DD, driver, Credentials)

# Run every day
while True:
    out = schedule.run_pending()
    time.sleep(60*10)