import time
import schedule
import os
import sys
import subprocess
cmd='rundll32.exe user32.dll, LockWorkStation'

import Paths_Credentials
import DD1
import DD2
import Functions
import Chrome_navigator
import Reports_automation
import Cyberduck


def BNED_DD(driver):
    # Define DD_update file save path
    Credentials = Paths_Credentials.Path()
    # Get Verba Connect username and password
    Credentials = Paths_Credentials.Verba_Credentials(Credentials=Credentials)
    # Download adoption and enrollment files
    adoption_files_path, enrollment_files_path, Warning = Cyberduck.get_new_old_files()
    # Lock screen
    print('Locking Screen')
    subprocess.call(cmd)
    # Save console prints to Reports file
    sys.stdout = Functions.Logger(Credentials)
    # DD1: adoptions and enrollments file comparison
    Old_ad_file, New_ad_file, DD_update, date = DD1.run(adoption_files_path=adoption_files_path,
                                                        enrollment_files_path=enrollment_files_path,
                                                        Credentials=Credentials)
    # Save Report File
    sys.stdout.close()
    # Save console prints to Reports file
    sys.stdout = Functions.Logger(Credentials)
    # Ask for schools and catalogs to leave out of online check and get report
    DD_update, schools_catalogs_report, reports_folder_path = Reports_automation.get_reports(driver=driver, DD_update=DD_update)
    # Wait for Slurpee to finish before checking
    Functions.wait_slurpee(DD_update=DD_update)
    # Save Report File
    sys.stdout.close()
    # DD2: Validate changes in Connect
    DD_update = DD2.run(Credentials=Credentials, DD_update=DD_update, driver=driver)
    # Save DD2_update file without report cases
    sys.stdout = Functions.Logger(Credentials)
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
    sys.stdout = Functions.Logger(Credentials)
    # Re check "No logical reason cases"
    print('No Logical Reason Cases: {}\n'
          'Cleared'.format(len(DD_update.loc[DD_update['Reason change not made'] == 'No Logical Reason'])))
    DD_update['Change made in Connect?'].loc[DD_update['Reason change not made'] == 'No Logical Reason'] = float(
        'nan')
    DD_update['Reason change not made'].loc[DD_update['Reason change not made'] == 'No Logical Reason'] = float(
        'nan')
    # Save Report File
    sys.stdout.close()
    # Re run online check on missing report cases
    DD_update = DD2.run(Credentials=Credentials, DD_update=DD_update, driver=driver)
    # Save console prints to Reports file
    sys.stdout = Functions.Logger(Credentials)
    # Save DD2_update final file (overwrites the first one)
    Functions.save_DD2(DD_update=DD_update, Credentials=Credentials, date=date)
    # print warning about downloaded files if necessary
    if Warning:
        print(Warning)
    # Save Report File
    sys.stdout.close()
    # Close driver
    driver.close()
    # Change dir to main path
    os.chdir(Credentials['main_path'])
    # Hibernate after 5 minutes
    # time.sleep(5 * 60)
    # os.system("shutdown.exe /h")

# Log in to connect first to solve captcha
# Define DD_update file save path
Credentials = Paths_Credentials.Path()
# Get Verba Connect username and password
Credentials = Paths_Credentials.Verba_Credentials(Credentials=Credentials)
# Open Chrome and log in to Verba Connect
driver = Chrome_navigator.verba_connect_login(Credentials=Credentials)

# Define run days and times
schedule.every().monday.at("02:35").do(BNED_DD, driver)
schedule.every().tuesday.at("02:35").do(BNED_DD, driver)
schedule.every().wednesday.at("02:35").do(BNED_DD, driver)
schedule.every().thursday.at("02:35").do(BNED_DD, driver)
schedule.every().friday.at("02:35").do(BNED_DD, driver)

# Run every day
while True:
    out = schedule.run_pending()
    time.sleep(60*10)