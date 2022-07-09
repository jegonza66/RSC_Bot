import pandas as pd
import os
import time
from datetime import datetime, timedelta
import sys
from func_timeout import FunctionTimedOut, func_timeout

import Cyberduck

def make_full_df(df):

    column_names = ['Date of Change (date of adoptions file of new data)', 'Type of Change', 'School', 'Catalog',
                    'Catalog Last End Date', 'Section', 'SKU', 'Previous Data', 'Section_new',
                    'Total Estimated Enrollments', 'SKU_new', 'Net Price', 'Student Price', 'Start Date', 'End Date',
                    'Change made in Connect?', 'Reason change not made', 'Issue',
                    'If New Schedule, are the key dates available?', 'New Item Work complete', 'Notes', 'Publisher',
                    'Issue with Tracker']

    full_df = pd.DataFrame(columns=column_names)

    for key in df.keys():
        full_df[key] = df[key]

    return full_df


def seasons_of_date(date):
    year = str(date.year)
    seasons = {'Spring': pd.date_range(start='21/03/' + year, end='20/06/' + year),
               'Summer': pd.date_range(start='21/06/' + year, end='22/09/' + year),
               'Fall': pd.date_range(start='23/09/' + year, end='20/12/' + year)}

    if date in seasons['Spring']:
        return 'Spring {}. Last end date {}'.format(year, date.strftime("%m/%d/%Y"))
    if date in seasons['Summer']:
        return 'Summer {}. Last end date {}'.format(year, date.strftime("%m/%d/%Y"))
    if date in seasons['Fall']:
        return 'Fall {}. Last end date {}'.format(year, date.strftime("%m/%d/%Y"))
    else:
        return 'Winter {}. Last end date {}'.format(year, date.strftime("%m/%d/%Y"))


def save_DD1(DD_update, Credentials, date):
    DD1_Save = DD_update.sort_values(['Type of Change', 'School', 'Catalog']).reset_index(drop=True)

    path_1 = Credentials['csv_save_path'] + 'DD1/'
    os.makedirs(path_1, exist_ok=True)
    file_name = path_1 + 'DD1 Update {}.xlsx'.format(date)
    DD1_Save.to_excel(file_name, index=False)
    print('\nDD1_update {} file saved to {}'.format(date, path_1))


def save_DD2(DD_update, Credentials, date):
    DD2_Save = DD_update.sort_values(['Type of Change', 'School', 'Catalog']).reset_index(drop=True)
    path_2 = Credentials['csv_save_path'] + 'DD2/'
    os.makedirs(path_2, exist_ok=True)
    file_name = path_2 + 'DD2 Update {}.xlsx'.format(date)
    DD2_Save.to_excel(file_name, index=False)
    print('\nDD2_update {} file saved to {}'.format(date, path_2))


def wait_slurpee(DD_update):
    missing_rows = DD_update['Change made in Connect?'].isna().sum() - \
                   len(DD_update.loc[(DD_update['Type of Change'] == 'new enrollment') &
                                     (DD_update['Change made in Connect?'] != 'Report')]) - \
                   len(DD_update.loc[(DD_update['Type of Change'] == 'deactivated enrollment') &
                                     (DD_update['Change made in Connect?'] != 'Report')]) - \
                   len(DD_update.loc[(DD_update['Type of Change'] == 'new schedule') &
                                     (DD_update['Change made in Connect?'] != 'Report')])
    hours = False
    while type(hours) != float:
        try:
            # Ask how much time to wait for slurpee. If no answer in five minutes wait 3 hs.
            try:
                hours = func_timeout(5 * 60, lambda: float(input('There are {} cases to be checked.\n'
                                'How much time (hours) would you like to wait before running the online check?'
                                '(so Slurpee can complete the changes).\n'
                                'Hours:'.format(missing_rows))))
            except FunctionTimedOut:
                hours = float(3)
        except ValueError:
            print("That's not an number!")
    if hours:
        print('Waiting until {} for Slurpee to finish changes before checking...'.
              format(format(datetime.now() + timedelta(hours=hours), '%H:%M:%S')))
    time.sleep(3600 * hours)


class Logger(object):
    def __init__(self, Credentials, date):
        save_path = Credentials['csv_save_path'] + 'Reports/'
        os.makedirs(save_path, exist_ok=True)
        file_date = datetime.strptime(date, '%d-%m-%Y')
        file_name = file_date.strftime(save_path + 'Report %Y_%m_%d.log')

        self.terminal = sys.stdout
        self.log = open(file_name, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass

    def close(self):
        self.log.close()
        sys.stdout = sys.stdout.terminal


def get_files(Credentials):
    Warning = False
    # Ask if automatically download files from cyberduck
    if Credentials['Verba_Username'] == 'joaquin.gonzalez':
        auto_cyberduck_download = input('Would you like to automatically download the files from cyberduck?')
        yes = {'yes', 'y', 'ye'}
        if auto_cyberduck_download in yes:
            # Download adoption and enrollment files
            adoption_files_path, enrollment_files_path, Warning = Cyberduck.get_new_old_files(Credentials=Credentials)
        else:
            adoption_files_path, enrollment_files_path = None, None
    else:
        adoption_files_path, enrollment_files_path = None, None
    return adoption_files_path, enrollment_files_path, Warning


def wipe_no_logical_cases(DD_update):
    print('No Logical Reason cases cleared: {}'
          .format(len(DD_update.loc[DD_update['Reason change not made'] == 'No Logical Reason'])))
    DD_update['Change made in Connect?'].loc[DD_update['Reason change not made'] == 'No Logical Reason'] = float(
        'nan')
    DD_update['Reason change not made'].loc[DD_update['Reason change not made'] == 'No Logical Reason'] = float(
        'nan')