import glob
import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from func_timeout import FunctionTimedOut, func_timeout

import Chrome_navigator

def ask_if_leave_out(DD_update):
    # sort schools by cases number (considering only cases to do (not "No expected change" or enrollments/schedules)
    Schools = DD_update['Extra_id'].drop_duplicates()
    schools_catalogs_cases = []
    for School in Schools:
        Catalogs = DD_update[(DD_update['Extra_id'] == School)]['Catalog']
        for Catalog in Catalogs:
            schools_catalogs_cases.append((len(DD_update.loc[(DD_update['Extra_id'] == School) &
                                                             (DD_update['Catalog'] == Catalog) &
                                                             (DD_update['Change made in Connect?'] != 'No Expected Change') &
                                                             (DD_update['Type of Change'] != 'new enrollment') &
                                                             (DD_update['Type of Change'] != 'deactivated enrollment') &
                                                             (DD_update['Type of Change'] != 'new schedule')]),
                                           ' - '.join([str(School), str(Catalog)])))
    schools_catalogs_cases = list(dict.fromkeys(schools_catalogs_cases))
    schools_catalogs_cases.sort(reverse=True)
    num_schools_catalogs_cases = []
    for i, tup in enumerate(schools_catalogs_cases):
        num_schools_catalogs_cases.append((i+1, tup))
    num_schools_catalogs_cases.sort(reverse=True)

    missing_rows = DD_update['Change made in Connect?'].isna().sum() - \
                   (DD_update['Type of Change'] == 'new enrollment').sum() - \
                   (DD_update['Type of Change'] == 'deactivated enrollment').sum() - \
                   (DD_update['Type of Change'] == 'new schedule').sum()

    print('\nTotal number of cases: {}\n'
          'Number of cases to be checked: {}\n'
          '{}'.format(len(DD_update), missing_rows, '\n'.join(str(line) for line in num_schools_catalogs_cases)))

    # Ask if want to get reports for certain catalogs. If no answer in five minutes Answer is no.
    School_Catalog_num = False
    while type(School_Catalog_num) != int:
        try:
            School_Catalog_num = func_timeout(5 * 60, lambda: int(input('\nPlease enter the number of catalogs to ask for reports.')))
        except ValueError:
            print("That's not an number!")
        except FunctionTimedOut:
            print('No')
            School_Catalog_num = 0

    schools_catalogs_report = {}
    if School_Catalog_num:
        num = int(School_Catalog_num)
        num_schools_catalogs_cases.sort(reverse=False)
        for i in range(num):
            School_Catalog = schools_catalogs_cases[i][1]
            School, Catalog = School_Catalog.split(" - ")
            if School not in schools_catalogs_report.keys():
                schools_catalogs_report[School] = [Catalog]
            else:
                schools_catalogs_report[School].append(Catalog)

    return schools_catalogs_report


def request_reports(schools_catalogs_report, driver, DD_update):
    restart = False
    Schools = schools_catalogs_report.keys()
    for School in Schools:
        print('\n{}'.format(School))
        School_Selected = Chrome_navigator.verba_open_school(driver=driver, Verba_School=School)
        Catalogs = schools_catalogs_report[School]
        if School_Selected:
            for Catalog in Catalogs:
                print('{}'.format(Catalog))
                Catalog_Selected = Chrome_navigator.verba_open_catalog(driver=driver, Catalog=Catalog)
                if Catalog_Selected:
                    Asked_for_report = Chrome_navigator.verba_ask_report(driver=driver, tenant_id=School, Catalog=Catalog)
                    if Asked_for_report:
                        print('Report sent to your e-mail\n')
                    else:
                        Answer = input('\nCould not as for the report of {} - {}. Plese choose one of the following options:\n'
                                       '1. Would you like me to check those cases online?\n'
                                       '2. Would you like to re-enter the school and catalog name?'.format(School, Catalog))
                        if Answer == '1':
                            # sacar de la lista de catalogs
                            schools_catalogs_report[School].remove(Catalog)
                        elif Answer == '2':
                            restart = True
                            # sacar de la lista de catalogs
                            schools_catalogs_report[School].remove(Catalog)

                            empty = {'', ' '}
                            School_Catalog = input(
                                '\nPlease enter the Schools and Catalogs to exclude separated by " - " \n'
                                '(Example: School - Catalog -> "Enter")\n'
                                'If you are done entering Schools and Catalogs, just press "Enter":')

                            if School_Catalog not in empty:
                                School, Catalog = School_Catalog.split(" - ")
                                if School not in schools_catalogs_report.keys():
                                    schools_catalogs_report[School] = [Catalog]
                                else:
                                    schools_catalogs_report[School].append(Catalog)
                            break
                else:
                    Answer = input(
                        '\nCould not as for the report of {} - {}. Plese choose one of the following options:\n'
                        '1. Would you like me to check those cases online?\n'
                        '2. Would you like to re-enter the school and catalog name?'.format(School, Catalog))
                    if Answer == '1':
                        # sacar de la lista de catalogs
                        schools_catalogs_report[School].remove(Catalog)

                    elif Answer == '2':
                        restart = True
                        # sacar de la lista de catalogs
                        schools_catalogs_report[School].remove(Catalog)

                        empty = {'', ' '}
                        School_Catalog = input(
                            '\nPlease enter the Schools and Catalogs to exclude separated by " - " \n'
                            '(Example: School - Catalog -> "Enter")\n'
                            'If you are done entering Schools and Catalogs, just press "Enter":')

                        if School_Catalog not in empty:
                            School, Catalog = School_Catalog.split(" - ")
                            if School not in schools_catalogs_report.keys():
                                schools_catalogs_report[School] = [Catalog]
                            else:
                                schools_catalogs_report[School].append(Catalog)
                        break
        else:
            Answer = input(
                '\nCould not as for the reports of {}. Plese choose one of the following options:\n'
                '1. Would you like me to check those cases online?\n'
                '2. Would you like to re-enter the school and catalog name?'.format(School))
            if Answer == '1':
                # sacar de la lista de catalogs
                schools_catalogs_report.pop(School, None)

            elif Answer == '2':
                restart = True
                # sacar de la lista de catalogs
                schools_catalogs_report.pop(School, None)

                empty = {'', ' '}
                School_Catalog = 'Yes'
                while (School_Catalog not in empty):
                    School_Catalog = input('\nPlease enter the Schools and Catalogs to exclude separated by " - " \n'
                                           '(Example: School - Catalog -> "Enter")\n'
                                           'If you are done entering Schools and Catalogs, just press "Enter":')

                    if School_Catalog not in empty:
                        School, Catalog = School_Catalog.split(" - ")
                        if School not in schools_catalogs_report.keys():
                            schools_catalogs_report[School] = [Catalog]
                        else:
                            schools_catalogs_report[School].append(Catalog)
                break
    return DD_update, schools_catalogs_report, restart


def DD_update_drop_schools_catalogs_report(DD_update, schools_catalogs_report):

    Schools = schools_catalogs_report.keys()
    for School in Schools:
        Catalogs = schools_catalogs_report[School]
        for Catalog in Catalogs:
            indexNames = DD_update[(DD_update['Extra_id'] == School) & (DD_update['Catalog'] == Catalog) &
                                   (DD_update['Change made in Connect?'] != 'No Expected Change')].index
            DD_update['Change made in Connect?'][indexNames] = 'Report'

    return DD_update


def get_reports(driver, DD_update):
    schools_catalogs_report = ask_if_leave_out(DD_update=DD_update)
    restart = True
    while restart:
        DD_update, schools_catalogs_report, restart = request_reports(schools_catalogs_report=schools_catalogs_report,
                                                             driver=driver, DD_update=DD_update)
    DD_update = DD_update_drop_schools_catalogs_report(schools_catalogs_report=schools_catalogs_report, DD_update=DD_update)

    if schools_catalogs_report != {}:
        reports_folder_path = ''
        Answer = input('\nDid you recieved the reports on your email?\n'
                       'Please answer "yes" or "no":')
        yes = {'yes', 'y', 'ye'}
        while Answer in yes:
            print('\nPlease move all the Report files to one folder and use the file explorer to '
                  'select that folder.')
            root = tk.Tk()
            root.withdraw()
            reports_folder_path = filedialog.askdirectory()
            Answer = False
    else:
        reports_folder_path = ''
    return DD_update, schools_catalogs_report, reports_folder_path


def ask_if_got_reports(reports_folder_path):
    if reports_folder_path == '':
        Answer = input('\nDid you recieved the reports on your email?\n'
                       'Please answer "yes" or "no":')
    else:
        Answer = 'yes'
    yes = {'yes', 'y', 'ye'}
    Reports = False
    while Answer in yes:
        try:
            if reports_folder_path == '':
                print('\nPlease put all the reports in one folder and use the dialog window to select that folder.')
                root = tk.Tk()
                root.withdraw()
                reports_folder_path = filedialog.askdirectory()

            all_filenames = [i.replace('\\', '/') for i in glob.glob(os.path.join(reports_folder_path, '*.xlsx'))]
            Reports = pd.concat([pd.read_excel(f, sheet_name='Detail of Items with Sections', dtype='object',
                                               keep_default_na=False) for f in all_filenames])

            #Add new columns to Report
            Reports['catalog'] = Reports['Catalog Name/Term Name'].map(str) + '/-/' + Reports['Connect User'].map(str)
            Reports['course'] = Reports['Department'].map(str) + '/-/' + Reports['Course'].map(str) \
                                    + '/-/' + Reports['Section'].map(str) + '/-/' + Reports['catalog'].map(str)
            Reports['supercourse'] = Reports['course'].map(str) + '/-/' + Reports['Billing ISBN'].map(str)
            Reports['superconcat'] = Reports['supercourse'].map(str) + '/-/' + \
                                     Reports['Schedule Name'].str.split(' - ').str.join('/-/') + '/-/' + \
                                     Reports['Net Price'].map(str) + '/-/' + Reports['Student Price'].map(str)

            Reports = Reports.reset_index(drop=True)
            Answer = False
        except:
            Answer = input('\nCould not load the files in that folder.\n'
                           'Please enter "yes" to confirm you got the reports and got them all in one folder.')

    return Reports


def compare_reports(DD_update, reports_folder_path):
    Reports = ask_if_got_reports(reports_folder_path=reports_folder_path)
    if type(Reports) != bool:
        print('Running Reports comparison')
        DD_Report_cases = DD_update.loc[(DD_update['Change made in Connect?'] == 'Report') &
                                        (DD_update['Type of Change'] != 'new enrollment') &
                                        (DD_update['Type of Change'] != 'deactivated enrollment') &
                                        (DD_update['Type of Change'] != 'new schedule')]
        made_changes = DD_Report_cases['Extra_Superconcat'].loc[(DD_Report_cases['Type of Change'] != 'deactivated section') &
                                                                (DD_Report_cases['Type of Change'] != 'updated item')]\
            .isin(Reports['superconcat'].loc[(Reports['Section In A Group?'] == 'yes') & (Reports['Section Activated?'] == 'yes')])


        # Check deactivated sections
        made_changes_deactivated = ~DD_Report_cases['Extra_Superconcat'].loc[
            (DD_Report_cases['Type of Change'] == 'deactivated section')].isin(Reports['superconcat'].loc[
                      (Reports['Section In A Group?'] == 'yes') & (Reports['Section Activated?'] == 'yes')])

        DD_update['Change made in Connect?'][made_changes[made_changes == True].index] = 'Yes'
        DD_update['Change made in Connect?'][made_changes_deactivated[made_changes_deactivated == True].index] = 'Yes'
        DD_update['Change made in Connect?'].loc[DD_update['Change made in Connect?'] == 'Report'] = float('nan')
    else:
        DD_update['Change made in Connect?'].loc[DD_update['Change made in Connect?'] == 'Report'] = float('nan')
    return DD_update, Reports



