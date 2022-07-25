import Paths_Credentials
import DD1
import DD2
import Functions
import Chrome_navigator
import Reports_automation

import sys
import os


# Get DD_update file save path Verba Connect username and password and Cyberduck download paths
Credentials = Paths_Credentials.get()
# Get Files
adoption_files_path, enrollment_files_path, Warning = Functions.get_files(Credentials=Credentials)
# # Save console prints to Reports file
# sys.stdout = Functions.Logger(Credentials=Credentials, date=date)
# DD1: adoptions and enrollments file comparison
Old_ad_file, New_ad_file, DD_update, date = DD1.run(adoption_files_path=adoption_files_path,
                                                    enrollment_files_path=enrollment_files_path,
                                                    Credentials=Credentials)
# Save Report File
sys.stdout.close()
# Save console prints to Reports file
sys.stdout = Functions.Logger(Credentials=Credentials, date=date)
# Open Chrome and log in to Verba Connect
driver = Chrome_navigator.verba_connect_login(Credentials=Credentials)
# Ask for schools and catalogs to leave out of online check and get report
DD_update, schools_catalogs_report, reports_folder_path = Reports_automation.get_reports(driver=driver, DD_update=DD_update)
# Wait for Slurpee to finish before checking
Functions.wait_slurpee(DD_update=DD_update)
# Save Report File
sys.stdout.close()
# DD2: Validate changes in Connect
DD_update = DD2.run(Credentials=Credentials, DD_update=DD_update, driver=driver, date=date)
# Save DD2_update file without report cases
sys.stdout = Functions.Logger(Credentials=Credentials, date=date)
# Functions.save_DD2(DD_update=DD_update, Credentials=Credentials, date=date)
# If decided to ask reports before
if schools_catalogs_report != {}:
    # Ask if reports recieved and make files comparison
    DD_update, Reports = Reports_automation.compare_reports(DD_update=DD_update, reports_folder_path=reports_folder_path)
    # Save Report File
    sys.stdout.close()
    # Re run online check on missing report cases
    DD_update = DD2.run(Credentials=Credentials, DD_update=DD_update, driver=driver)
# Save console prints to Reports file
sys.stdout = Functions.Logger(Credentials=Credentials, date=date)
# Re check "No logical reason cases"
Functions.wipe_no_logical_cases(DD_update=DD_update)
# Save Report File
sys.stdout.close()
# Re run online check on missing report cases
DD_update = DD2.run(Credentials=Credentials, DD_update=DD_update, driver=driver)
sys.stdout = Functions.Logger(Credentials=Credentials, date=date)
# Save DD2_update final file (overwrites the other)
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
