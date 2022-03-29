import Adoptions
import Enrollment

def run():

    # Load adoptions files
    Old_ad_file, New_ad_file, date = Adoptions.load_files()
    # add new concantenated columns
    Old_ad_file, New_ad_file = Adoptions.add_new_columns(Old_ad_file=Old_ad_file, New_ad_file=New_ad_file)
    # Compare ald and new files
    DD_update = Adoptions.compare_make_DD_update(Old_ad_file=Old_ad_file, New_ad_file=New_ad_file)

    # Load enrollment files
    Old_en_file, New_en_file = Enrollment.load_files()
    # add new concantenated columns
    Old_en_file, New_en_file = Enrollment.add_new_columns(Old_en_file=Old_en_file, New_en_file=New_en_file)
    # Compare ald and new files
    DD_update = Enrollment.compare_make_DD_update(Old_en_file=Old_en_file, New_en_file=New_en_file, Old_ad_file=Old_ad_file,
                                                  New_ad_file=New_ad_file, DD_update=DD_update, date=date)

    # Sort rows by school and catalog to check them in order
    DD_update = DD_update.sort_values(['School', 'Catalog', 'Type of Change']).reset_index(drop=True)

    return Old_ad_file, New_ad_file, DD_update, date