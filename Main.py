import time

import Paths_Credentials
import DD1
import DD2
import Functions
import Chrome_navigator
import Reports_automation
import Cyberduck

import schedule
import os

def DD1():
    # Define DD_update file save path
    Credentials = Paths_Credentials.Path()

    # Get Verba Connect username and password
    Credentials = Paths_Credentials.Verba_Credentials(Credentials=Credentials)

    # Download adoption and enrollment files
    adoption_files_path, enrollment_files_path = Cyberduck.get_new_old_files()

    # DD1: adoptions and enrollments file comparison
    Old_ad_file, New_ad_file, DD_update, date = DD1.run(adoption_files_path=adoption_files_path,
                                                        enrollment_files_path=enrollment_files_path,
                                                        Credentials=Credentials)

    # Open Chrome and log in to Verba Connect
    driver = Chrome_navigator.verba_connect_login(Credentials=Credentials)

    # Ask for schools and catalogs to leave out of online check and get report
    DD_update, schools_catalogs_report, reports_folder_path = Reports_automation.get_reports(driver=driver, DD_update=DD_update)

    # Wait for Slurpee to finish before checking
    Functions.wait_slurpee(DD_update=DD_update)

    # DD2: Validate changes in Connect
    DD_update = DD2.run(DD_update=DD_update, driver=driver)

    # Save DD2_update file without report cases
    Functions.save_DD2(DD_update=DD_update, Credentials=Credentials, date=date)

    # Re check "No logical reason cases"
    print('No Logical Reason Cases: {}\n'
          'Cleared'.format(len(DD_update.loc[DD_update['Reason change not made'] == 'No Logical Reason'])))
    DD_update['Change made in Connect?'].loc[DD_update['Reason change not made'] == 'No Logical Reason'] = float('nan')
    DD_update['Reason change not made'].loc[DD_update['Reason change not made'] == 'No Logical Reason'] = float('nan')

    # If decided to ask reports before
    if schools_catalogs_report != {}:
        # Ask if reports recieved and make files comparison
        DD_update, Reports = Reports_automation.compare_reports(DD_update=DD_update, reports_folder_path=reports_folder_path)

    # Re run online check on missing report cases and No logical reason
    DD_update = DD2.run(DD_update=DD_update, driver=driver)

    # Save DD2_update final file (overwrites the other)
    Functions.save_DD2(DD_update=DD_update, Credentials=Credentials, date=date)

    time.sleep(60)
    os.system("shutdown.exe /h")

schedule.every().monday.at("23:00").do(DD1)
schedule.every().tuesday.at("23:00").do(DD1)
schedule.every().wednesday.at("23:00").do(DD1)
schedule.every().thursday.at("23:00").do(DD1)
schedule.every().friday.at("23:00").do(DD1)

while True:
    schedule.run_pending()
    time.sleep(60*30)
