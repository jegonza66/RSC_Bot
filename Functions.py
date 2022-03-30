import pandas as pd
import os
import time
from datetime import datetime, timedelta

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


def complete_deactivated_catalog_section(DD_update):

    deactivated_catalogs = DD_update[DD_update['Type of Change'] == 'deactivated catalog'][
        ['School', 'Catalog']].reset_index(drop=True)

    for index, row in deactivated_catalogs.iterrows():
        School = deactivated_catalogs.iloc[index]['School']
        Catalog = deactivated_catalogs.iloc[index]['Catalog']

        DD_update.loc[(DD_update['Type of Change'] == 'deactivated catalog') & (DD_update['School'] == School) & (
                DD_update['Catalog'] == Catalog), 'Change made in Connect?'] = 'No Expected Change'

        DD_update.loc[(DD_update['Type of Change'] == 'deactivated section') & (DD_update['School'] == School) & (
                DD_update['Catalog'] == Catalog), 'Change made in Connect?'] = 'No Expected Change'

    # Take new returned catalogs and set to no expected change, term has ended
    today = datetime.today().date()
    new_catalogs = DD_update['Catalog Last End Date'][(DD_update['Type of Change'] == 'new catalog')]
    catalogs_dates = [datetime.strptime(date[1][-10:], '%m/%d/%Y').date() for date in
                      new_catalogs.str.split('Last end date ')]
    new_returned_catalogs_index = [catalog_end_date < today for catalog_end_date in catalogs_dates]
    new_returned_catalogs = DD_update[(DD_update['Type of Change'] == 'new catalog')][
        ['School', 'Catalog']][new_returned_catalogs_index]

    for index, row in new_returned_catalogs.iterrows():
        School = DD_update.iloc[index]['School']
        Catalog = DD_update.iloc[index]['Catalog']

        DD_update.loc[(DD_update['Type of Change'] == 'new catalog') & (DD_update['School'] == School) & (
                DD_update['Catalog'] == Catalog), 'Change made in Connect?'] = 'No Expected Change'

        DD_update.loc[(DD_update['Type of Change'] == 'new catalog') & (DD_update['School'] == School) & (
                DD_update['Catalog'] == Catalog), 'Issue'] = 'term has ended'

        DD_update.loc[(DD_update['Type of Change'] == 'new section') & (DD_update['School'] == School) & (
                DD_update['Catalog'] == Catalog), 'Change made in Connect?'] = 'No Expected Change'

        DD_update.loc[(DD_update['Type of Change'] == 'new section') & (DD_update['School'] == School) & (
                DD_update['Catalog'] == Catalog), 'Issue'] = 'term has ended'

    return DD_update

def save_DD1(DD_update, Credentials, date):
    # DD1_Save = DD_update.loc[:, ~DD_update.columns.str.startswith('Extra')]
    DD1_Save = DD_update.sort_values(['Type of Change', 'School', 'Catalog']).reset_index(drop=True)

    path_1 = Credentials['csv_save_path'] + 'DD1/'
    os.makedirs(path_1, exist_ok=True)
    file_name = path_1 + 'DD1 Update {}.xlsx'.format(date)
    DD1_Save.to_excel(file_name, index=False)
    print('\nDD1_update {} file saved to {}'.format(date, path_1))

def save_DD2(DD_update, Credentials, date):
    # DD2_Save = DD_update.loc[:, ~DD_update.columns.str.startswith('Extra')]
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
            hours = float(input('There are {} cases to be checked.\n'
                                'How much time (hours) would you like to wait before running the online check?'
                                '(so Slurpee can complete the changes).\n'
                                'Hours:'.format(missing_rows)))
        except ValueError:
            print("That's not an number!")
    print('Waiting until {} for Slurpee to finish changes before checking...'.format(format(datetime.now() + timedelta(hours=hours),
                                                                                            '%H:%M:%S')))
    time.sleep(3600 * hours)