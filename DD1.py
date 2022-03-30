import Adoptions
import Enrollment
import Functions

from datetime import datetime

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

def run(adoption_files_path, enrollment_files_path, Credentials):

    # Load adoptions files
    Old_ad_file, New_ad_file, date = Adoptions.load_files(adoption_files_path)
    # add new concantenated columns
    Old_ad_file, New_ad_file = Adoptions.add_new_columns(Old_ad_file=Old_ad_file, New_ad_file=New_ad_file)
    # Compare ald and new files
    DD_update = Adoptions.compare_make_DD_update(Old_ad_file=Old_ad_file, New_ad_file=New_ad_file)

    # Load enrollment files
    Old_en_file, New_en_file = Enrollment.load_files(enrollment_files_path)
    # add new concantenated columns
    Old_en_file, New_en_file = Enrollment.add_new_columns(Old_en_file=Old_en_file, New_en_file=New_en_file)
    # Compare ald and new files
    DD_update = Enrollment.compare_make_DD_update(Old_en_file=Old_en_file, New_en_file=New_en_file, Old_ad_file=Old_ad_file,
                                                  New_ad_file=New_ad_file, DD_update=DD_update, date=date)

    # Sort rows by school and catalog to check them in order
    DD_update = DD_update.sort_values(['School', 'Catalog', 'Type of Change']).reset_index(drop=True)

    # Complete no expected change on deactivated catalogs and sections
    DD_update = complete_deactivated_catalog_section(DD_update=DD_update)

    # Save DD1_update file before Check in Connect
    Functions.save_DD1(DD_update=DD_update, Credentials=Credentials, date=date)

    return Old_ad_file, New_ad_file, DD_update, date