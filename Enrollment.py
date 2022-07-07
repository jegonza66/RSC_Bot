import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from itertools import compress

import Functions


def load_files(Credentials, enrollment_files_path):

    if enrollment_files_path is None:
        # Read files
        print('Please use the dialog window to go to the location of the OLD enrollment file.')
        # Open file explorer dialog
        root = tk.Tk()
        root.withdraw()
        Enrollment_old_path = filedialog.askopenfilename()

        print('Please use the dialog window to go to the location of the NEW enrollment file.')
        root = tk.Tk()
        root.withdraw()
        Enrollment_new_path = filedialog.askopenfilename()
    else:
        file_date = datetime.today().date().strftime('%Y%m%d')
        new_index = [file_date in file for file in enrollment_files_path]
        old_index = [not el for el in new_index]
        Enrollment_old_path = list(compress(enrollment_files_path, old_index))[0]
        Enrollment_new_path = list(compress(enrollment_files_path, new_index))[0]

    print('Loading old enrollment file: {}'.format(Enrollment_old_path.split(Credentials['adoption_enrollment_path'])[-1]))
    Old_en_file = pd.read_csv(Enrollment_old_path, keep_default_na=False)
    print('Done')

    print('Loading new enrollment file: {}'.format(Enrollment_new_path.split(Credentials['adoption_enrollment_path'])[-1]))
    New_en_file = pd.read_csv(Enrollment_new_path, keep_default_na=False)
    print('Done')

    return Old_en_file, New_en_file


def add_new_columns(Old_en_file, New_en_file):

    print('Adding new concat columns.')

    Old_en_file['catalog'] = Old_en_file['term_name'].map(str) + '/-/' + Old_en_file['tenant_id'].map(str)
    New_en_file['catalog'] = New_en_file['term_name'].map(str) + '/-/' + New_en_file['tenant_id'].map(str)

    return Old_en_file, New_en_file


def compare_make_DD_update(Old_en_file, New_en_file, Old_ad_file, New_ad_file, DD_update, date):

    print('Comparing old and new files.')

    # New enrollments
    new_enrollments_index = ~New_en_file['catalog'].isin(Old_en_file['catalog'])
    new_enrollments = New_en_file[new_enrollments_index].drop_duplicates('catalog')
    new_enrollments_filtered = new_enrollments[['tenant_name', 'term_name', 'catalog', 'tenant_id']].reset_index(drop=True)

    last_end_dates = []
    for catalog in new_enrollments_filtered['catalog']:
        new_enrollment_catalog_dates = New_ad_file[['catalog', 'schedule_end']].loc[New_ad_file['catalog']
                                                                                    == catalog]
        new_enrollment_sorted = new_enrollment_catalog_dates.sort_values(['catalog', 'schedule_end'],
                                                                         ascending=[True, False])
        new_enrollment_date = new_enrollment_sorted.drop_duplicates('catalog').reset_index(drop=True)
        last_end_dates.append(new_enrollment_date['schedule_end'].values[0])

    new_enrollments_filtered['schedule_end'] = last_end_dates
    new_enrollments_filtered['schedule_end'] = pd.to_datetime(new_enrollments_filtered['schedule_end'],
                                                                      format="%Y-%m-%d")
    new_enrollments_filtered['schedule_end'] = new_enrollments_filtered.schedule_end.map(Functions.seasons_of_date)
    new_enrollments_filtered.drop('catalog', axis='columns', inplace=True)
    new_enrollments_filtered = new_enrollments_filtered.rename(columns={'tenant_name': 'School', 'term_name': 'Catalog',
                                                                        'schedule_end': 'Catalog Last End Date',
                                                                        'tenant_id': 'Extra_id'})
    new_enrollments_df = Functions.make_full_df(new_enrollments_filtered)
    new_enrollments_df['Type of Change'] = 'new enrollment'


    # Deactivated enrollments
    deactivated_enrollments_index = ~Old_en_file['catalog'].isin(New_en_file['catalog'])
    deactivated_enrollments = Old_en_file[deactivated_enrollments_index].drop_duplicates('catalog')
    deactivated_enrollments_filtered = deactivated_enrollments[['tenant_name', 'term_name', 'catalog', 'tenant_id']].\
        reset_index(drop=True)

    last_end_dates = []
    for catalog in deactivated_enrollments_filtered['catalog']:
        deactivated_enrollment_catalog_dates = Old_ad_file[['catalog', 'schedule_end']].loc[Old_ad_file['catalog']
                                                                                            == catalog]
        deactivated_enrollment_sorted = deactivated_enrollment_catalog_dates.sort_values(['catalog', 'schedule_end'],
                                                                                           ascending=[True, False])
        deactivated_enrollment_date = deactivated_enrollment_sorted.drop_duplicates('catalog').reset_index(drop=True)
        last_end_dates.append(deactivated_enrollment_date['schedule_end'].values[0])

    deactivated_enrollments_filtered['schedule_end'] = last_end_dates
    deactivated_enrollments_filtered['schedule_end'] = pd.to_datetime(deactivated_enrollments_filtered['schedule_end'],
                                                                    format="%Y-%m-%d")
    deactivated_enrollments_filtered['schedule_end'] = deactivated_enrollments_filtered.schedule_end.map(Functions.seasons_of_date)
    deactivated_enrollments_filtered.drop('catalog', axis='columns', inplace=True)
    deactivated_enrollments_filtered = deactivated_enrollments_filtered.reset_index(drop=True).rename(
        columns={'tenant_name': 'School', 'term_name': 'Catalog', 'schedule_end': 'Catalog Last End Date',
                 'tenant_id': 'Extra_id'})
    deactivated_enrollments_df = Functions.make_full_df(deactivated_enrollments_filtered)
    deactivated_enrollments_df['Type of Change'] = 'deactivated enrollment'

    if deactivated_enrollments_df.__len__() or new_enrollments_df.__len__():
        print('Loading enrollment changes to DD_update file')
        DD_update = pd.concat([DD_update, new_enrollments_df, deactivated_enrollments_df]).reset_index(drop=True)

    DD_update['Date of Change (date of adoptions file of new data)'] = pd.to_datetime(date, format="%d-%m-%Y").strftime("%m/%d/%Y")
    print('Done')

    return DD_update