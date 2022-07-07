import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from itertools import compress

import Functions


def load_files(Credentials, adoption_files_path):

    if adoption_files_path is None:
        # Read files
        print('Please use the dialog window to go to the location of the OLD adoption file.')
        # Open file explorer dialog
        root = tk.Tk()
        root.withdraw()
        Adoption_old_path = filedialog.askopenfilename()

        print('Please use the dialog window to go to the location of the NEW adoption file.')
        root = tk.Tk()
        root.withdraw()
        Adoption_new_path = filedialog.askopenfilename()

    else:
        # Get files with right dates
        file_date = datetime.today().date().strftime('%Y%m%d')
        new_index = [file_date in file for file in adoption_files_path]
        old_index = [not el for el in new_index]
        Adoption_old_path = list(compress(adoption_files_path, old_index))[0]
        Adoption_new_path = list(compress(adoption_files_path, new_index))[0]

    print('Loading Old adoption file: {}'.format(Adoption_old_path.split(Credentials['adoption_enrollment_path'])[-1]))
    Old_ad_file = pd.read_csv(Adoption_old_path, keep_default_na=False)
    print('Done')

    print('Loading new adoption file: {}'.format(Adoption_new_path.split(Credentials['adoption_enrollment_path'])[-1]))
    New_ad_file = pd.read_csv(Adoption_new_path, keep_default_na=False)
    print('Done')

    New_ad_file['section_code_DD'] = New_ad_file['section_code'].str.replace(r'^(0+)', '', regex=True)
    Old_ad_file['section_code_DD'] = Old_ad_file['section_code'].str.replace(r'^(0+)', '', regex=True)

    date = Adoption_new_path.split('_')
    date = pd.to_datetime(date[-2], format="%Y%m%d").strftime("%d-%m-%Y")

    return Old_ad_file, New_ad_file, date


def add_new_columns(Old_ad_file, New_ad_file):
    print('Adding new concat columns.')

    Old_ad_file['catalog'] = Old_ad_file['term_name'].map(str) + '/-/' + Old_ad_file['tenant_id'].map(str)
    New_ad_file['catalog'] = New_ad_file['term_name'].map(str) + '/-/' + New_ad_file['tenant_id'].map(str)

    Old_ad_file['course_DD'] = Old_ad_file['department_name'].map(str) + '-' + Old_ad_file['course_number'].map(str) \
                              + '-' + Old_ad_file['section_code_DD'].map(str) + '-' + Old_ad_file['term_name'].map(str)
    New_ad_file['course_DD'] = New_ad_file['department_name'].map(str) + '-' + New_ad_file['course_number'].map(str) \
                              + '-' + New_ad_file['section_code_DD'].map(str) + '-' + New_ad_file['term_name'].map(str)

    Old_ad_file['course'] = Old_ad_file['department_name'].map(str) + '/-/' + Old_ad_file['course_number'].map(str) \
                         + '/-/' + Old_ad_file['section_code'].map(str) + '/-/' + Old_ad_file['catalog'].map(str)
    New_ad_file['course'] = New_ad_file['department_name'].map(str) + '/-/' + New_ad_file['course_number'].map(str) \
                         + '/-/' + New_ad_file['section_code'].map(str) + '/-/' + New_ad_file['catalog'].map(str)

    Old_ad_file['supercourse'] = Old_ad_file['course'].map(str) + '/-/' + Old_ad_file['sku'].map(str)
    New_ad_file['supercourse'] = New_ad_file['course'].map(str) + '/-/' + New_ad_file['sku'].map(str)

    Old_ad_file['sku concat'] = Old_ad_file['sku'].map(str) + '/-/' + Old_ad_file['tenant_id'].map(str) + '/-/' \
                             + Old_ad_file['term_name'].map(str)
    New_ad_file['sku concat'] = New_ad_file['sku'].map(str) + '/-/' + New_ad_file['tenant_id'].map(str) + '/-/' \
                             + New_ad_file['term_name'].map(str)

    Old_ad_file['schedule concat'] = Old_ad_file['schedule_start'].map(str) + '/-/' + Old_ad_file['schedule_end'].map(str) \
                                  + '/-/' + Old_ad_file['tenant_id'].map(str) + '/-/' + Old_ad_file['term_name'].map(str)
    New_ad_file['schedule concat'] = New_ad_file['schedule_start'].map(str) + '/-/' + New_ad_file['schedule_end'].map(str) \
                                  + '/-/' + New_ad_file['tenant_id'].map(str) + '/-/' + New_ad_file['term_name'].map(str)

    Old_ad_file['opt out concat'] = Old_ad_file['participation_model'].map(str) + '/-/' + Old_ad_file['tenant_id'].map(str) \
                                 + '/-/' + Old_ad_file['term_name'].map(str)
    New_ad_file['opt out concat'] = New_ad_file['participation_model'].map(str) + '/-/' + New_ad_file['tenant_id'].map(str) \
                                 + '/-/' + New_ad_file['term_name'].map(str)

    Old_ad_file['superconcat'] = Old_ad_file['supercourse'].map(str) + '/-/' + Old_ad_file['schedule_start'].map(str) + \
                                 '/-/' + Old_ad_file['schedule_end'].map(str) + '/-/' + Old_ad_file['net_price'].map(str) + \
                                 '/-/' + Old_ad_file['student_price'].map(str)
    New_ad_file['superconcat'] = New_ad_file['supercourse'].map(str) + '/-/' + New_ad_file['schedule_start'].map(str) + \
                                 '/-/' + New_ad_file['schedule_end'].map(str) + '/-/' + New_ad_file['net_price'].map(str) + \
                                 '/-/' + New_ad_file['student_price'].map(str)

    return Old_ad_file, New_ad_file


def compare_make_DD_update(Old_ad_file, New_ad_file):
    print('Comparing old and new files.')

    # New sections
    new_sections_index = ~New_ad_file['course'].isin(Old_ad_file['course'])
    new_sections = New_ad_file[['tenant_name', 'term_name', 'course_DD', 'sku', 'tenant_id', 'course', 'schedule_start',
                                'schedule_end', 'superconcat']][new_sections_index].reset_index(drop=True). \
        rename(columns={'tenant_name': 'School', 'term_name': 'Catalog', 'course_DD': 'Section_new',
                        'sku': 'Extra_SKU', 'tenant_id': 'Extra_id', 'course': 'Extra_Section',
                        'schedule_start': 'Extra_Start Date', 'schedule_end': 'Extra_End Date', 'superconcat': 'Extra_Superconcat'})
    new_sections_df = Functions.make_full_df(new_sections)
    new_sections_df['Type of Change'] = 'new section'

    # Deactivated sections
    deactivated_sections_index = ~Old_ad_file['course'].isin(New_ad_file['course'])
    deactivated_sections = Old_ad_file[['tenant_name', 'term_name', 'course_DD', 'sku', 'tenant_id', 'course',
                                        'schedule_start', 'schedule_end', 'superconcat']][deactivated_sections_index]. \
        reset_index(drop=True).rename(
        columns={'tenant_name': 'School', 'term_name': 'Catalog', 'course_DD': 'Section', 'sku': 'Extra_SKU',
                 'tenant_id': 'Extra_id', 'course': 'Extra_Section', 'schedule_start': 'Extra_Start Date',
                 'schedule_end': 'Extra_End Date', 'superconcat': 'Extra_Superconcat'})
    deactivated_sections_df = Functions.make_full_df(deactivated_sections)
    deactivated_sections_df['Type of Change'] = 'deactivated section'

    # New Catalogs
    new_catalogs_index = ~New_ad_file['catalog'].isin(Old_ad_file['catalog'])
    new_catalogs = New_ad_file[new_catalogs_index]

    # separar por catalogo y tomar la ultima schedule end y agregar estacion y año
    new_catalogs_sorted = new_catalogs.sort_values(['catalog', 'schedule_end'], ascending=[True, False])
    new_catalogs_filtered = new_catalogs_sorted.drop_duplicates('catalog').reset_index(drop=True)
    new_catalogs_filtered['schedule_end'] = pd.to_datetime(new_catalogs_filtered['schedule_end'], format="%Y-%m-%d")
    new_catalogs_filtered['schedule_end'] = new_catalogs_filtered.schedule_end.map(Functions.seasons_of_date)
    new_catalogs_filtered = new_catalogs_filtered[['tenant_name', 'term_name', 'schedule_end', 'sku', 'tenant_id',
                                                   'course', 'superconcat']].reset_index(drop=True). \
        rename(columns={'tenant_name': 'School', 'term_name': 'Catalog', 'schedule_end': 'Catalog Last End Date',
                        'sku': 'Extra_SKU', 'tenant_id': 'Extra_id', 'course': 'Extra_Section',
                        'superconcat': 'Extra_Superconcat'})
    new_catalogs_df = Functions.make_full_df(new_catalogs_filtered)
    new_catalogs_df['Type of Change'] = 'new catalog'

    # Deactivated Catalogs
    deactivated_catalogs_index = ~Old_ad_file['catalog'].isin(New_ad_file['catalog'])
    deactivated_catalogs = Old_ad_file[deactivated_catalogs_index]
    deactivated_catalogs_sorted = deactivated_catalogs.sort_values(['catalog', 'schedule_end'], ascending=[True, False])
    deactivated_catalogs_filtered = deactivated_catalogs_sorted.drop_duplicates('catalog').reset_index(drop=True)
    deactivated_catalogs_filtered['schedule_end'] = pd.to_datetime(deactivated_catalogs_filtered['schedule_end'],
                                                                   format="%Y-%m-%d")
    deactivated_catalogs_filtered['schedule_end'] = deactivated_catalogs_filtered.schedule_end.map(
        Functions.seasons_of_date)
    deactivated_catalogs_filtered = deactivated_catalogs_filtered[['tenant_name', 'term_name', 'schedule_end', 'sku',
                                                                   'tenant_id', 'course', 'superconcat']]. \
        reset_index(drop=True).rename(columns={'tenant_name': 'School', 'term_name': 'Catalog', 'schedule_end':
        'Catalog Last End Date', 'sku': 'Extra_SKU', 'tenant_id': 'Extra_id', 'course': 'Extra_Section'
                                               , 'superconcat': 'Extra_Superconcat'})
    deactivated_catalogs_df = Functions.make_full_df(deactivated_catalogs_filtered)
    deactivated_catalogs_df['Type of Change'] = 'deactivated catalog'

    # New items
    new_items_current = New_ad_file.drop_duplicates(['sku concat', 'net_price', 'student_price'])
    new_items_index = ~new_items_current['sku concat'].isin(Old_ad_file['sku concat'])
    new_items = new_items_current[new_items_index][['tenant_name', 'term_name', 'course', 'sku', 'tenant_id', 'schedule_start',
                                                    'schedule_end', 'net_price', 'student_price', 'superconcat']].reset_index(drop=True)
    new_items = pd.DataFrame(new_items).rename(columns={'tenant_name': 'School', 'term_name': 'Catalog', 'course': 'Extra_Section',
                                                        'sku': 'SKU_new', 'tenant_id': 'Extra_id',
                                                        'schedule_start': 'Extra_Start Date', 'schedule_end': 'Extra_End Date',
                                                        'net_price': 'Extra_Net Price', 'student_price': 'Extra_Student Price',
                                                        'superconcat': 'Extra_Superconcat'})
    new_items_df = Functions.make_full_df(new_items)
    new_items_df['Type of Change'] = 'new item'

    # New Schedules
    new_schedules_current = New_ad_file.drop_duplicates('schedule concat')
    new_schedules_index = ~new_schedules_current['schedule concat'].isin(Old_ad_file['schedule concat'])
    new_schedules = new_schedules_current[new_schedules_index][['schedule_start', 'schedule_end', 'tenant_name',
                                                                'term_name', 'sku', 'tenant_id', 'course',
                                                                'superconcat']].reset_index(drop=True)
    if len(new_schedules):
        new_schedules['schedule_start'] = pd.to_datetime(new_schedules['schedule_start'], format="%Y-%m-%d %H:%M:%S").dt.strftime("%m/%d/%Y")
        new_schedules['schedule_end'] = pd.to_datetime(new_schedules['schedule_end'], format="%Y-%m-%d %H:%M:%S").dt.strftime("%m/%d/%Y")
    new_schedules = new_schedules.rename(columns={'tenant_name': 'School', 'term_name': 'Catalog',
                                                  'schedule_start': 'Start Date', 'schedule_end': 'End Date',
                                                  'sku': 'Extra_SKU', 'tenant_id': 'Extra_id', 'course': 'Extra_Section',
                                                  'superconcat': 'Extra_Superconcat'})
    new_schedules_df = Functions.make_full_df(new_schedules)
    new_schedules_df['Type of Change'] = 'new schedule'

    # Deactivated items
    deactivated_items_index = ~Old_ad_file['supercourse'].isin(New_ad_file['supercourse'])
    deactivated_items_all = Old_ad_file[(~deactivated_sections_index) & (deactivated_items_index)].sort_values('supercourse')
    
    # Updated items
    updated_items_index = ~New_ad_file['supercourse'].isin(Old_ad_file['supercourse'])
    updated_items_index_old_section = (~new_sections_index) & (updated_items_index)
    updated_items_all = New_ad_file[updated_items_index_old_section].sort_values('supercourse')
    updated_items = updated_items_all.loc[updated_items_all['course'].isin(deactivated_items_all['course'])]

    deactivated_items = deactivated_items_all.loc[deactivated_items_all['course'].isin(updated_items_all['course'])]
    deactivated_skus = []
    for course in updated_items['course']:
        deactivated_skus.append(deactivated_items_all[deactivated_items_all['course'] == course]['sku'].values)

    # repeat the updated items rows to match the amount of deactivated items for each course
    updated_items = updated_items.iloc[np.repeat(np.arange(len(updated_items)), [len(skus) for skus in deactivated_skus])]

    # Additional Items
    additional_items_raw = New_ad_file.loc[New_ad_file['course'].isin(updated_items_all['course'])]
    merged = updated_items_all.merge(additional_items_raw, how='right', indicator=True)
    additional_items_index = merged['_merge'] == 'right_only'
    additional_items = merged[additional_items_index].drop('_merge', axis='columns').sort_values('supercourse').reset_index(drop=True)

    new_skus = []
    for course in additional_items['course']:
        new_skus.append(updated_items_all[updated_items_all['course'] == course]['sku'].values)

    additional_items = additional_items.iloc[np.repeat(np.arange(len(additional_items)), [len(skus) for skus in new_skus])]

    additional_items_filtered = additional_items[['tenant_name', 'term_name', 'course_DD', 'sku',
                                                  'tenant_id', 'course', 'schedule_start', 'schedule_end',
                                                  'net_price', 'student_price', 'superconcat']].reset_index(drop=True). \
        rename(columns={'tenant_name': 'School', 'term_name': 'Catalog', 'course_DD': 'Section', 'sku': 'SKU',
                       'tenant_id': 'Extra_id', 'course': 'Extra_Section', 'schedule_start': 'Extra_Start Date',
                        'schedule_end': 'Extra_End Date', 'net_price': 'Extra_Net Price',
                        'student_price': 'Extra_Student Price', 'superconcat': 'Extra_Superconcat'}).sort_values('Section')

    updated_items_filtered = updated_items[['tenant_name', 'term_name', 'course_DD', 'sku', 'tenant_id',
                                            'course', 'schedule_start', 'schedule_end', 'net_price', 'student_price',
                                            'superconcat']].\
        reset_index(drop=True).rename(columns={'tenant_name': 'School', 'term_name': 'Catalog', 'course_DD': 'Section',
                                               'sku': 'SKU_new', 'tenant_id': 'Extra_id', 'course': 'Extra_Section',
                                               'schedule_start': 'Extra_Start Date', 'schedule_end': 'Extra_End Date',
                                               'net_price': 'Extra_Net Price', 'student_price': 'Extra_Student Price',
                                               'superconcat': 'Extra_Superconcat'}).sort_values('Section')
    if len(deactivated_skus):
        deactivated_skus = np.concatenate(deactivated_skus).ravel()
    if len(new_skus):
        new_skus = np.concatenate(new_skus).ravel()

    updated_items_filtered['SKU'] = deactivated_skus
    additional_items_filtered['SKU_new'] = new_skus

    updated_items_df = Functions.make_full_df(updated_items_filtered)
    updated_items_df['Type of Change'] = 'updated item'
    additional_items_df = Functions.make_full_df(additional_items_filtered)
    additional_items_df['Type of Change'] = 'additional item'

    # Opt Out
    opt_out_index = ~Old_ad_file['opt out concat'].isin(New_ad_file['opt out concat'])
    opt_out = Old_ad_file[['tenant_name', 'term_name', 'sku', 'tenant_id', 'course', 'superconcat']][~deactivated_catalogs_index & opt_out_index]. \
        reset_index(drop=True).rename(columns={'tenant_name': 'School', 'term_name': 'Catalog', 'sku': 'Extra_SKU',
                                               'tenant_id': 'Extra_id', 'course': 'Extra_Section',
                                               'superconcat': 'Extra_Superconcat'})
    opt_out['Previous Data'] = 'opt-in'
    opt_out['Section_new'] = 'opt-out'
    opt_out_df = Functions.make_full_df(opt_out)
    opt_out_df['Type of Change'] = 'participation model change'

    # Make matching supercourses files for net price comparison
    matching_supercourse_index_old = Old_ad_file['supercourse'].isin(New_ad_file['supercourse']).reset_index(
        drop=True)
    matching_supercourse_index_new = New_ad_file['supercourse'].isin(Old_ad_file['supercourse']).reset_index(
        drop=True)
    Matching_Old_ad_file = Old_ad_file.loc[matching_supercourse_index_old].fillna('').drop_duplicates('supercourse').\
        sort_values('supercourse').reset_index(
        drop=True)
    Matching_New_ad_file = New_ad_file.loc[matching_supercourse_index_new].fillna('').drop_duplicates('supercourse').\
        sort_values('supercourse').reset_index(
        drop=True)


    # Net Price
    net_price_change_index = ~(Matching_Old_ad_file['net_price'] == Matching_New_ad_file['net_price'])
    net_price_change = Matching_Old_ad_file[['tenant_name', 'term_name', 'course_DD', 'sku', 'net_price', 'tenant_id',
                                             'course', 'schedule_start', 'schedule_end']][
        net_price_change_index]. \
        rename(columns={'tenant_name': 'School', 'term_name': 'Catalog', 'course_DD': 'Section', 'sku': 'SKU',
                        'net_price': 'Previous Data', 'tenant_id': 'Extra_id', 'course': 'Extra_Section',
                        'schedule_start': 'Extra_Start Date', 'schedule_end': 'Extra_End Date'})
    net_price_change['Net Price'] = Matching_New_ad_file['net_price'][net_price_change_index]
    net_price_change['Extra_Superconcat'] = Matching_New_ad_file['superconcat'][net_price_change_index]

    net_price_df = Functions.make_full_df(net_price_change)
    net_price_df['Type of Change'] = 'net price change'

    # Student Price
    student_price_change_index = ~(Matching_Old_ad_file['student_price'] == Matching_New_ad_file['student_price'])
    student_price_change = Matching_Old_ad_file[['tenant_name', 'term_name', 'course_DD', 'sku', 'student_price',
                                              'tenant_id', 'course', 'schedule_start', 'schedule_end']][
        student_price_change_index]. \
        rename(columns={'tenant_name': 'School', 'term_name': 'Catalog', 'course_DD': 'Section', 'sku': 'SKU',
                        'student_price': 'Previous Data', 'tenant_id': 'Extra_id', 'course': 'Extra_Section',
                        'schedule_start': 'Extra_Start Date', 'schedule_end': 'Extra_End Date'})
    student_price_change['Student Price'] = Matching_New_ad_file['student_price'][student_price_change_index]
    student_price_change['Extra_Superconcat'] = Matching_New_ad_file['superconcat'][student_price_change_index]

    student_price_df = Functions.make_full_df(student_price_change)
    student_price_df['Type of Change'] = 'student price change'

    # Start date change
    schedule_start_change_index = ~(Matching_Old_ad_file['schedule_start'] == Matching_New_ad_file['schedule_start'])
    schedule_start_change = Matching_Old_ad_file[['tenant_name', 'term_name', 'course_DD', 'sku', 'schedule_start',
                                                  'tenant_id', 'course', 'schedule_end']][schedule_start_change_index]. \
        rename(columns={'tenant_name': 'School', 'term_name': 'Catalog', 'course_DD': 'Section', 'sku': 'SKU',
                        'schedule_start': 'Previous Data', 'tenant_id': 'Extra_id', 'course': 'Extra_Section',
                        'schedule_end': 'Extra_End Date'})

    schedule_start_change['Extra_Start Date'] = schedule_start_change['Previous Data'].values
    schedule_start_change['Previous Data'] = pd.to_datetime(schedule_start_change['Previous Data'],
                                                            format="%Y-%m-%d").dt.strftime("%m/%d/%Y")

    schedule_start_change['Start Date'] = pd.to_datetime(
        Matching_New_ad_file['schedule_start'][schedule_start_change_index],
        format="%Y-%m-%d").dt.strftime("%m/%d/%Y")
    schedule_start_change['Extra_Superconcat'] = Matching_New_ad_file['superconcat'][schedule_start_change_index]


    schedule_start_df = Functions.make_full_df(schedule_start_change)
    schedule_start_df['Type of Change'] = 'start date change'

    # End date change
    schedule_end_change_index = ~(Matching_Old_ad_file['schedule_end'] == Matching_New_ad_file['schedule_end'])
    schedule_end_change = Matching_Old_ad_file[['tenant_name', 'term_name', 'course_DD', 'sku', 'schedule_end',
                                             'tenant_id', 'course', 'schedule_start']][schedule_end_change_index]. \
        rename(columns={'tenant_name': 'School', 'term_name': 'Catalog', 'course_DD': 'Section', 'sku': 'SKU',
                        'schedule_end': 'Previous Data', 'tenant_id': 'Extra_id', 'course': 'Extra_Section',
                        'schedule_start': 'Extra_Start Date'})

    schedule_end_change['Extra_End Date'] = schedule_end_change['Previous Data'].values
    schedule_end_change['Previous Data'] = pd.to_datetime(schedule_end_change['Previous Data'],
                                                          format="%Y-%m-%d").dt.strftime("%m/%d/%Y")

    schedule_end_change['End Date'] = pd.to_datetime(Matching_New_ad_file['schedule_end'][schedule_end_change_index],
                                                     format="%Y-%m-%d").dt.strftime("%m/%d/%Y")
    schedule_end_change['Extra_Superconcat'] = Matching_New_ad_file['superconcat'][schedule_end_change_index]

    schedule_end_df = Functions.make_full_df(schedule_end_change)
    schedule_end_df['Type of Change'] = 'end date change'

    print('Loading adoption changes to DD_update file.')

    DD_update = pd.concat([new_sections_df, updated_items_df, additional_items_df, new_items_df, new_schedules_df,
                           new_catalogs_df, deactivated_catalogs_df, deactivated_sections_df, net_price_df,
                           student_price_df, schedule_start_df, schedule_end_df, opt_out_df]).reset_index(drop=True)
    print('Done.')

    return DD_update
