from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import pickle
import os


# ----------------------------------------------------------------------------------------------------------------------
def paths(Credentials_file='Credentials/Credentials.pkl'):
    try:
        f = open(Credentials_file, 'rb')
        Credentials = pickle.load(f)
        f.close()
        Credentials = ams_credentials(Credentials=Credentials)
    except:
        Credentials = {}
        Credentials = ams_credentials(Credentials=Credentials)
        os.makedirs('Credentials', exist_ok=True)
        f = open(Credentials_file, 'wb')
        pickle.dump(Credentials, f)
        f.close()

    return Credentials


def ams_credentials(Credentials, Credentials_file='Credentials/Credentials.pkl'):
    try:
        Credentials['AMS_Username'] and Credentials['AMS_Password'] and Credentials['AMS_Tasks_filepath']
        return Credentials
    except:
        print('No AMS Connect Credentials found. Please Enter your username and password.\n')
        Credentials['AMS_Username'] = input('Username:')
        Credentials['AMS_Password'] = input('Password:')
        Credentials['AMS_Tasks_filepath'] = input(
            'Please copy and paste the path to the AMS_Tasks file.\nPath:').replace('\\', '/')
        # Save Verba credentials in Credentials file
        f = open(Credentials_file, 'wb')
        pickle.dump(Credentials, f)
        f.close()

    return Credentials


# ----------------------------------------------------------------------------------------------------------------------

def login_ams(username, password):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://ams.gfolkdev.net/')

    id_box = driver.find_element(By.ID, 'provider_user_email')
    id_box.send_keys(username)

    pass_box = driver.find_element(By.ID, 'provider_user_password')
    pass_box.send_keys(password)

    login_button_css = 'input[type="submit"]'
    login_button = driver.find_element(By.CSS_SELECTOR, login_button_css)
    login_button.click()

    driver.maximize_window()

    return driver


def upload_tasks(driver, tasks_to_upload):
    for index, row in tasks_to_upload.iterrows():
        # upload client
        select_client = Select(driver.find_element(By.ID, 'time_entry_client_id'))
        select_client.select_by_visible_text(row.client)

        # upload project
        select_project = Select(driver.find_element(By.ID, 'time_entry_project_id'))
        select_project.select_by_visible_text(row.project)

        # upload task
        select_task = Select(driver.find_element(By.ID, 'time_entry_service_id'))
        select_task.select_by_visible_text(row.task)

        # upload note
        notes_box = driver.find_element(By.ID, 'time_entry_notes')
        notes_box.send_keys(row.note)

        # upload start date
        start_time = driver.find_element(By.ID, 'time_entry_start_time')
        start_time.send_keys(row.start_date)

        # upload end date
        end_time = driver.find_element(By.ID, 'time_entry_end_time')
        end_time.send_keys(row.end_date + "\ue007")
        time.sleep(1)



def get_date_by_name(name):
    today = datetime.today()

    # get the 1° day of the week
    start_date_week = today - timedelta(days=today.weekday())

    # dictionary to calculate all days depending on first day of the week
    days_of_week = {"Monday": start_date_week,
                    "Tuesday": start_date_week + timedelta(1),
                    "Wednesday": start_date_week + timedelta(2),
                    "Thursday": start_date_week + timedelta(3),
                    "Friday": start_date_week + timedelta(4),
                    "Saturday": start_date_week + timedelta(5),
                    "Sunday": start_date_week + timedelta(6)
                    }

    # return date depending on the day's name
    try:
        date_by_name = days_of_week[name]
        date_by_name = date_by_name.strftime('%Y/%m/%d')
    except:
        raise ValueError("The day name wasn't recognized")

    return date_by_name


def Track(driver, days_list, excel_tasks):
    # upload entries of all week
    for day in days_list:
        # upload day by day
        tasks_to_upload = excel_tasks[excel_tasks["day"] == day]
        date_to_enter = get_date_by_name(day)

        # get in day's sheet
        time.sleep(1)
        day_box = driver.find_element(By.CSS_SELECTOR, f'div[data-day="{date_to_enter}"]')
        day_box.click()

        # get list of inputs
        list_inputs = driver.find_elements(By.XPATH, "//tr[@data-time-entries-table-target='timeEntries']")

        # check if there is any input in AMS before updating tasks
        if list_inputs:
            raise ValueError(f'The sheet of {day} is not empty')

        # input tasks
        upload_tasks(driver, tasks_to_upload)