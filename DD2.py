import Chrome_navigator
from datetime import datetime
import time
import pandas as pd


def check_new_section(row, index, previous_school, previous_catalog, DD_update, driver):
    tenant_id, Catalog = row['Extra_id'], row['Catalog']
    School_change = tenant_id != previous_school
    Catalog_change = Catalog != previous_catalog

    sku = row['Extra_SKU']
    start_date = row['Extra_Start Date']
    end_date = row['Extra_End Date']

    department_name = row['Extra_Section'].split('/-/')[0]
    course_number = row['Extra_Section'].split('/-/')[1]
    section_code = row['Extra_Section'].split('/-/')[2]

    print('{} - {} - {} - {}'.format(tenant_id, Catalog, '-'.join([department_name, course_number,
                                                                   section_code]), sku))
    print(row['Type of Change'])

    if School_change:
        School_Selected = Chrome_navigator.verba_open_school(driver=driver, Verba_School=tenant_id)
    else:
        School_Selected = True

    if School_Selected:
        previous_school = tenant_id
        if School_change or Catalog_change:
            Catalog_Selected = Chrome_navigator.verba_open_catalog(driver=driver, Catalog=Catalog)
        else:
            Catalog_Selected = True

        if Catalog_Selected:
            previous_catalog = Catalog
            schedule_start_date, opt_out_date, invoice_date = Chrome_navigator.verba_dashboard_schedule(driver=driver,
                                                                                                        start_date=start_date,
                                                                                                        end_date=end_date)
            Past_Invoice = False
            Past_Opt_Out = False
            if (type(opt_out_date) == datetime) & (type(invoice_date) == datetime):
                today = datetime.today().date()
                if today > invoice_date.date():
                    Past_Invoice = True

                elif today > opt_out_date.date():
                    Past_Opt_Out = True

            Items_Menu_Open = Chrome_navigator.verba_open_item_menu(driver=driver)
            if Items_Menu_Open:
                Item_Open = Chrome_navigator.verba_open_item(driver=driver, sku=sku)
                if Item_Open:
                    Course_Active, schedule = Chrome_navigator.verba_active_schedule(driver=driver,
                                                                                     department_name=department_name,
                                                                                     course_number=course_number,
                                                                                     section_code=section_code)
                    if Past_Invoice:
                        DD_update['Change made in Connect?'][index] = 'No Expected Change'
                        DD_update['Reason change not made'][index] = 'After Invoice'
                        print('Past Invoice Date. Dismiss')
                    elif Past_Opt_Out:
                        DD_update['Change made in Connect?'][index] = 'No'
                        DD_update['Reason change not made'][index] = 'After Opt-Out Deadline'
                        print('Past Opt Out Date. Change manually')

                    if (Course_Active == 'Active') & (schedule == ' - '.join([start_date, end_date])):
                        DD_update['Change made in Connect?'][index] = 'Yes'
                        if Past_Invoice or Past_Opt_Out:
                            DD_update['Reason change not made'][index] = 'No Logical Reason'
                        print('OK')

                    if (Course_Active != 'Active') & (not Past_Invoice) & (not Past_Opt_Out):
                        DD_update['Change made in Connect?'][index] = 'No'
                        DD_update['Reason change not made'][index] = 'No Logical Reason'
                        print('OK')

    return DD_update, previous_school, previous_catalog


def check_new_item(row, index, previous_school, previous_catalog, DD_update, driver):
    tenant_id, Catalog = row['Extra_id'], row['Catalog']
    School_change = tenant_id != previous_school
    Catalog_change = Catalog != previous_catalog

    sku = row['SKU_new']

    net_price = row['Extra_Net Price']
    student_price = row['Extra_Student Price']

    department_name = row['Extra_Section'].split('/-/')[0]
    course_number = row['Extra_Section'].split('/-/')[1]
    section_code = row['Extra_Section'].split('/-/')[2]

    print('{} - {} - {} - {}'.format(tenant_id, Catalog, '-'.join([department_name, course_number,
                                                                   section_code]), sku))
    print(row['Type of Change'])

    if School_change:
        School_Selected = Chrome_navigator.verba_open_school(driver=driver, Verba_School=tenant_id)
    else:
        School_Selected = True

    if School_Selected:
        previous_school = tenant_id
        if School_change or Catalog_change:
            Catalog_Selected = Chrome_navigator.verba_open_catalog(driver=driver, Catalog=Catalog)
        else:
            Catalog_Selected = True

        if Catalog_Selected:
            previous_catalog = Catalog
            Items_Menu_Open = Chrome_navigator.verba_open_item_menu(driver=driver)
            if Items_Menu_Open:
                Item_Open = Chrome_navigator.verba_open_item(driver=driver, sku=sku)
                if Item_Open:
                    DD_update['Change made in Connect?'][index] = 'Yes'
                    print('OK')

                    Price_checked, connect_net_price, connect_student_price = Chrome_navigator.verba_price(driver=driver)

                    if Price_checked and (net_price != connect_net_price) or (student_price != connect_student_price):
                        DD_update['Issue'][index] = 'SKU with multiple prices'
                        print('SKU with multiple prices')
                else:
                    DD_update['Change made in Connect?'][index] = 'No'
                    DD_update['Reason change not made'][index] = 'No Logical Reason'
                    print('Change not made')

    return DD_update, previous_school, previous_catalog


def check_add_item(row, index, previous_school, previous_catalog, DD_update, driver):
    tenant_id, Catalog = row['Extra_id'], row['Catalog']
    School_change = tenant_id != previous_school
    Catalog_change = Catalog != previous_catalog

    sku = row['SKU_new']
    start_date = row['Extra_Start Date']
    end_date = row['Extra_End Date']

    department_name = row['Extra_Section'].split('/-/')[0]
    course_number = row['Extra_Section'].split('/-/')[1]
    section_code = row['Extra_Section'].split('/-/')[2]

    print('{} - {} - {} - {}'.format(tenant_id, Catalog, '-'.join([department_name, course_number,
                                                                   section_code]), sku))
    print(row['Type of Change'])

    if School_change:
        School_Selected = Chrome_navigator.verba_open_school(driver=driver, Verba_School=tenant_id)
    else:
        School_Selected = True

    if School_Selected:
        previous_school = tenant_id
        if School_change or Catalog_change:
            Catalog_Selected = Chrome_navigator.verba_open_catalog(driver=driver, Catalog=Catalog)
        else:
            Catalog_Selected = True

        if Catalog_Selected:
            previous_catalog = Catalog
            schedule_start_date, opt_out_date, invoice_date = Chrome_navigator.verba_dashboard_schedule(driver=driver,
                                                                                                        start_date=start_date,
                                                                                                        end_date=end_date)
            Past_Invoice = False
            Past_Opt_Out = False
            if (type(opt_out_date) == datetime) & (type(invoice_date) == datetime):
                today = datetime.today().date()
                if today > invoice_date.date():
                    Past_Invoice = True

                elif today > opt_out_date.date():
                    Past_Opt_Out = True

            Items_Menu_Open = Chrome_navigator.verba_open_item_menu(driver=driver)
            if Items_Menu_Open:
                Item_Open = Chrome_navigator.verba_open_item(driver=driver, sku=sku)
                if Item_Open:
                    Course_Active, schedule = Chrome_navigator.verba_active_schedule(driver=driver,
                                                                                     department_name=department_name,
                                                                                     course_number=course_number,
                                                                                     section_code=section_code)
                    if Past_Invoice:
                        DD_update['Change made in Connect?'][index] = 'No Expected Change'
                        DD_update['Reason change not made'][index] = 'After Invoice'
                        print('Past Invoice Date. Dismiss')
                    elif Past_Opt_Out:
                        DD_update['Change made in Connect?'][index] = 'No'
                        DD_update['Reason change not made'][index] = 'After Opt-Out Deadline'
                        print('Past Opt Out Date. Change manually')

                    if (Course_Active == 'Active') & (schedule == ' - '.join([start_date, end_date])):
                        DD_update['Change made in Connect?'][index] = 'Yes'
                        if Past_Invoice or Past_Opt_Out:
                            DD_update['Reason change not made'][index] = 'No Logical Reason'
                        print('OK')

    return DD_update, previous_school, previous_catalog


def check_upd_item(row, index, previous_school, previous_catalog, DD_update, driver):
    New_file_OK = False
    Old_file_OK = False

    tenant_id, Catalog = row['Extra_id'], row['Catalog']
    School_change = tenant_id != previous_school
    Catalog_change = Catalog != previous_catalog

    old_sku = row['SKU']
    sku = row['SKU_new']
    start_date = row['Extra_Start Date']
    end_date = row['Extra_End Date']

    department_name = row['Extra_Section'].split('/-/')[0]
    course_number = row['Extra_Section'].split('/-/')[1]
    section_code = row['Extra_Section'].split('/-/')[2]

    print('{} - {} - {} - {}'.format(tenant_id, Catalog, '-'.join([department_name, course_number,
                                                                   section_code]), sku))
    print(row['Type of Change'])

    if School_change:
        School_Selected = Chrome_navigator.verba_open_school(driver=driver, Verba_School=tenant_id)
    else:
        School_Selected = True

    if School_Selected:
        previous_school = tenant_id
        if School_change or Catalog_change:
            Catalog_Selected = Chrome_navigator.verba_open_catalog(driver=driver, Catalog=Catalog)
        else:
            Catalog_Selected = True

        if Catalog_Selected:
            previous_catalog = Catalog
            schedule_start_date, opt_out_date, invoice_date = Chrome_navigator.verba_dashboard_schedule(driver=driver,
                                                                                                        start_date=start_date,
                                                                                                        end_date=end_date)
            Past_Invoice = False
            Past_Opt_Out = False
            if (type(opt_out_date) == datetime) & (type(invoice_date) == datetime):
                today = datetime.today().date()
                if today > invoice_date.date():
                    Past_Invoice = True

                elif today > opt_out_date.date():
                    Past_Opt_Out = True

            Items_Menu_Open = Chrome_navigator.verba_open_item_menu(driver=driver)
            if Items_Menu_Open:
                Item_Open = Chrome_navigator.verba_open_item(driver=driver, sku=sku)
                if Item_Open:
                    Course_Active, schedule = Chrome_navigator.verba_active_schedule(driver=driver,
                                                                                     department_name=department_name,
                                                                                     course_number=course_number,
                                                                                     section_code=section_code)

                    if (Course_Active == 'Active') & (schedule == ' - '.join([start_date, end_date])):
                        New_file_OK = True

        # Check old item deactivated
        if Catalog_Selected:
            print('Checking if old sku is Inactive')
            Items_Menu_Open = Chrome_navigator.verba_open_item_menu(driver=driver)
            if Items_Menu_Open:
                Item_Open = Chrome_navigator.verba_open_item(driver=driver, sku=sku)
                if Item_Open:
                    Old_Course_Active, old_schedule = Chrome_navigator.verba_active_schedule(driver=driver,
                                                                                             department_name=department_name,
                                                                                             course_number=course_number,
                                                                                             section_code=section_code)
                    if (Old_Course_Active != 'Active') & (old_schedule == ' - '.join([start_date, end_date])):
                        Old_file_OK = True

                if Past_Invoice:
                    DD_update['Change made in Connect?'][index] = 'No Expected Change'
                    DD_update['Reason change not made'][index] = 'After Invoice'
                    print('Past Invoice Date. Dismiss')
                elif Past_Opt_Out:
                    DD_update['Change made in Connect?'][index] = 'No'
                    DD_update['Reason change not made'][index] = 'After Opt-Out Deadline'
                    print('Past Opt Out Date. Change manually')

                if New_file_OK & Old_file_OK:
                    DD_update['Change made in Connect?'][index] = 'Yes'
                    if Past_Invoice or Past_Opt_Out:
                        DD_update['Reason change not made'][index] = 'No Logical Reason'
                    print('OK')

    return DD_update, previous_school, previous_catalog


def check_new_catalog(row, index, previous_school, previous_catalog, DD_update, driver):
    tenant_id, Catalog = row['Extra_id'], row['Catalog']
    School_change = tenant_id != previous_school
    Catalog_change = Catalog != previous_catalog

    print('{} - {}'.format(tenant_id, Catalog))
    print(row['Type of Change'])

    if School_change:
        School_Selected = Chrome_navigator.verba_open_school(driver=driver, Verba_School=tenant_id)
    else:
        School_Selected = True

    if School_Selected:
        previous_school = tenant_id
        if School_change or Catalog_change:
            Catalog_Selected = Chrome_navigator.verba_open_catalog(driver=driver, Catalog=Catalog)
        else:
            Catalog_Selected = True

        if Catalog_Selected:
            previous_catalog = Catalog
            DD_update['Change made in Connect?'][index] = 'Yes'
            print('OK')

    return DD_update, previous_school, previous_catalog


def check_deact_section(row, index, previous_school, previous_catalog, DD_update, driver):
    tenant_id, Catalog = row['Extra_id'], row['Catalog']
    School_change = tenant_id != previous_school
    Catalog_change = Catalog != previous_catalog

    sku = row['Extra_SKU']
    start_date = row['Extra_Start Date']
    end_date = row['Extra_End Date']

    department_name = row['Extra_Section'].split('/-/')[0]
    course_number = row['Extra_Section'].split('/-/')[1]
    section_code = row['Extra_Section'].split('/-/')[2]

    print('{} - {} - {} - {}'.format(tenant_id, Catalog, '-'.join([department_name, course_number,
                                                                   section_code]), sku))
    print(row['Type of Change'])

    if School_change:
        School_Selected = Chrome_navigator.verba_open_school(driver=driver, Verba_School=tenant_id)
    else:
        School_Selected = True

    if School_Selected:
        previous_school = tenant_id
        if School_change or Catalog_change:
            Catalog_Selected = Chrome_navigator.verba_open_catalog(driver=driver, Catalog=Catalog)
        else:
            Catalog_Selected = True

        if Catalog_Selected:
            previous_catalog = Catalog
            schedule_start_date, opt_out_date, invoice_date = Chrome_navigator.verba_dashboard_schedule(driver=driver,
                                                                                                        start_date=start_date,
                                                                                                        end_date=end_date)
            Past_Invoice = False
            if (type(invoice_date) == datetime):
                today = datetime.today().date()
                if today > invoice_date.date():
                    Past_Invoice = True

            Items_Menu_Open = Chrome_navigator.verba_open_item_menu(driver=driver)
            if Items_Menu_Open:
                Item_Open = Chrome_navigator.verba_open_item(driver=driver, sku=sku)

                if Item_Open:
                    Course_Active, schedule = Chrome_navigator.verba_active_schedule(driver=driver,
                                                                                     department_name=department_name,
                                                                                     course_number=course_number,
                                                                                     section_code=section_code)
                    if Past_Invoice:
                        DD_update['Change made in Connect?'][index] = 'No Expected Change'
                        DD_update['Reason change not made'][index] = 'After Invoice'
                        print('Past Invoice Date. Dismiss')

                    if (Course_Active != 'Active'):
                        DD_update['Change made in Connect?'][index] = 'Yes'
                        if Past_Invoice:
                            DD_update['Reason change not made'][index] = 'No Logical Reason'
                        print('OK')

                    if (Course_Active == 'Active') and not Past_Invoice:
                        DD_update['Change made in Connect?'][index] = 'No'
                        DD_update['Reason change not made'][index] = 'No Logical Reason'
                        print('Change not made')

                else:
                    DD_update['Change made in Connect?'][index] = 'Yes'
                    if Past_Invoice:
                        DD_update['Reason change not made'][index] = 'No Logical Reason'
                    print('OK')

    return DD_update, previous_school, previous_catalog


def check_net_price(row, index, previous_school, previous_catalog, DD_update, driver):
    tenant_id, Catalog = row['Extra_id'], row['Catalog']
    School_change = tenant_id != previous_school
    Catalog_change = Catalog != previous_catalog

    sku = row['SKU']
    start_date = row['Extra_Start Date']
    end_date = row['Extra_End Date']

    net_price = row['Net Price']

    department_name = row['Extra_Section'].split('/-/')[0]
    course_number = row['Extra_Section'].split('/-/')[1]
    section_code = row['Extra_Section'].split('/-/')[2]

    print('{} - {} - {} - {}'.format(tenant_id, Catalog, '-'.join([department_name, course_number,
                                                                   section_code]), sku))
    print(row['Type of Change'])

    if School_change:
        School_Selected = Chrome_navigator.verba_open_school(driver=driver, Verba_School=tenant_id)
    else:
        School_Selected = True

    if School_Selected:
        previous_school = tenant_id
        if School_change or Catalog_change:
            Catalog_Selected = Chrome_navigator.verba_open_catalog(driver=driver, Catalog=Catalog)
        else:
            Catalog_Selected = True

        if Catalog_Selected:
            previous_catalog = Catalog
            schedule_start_date, opt_out_date, invoice_date = Chrome_navigator.verba_dashboard_schedule(driver=driver,
                                                                                                        start_date=start_date,
                                                                                                        end_date=end_date)
            Past_Invoice = False
            if (type(invoice_date) == datetime):
                today = datetime.today().date()
                if today > invoice_date.date():
                    Past_Invoice = True

            Items_Menu_Open = Chrome_navigator.verba_open_item_menu(driver=driver)
            if Items_Menu_Open:
                Item_Open = Chrome_navigator.verba_open_item(driver=driver, sku=sku)
                if Item_Open:
                    Price_checked, connect_net_price, connect_student_price = Chrome_navigator.verba_price(driver=driver)

                    if Price_checked and (net_price == connect_net_price):
                        DD_update['Change made in Connect?'][index] = 'Yes'
                        if Past_Invoice:
                            DD_update['Reason change not made'][index] = 'No Logical Reason'
                        print('OK')

                    elif Price_checked and (net_price != connect_net_price):
                        DD_update['Change made in Connect?'][index] = 'No'
                        DD_update['Reason change not made'][index] = 'No Logical Reason'
                        print('Change not made')
                        if Past_Invoice:
                            DD_update['Change made in Connect?'][index] = 'No Expected Change'
                            DD_update['Reason change not made'][index] = 'After Invoice'
                            print('Past Invoice Date. Dismiss')


    return DD_update, previous_school, previous_catalog


def check_student_price(row, index, previous_school, previous_catalog, DD_update, driver):
    tenant_id, Catalog = row['Extra_id'], row['Catalog']
    School_change = tenant_id != previous_school
    Catalog_change = Catalog != previous_catalog

    sku = row['SKU']
    start_date = row['Extra_Start Date']
    end_date = row['Extra_End Date']

    student_price = row['Student Price']

    department_name = row['Extra_Section'].split('/-/')[0]
    course_number = row['Extra_Section'].split('/-/')[1]
    section_code = row['Extra_Section'].split('/-/')[2]

    print('{} - {} - {} - {}'.format(tenant_id, Catalog, '-'.join([department_name, course_number,
                                                                   section_code]), sku))
    print(row['Type of Change'])

    if School_change:
        School_Selected = Chrome_navigator.verba_open_school(driver=driver, Verba_School=tenant_id)
    else:
        School_Selected = True

    if School_Selected:
        previous_school = tenant_id
        if School_change or Catalog_change:
            Catalog_Selected = Chrome_navigator.verba_open_catalog(driver=driver, Catalog=Catalog)
        else:
            Catalog_Selected = True

        if Catalog_Selected:
            previous_catalog = Catalog
            schedule_start_date, opt_out_date, invoice_date = Chrome_navigator.verba_dashboard_schedule(driver=driver,
                                                                                                        start_date=start_date,
                                                                                                        end_date=end_date)
            Past_Invoice = False
            if (type(invoice_date) == datetime):
                today = datetime.today().date()
                if today > invoice_date.date():
                    Past_Invoice = True

            Items_Menu_Open = Chrome_navigator.verba_open_item_menu(driver=driver)
            if Items_Menu_Open:
                Item_Open = Chrome_navigator.verba_open_item(driver=driver, sku=sku)
                if Item_Open:
                    Price_checked, connect_net_price, connect_student_price = Chrome_navigator.verba_price(driver=driver)

                    if Price_checked and (student_price == connect_student_price):
                        DD_update['Change made in Connect?'][index] = 'Yes'
                        if Past_Invoice:
                            DD_update['Reason change not made'][index] = 'No Logical Reason'
                        print('OK')

                    elif Price_checked and (student_price != connect_student_price):
                        DD_update['Change made in Connect?'][index] = 'No'
                        DD_update['Reason change not made'][index] = 'No Logical Reason'
                        print('Change not made')
                        if Past_Invoice:
                            DD_update['Change made in Connect?'][index] = 'No Expected Change'
                            DD_update['Reason change not made'][index] = 'After Invoice'
                            print('Past Invoice Date. Dismiss')


    return DD_update, previous_school, previous_catalog


def check_start_date(row, index, previous_school, previous_catalog, DD_update, driver):
    tenant_id, Catalog = row['Extra_id'], row['Catalog']
    School_change = tenant_id != previous_school
    Catalog_change = Catalog != previous_catalog

    sku = row['SKU']
    old_start_date = row['Extra_Start Date']
    old_end_date = row['Extra_End Date']
    new_start_date = pd.to_datetime(row['Start Date'], format="%m/%d/%Y").strftime("%Y-%m-%d")

    department_name = row['Extra_Section'].split('/-/')[0]
    course_number = row['Extra_Section'].split('/-/')[1]
    section_code = row['Extra_Section'].split('/-/')[2]

    print('{} - {} - {} - {}'.format(tenant_id, Catalog, '-'.join([department_name, course_number,
                                                                   section_code]), sku))
    print(row['Type of Change'])

    if School_change:
        School_Selected = Chrome_navigator.verba_open_school(driver=driver, Verba_School=tenant_id)
    else:
        School_Selected = True

    if School_Selected:
        previous_school = tenant_id
        if School_change or Catalog_change:
            Catalog_Selected = Chrome_navigator.verba_open_catalog(driver=driver, Catalog=Catalog)
        else:
            Catalog_Selected = True

        if Catalog_Selected:
            previous_catalog = Catalog
            # Check if Active Catalog:
            Catalog_active_button = Chrome_navigator.verba_active_catalog(driver=driver)

            if Catalog_active_button == 'CATALOG ACTIVATED':
                # Si el catalogo esta activo
                # Chequeo las fechas de invoice
                schedule_start_date, opt_out_date, invoice_date = Chrome_navigator.verba_dashboard_schedule(
                    driver=driver,
                    start_date=old_start_date,
                    end_date=old_end_date)
                if (type(invoice_date) == datetime):
                    today = datetime.today().date()

                    # Si estoy antes de invoice:
                    # Chequear start y end date del item
                    # Si fechas mal: NO - Reason: After Catalog Activation - Hacerlo manual
                    # Si fechas bien: Yes - No Logical Reason
                    if today <= invoice_date.date():
                        Items_Menu_Open = Chrome_navigator.verba_open_item_menu(driver=driver)
                        if Items_Menu_Open:
                            Item_Open = Chrome_navigator.verba_open_item(driver=driver, sku=sku)
                            if Item_Open:
                                Course_Active, schedule = Chrome_navigator.verba_active_schedule(driver=driver,
                                                                                                 department_name=department_name,
                                                                                                 course_number=course_number,
                                                                                                 section_code=section_code)

                                if (schedule.split(' - ')[0] == new_start_date):
                                    DD_update['Change made in Connect?'][index] = 'Yes'
                                    DD_update['Reason change not made'][index] = 'No Logical Reason'
                                    print('OK')

                                elif (schedule != None) & (schedule.split(' - ')[0] != new_start_date):
                                    DD_update['Change made in Connect?'][index] = 'No'
                                    DD_update['Reason change not made'][index] = 'After Catalog Activation'
                                    print('OK')

                    # Si estoy despues del invoice:
                    # Chequear start y end date del item
                    # Si fechas estan mal: No expected Change - After Invoice
                    # Si fechas estan bien: Yes - No logical Reason
                    elif today > invoice_date.date():

                        Items_Menu_Open = Chrome_navigator.verba_open_item_menu(driver=driver)
                        if Items_Menu_Open:
                            Item_Open = Chrome_navigator.verba_open_item(driver=driver, sku=sku)
                            if Item_Open:
                                Course_Active, schedule = Chrome_navigator.verba_active_schedule(driver=driver,
                                                                                                 department_name=department_name,
                                                                                                 course_number=course_number,
                                                                                                 section_code=section_code)

                                if (schedule.split(' - ')[0] == new_start_date):
                                    DD_update['Change made in Connect?'][index] = 'Yes'
                                    DD_update['Reason change not made'][index] = 'No Logical Reason'
                                    print('OK')

                                elif (schedule != None) & (schedule.split(' - ')[0] != new_start_date):
                                    DD_update['Change made in Connect?'][index] = 'No Expected Change'
                                    DD_update['Reason change not made'][index] = 'After Invoice'
                                    print('OK')
                else:
                    print('Could not check invoice date')

            elif Catalog_active_button == 'ACTIVATE CATALOG':
                # Chequear start y end date del item
                # Si la fecha esta ok: Yes
                # Si la fecha esta mal: No - No logical Reason

                Items_Menu_Open = Chrome_navigator.verba_open_item_menu(driver=driver)
                if Items_Menu_Open:
                    Item_Open = Chrome_navigator.verba_open_item(driver=driver, sku=sku)
                    if Item_Open:
                        Course_Active, schedule = Chrome_navigator.verba_active_schedule(driver=driver,
                                                                                         department_name=department_name,
                                                                                         course_number=course_number,
                                                                                         section_code=section_code)

                        if (schedule.split(' - ')[0] == new_start_date):
                            DD_update['Change made in Connect?'][index] = 'Yes'
                            print('OK')

                        elif (schedule != None) & (schedule.split(' - ')[0] != new_start_date):
                            DD_update['Change made in Connect?'][index] = 'No'
                            DD_update['Reason change not made'][index] = 'No Logical Reason'
                            print('OK')

            elif Catalog_active_button == 'NOT FOUND':
                print('Active Catalog Button not found')

    return DD_update, previous_school, previous_catalog


def check_end_date(row, index, previous_school, previous_catalog, DD_update, driver):
    tenant_id, Catalog = row['Extra_id'], row['Catalog']
    School_change = tenant_id != previous_school
    Catalog_change = Catalog != previous_catalog

    sku = row['SKU']
    old_start_date = row['Extra_Start Date']
    old_end_date = row['Extra_End Date']
    new_end_date = pd.to_datetime(row['End Date'], format="%m/%d/%Y").strftime("%Y-%m-%d")

    department_name = row['Extra_Section'].split('/-/')[0]
    course_number = row['Extra_Section'].split('/-/')[1]
    section_code = row['Extra_Section'].split('/-/')[2]

    print('{} - {} - {} - {}'.format(tenant_id, Catalog, '-'.join([department_name, course_number,
                                                                   section_code]), sku))
    print(row['Type of Change'])

    if School_change:
        School_Selected = Chrome_navigator.verba_open_school(driver=driver, Verba_School=tenant_id)
    else:
        School_Selected = True

    if School_Selected:
        previous_school = tenant_id
        if School_change or Catalog_change:
            Catalog_Selected = Chrome_navigator.verba_open_catalog(driver=driver, Catalog=Catalog)
        else:
            Catalog_Selected = True

        if Catalog_Selected:
            previous_catalog = Catalog
            # Check if Active Catalog:
            Catalog_active_button = Chrome_navigator.verba_active_catalog(driver=driver)

            if Catalog_active_button == 'CATALOG ACTIVATED':
                # Si el catalogo esta activo
                # Chequeo las fechas de invoice
                schedule_start_date, opt_out_date, invoice_date = Chrome_navigator.verba_dashboard_schedule(
                    driver=driver,
                    start_date=old_start_date,
                    end_date=old_end_date)
                if (type(invoice_date) == datetime):
                    today = datetime.today().date()

                    # Si estoy antes de invoice:
                    # Chequear start y end date del item
                    # Si fechas mal: NO - Reason: After Catalog Activation - Hacerlo manual
                    # Si fechas bien: Yes - No Logical Reason
                    if today <= invoice_date.date():
                        Items_Menu_Open = Chrome_navigator.verba_open_item_menu(driver=driver)
                        if Items_Menu_Open:
                            Item_Open = Chrome_navigator.verba_open_item(driver=driver, sku=sku)
                            if Item_Open:
                                Course_Active, schedule = Chrome_navigator.verba_active_schedule(driver=driver,
                                                                                                 department_name=department_name,
                                                                                                 course_number=course_number,
                                                                                                 section_code=section_code)

                                if (schedule.split(' - ')[1] == new_end_date):
                                    DD_update['Change made in Connect?'][index] = 'Yes'
                                    DD_update['Reason change not made'][index] = 'No Logical Reason'
                                    print('OK')

                                elif (schedule != None) & (schedule.split(' - ')[1] != new_end_date):
                                    DD_update['Change made in Connect?'][index] = 'No'
                                    DD_update['Reason change not made'][index] = 'After Catalog Activation'
                                    print('OK')

                    # Si estoy despues del invoice:
                    # Chequear start y end date del item
                    # Si fechas estan mal: No expected Change - After Invoice
                    # Si fechas estan bien: Yes - No logical Reason
                    elif today > invoice_date.date():

                        Items_Menu_Open = Chrome_navigator.verba_open_item_menu(driver=driver)
                        if Items_Menu_Open:
                            Item_Open = Chrome_navigator.verba_open_item(driver=driver, sku=sku)
                            if Item_Open:
                                Course_Active, schedule = Chrome_navigator.verba_active_schedule(driver=driver,
                                                                                                 department_name=department_name,
                                                                                                 course_number=course_number,
                                                                                                 section_code=section_code)

                                if (schedule.split(' - ')[1] == new_end_date):
                                    DD_update['Change made in Connect?'][index] = 'Yes'
                                    DD_update['Reason change not made'][index] = 'No Logical Reason'
                                    print('OK')

                                elif (schedule != None) & (schedule.split(' - ')[1] != new_end_date):
                                    DD_update['Change made in Connect?'][index] = 'No Expected Change'
                                    DD_update['Reason change not made'][index] = 'After Invoice'
                                    print('OK')
                else:
                    print('Could not check invoice date')

            elif Catalog_active_button == 'ACTIVATE CATALOG':
                # Chequear start y end date del item
                # Si la fecha esta ok: Yes
                # Si la fecha esta mal: No - No logical Reason

                Items_Menu_Open = Chrome_navigator.verba_open_item_menu(driver=driver)
                if Items_Menu_Open:
                    Item_Open = Chrome_navigator.verba_open_item(driver=driver, sku=sku)
                    if Item_Open:
                        Course_Active, schedule = Chrome_navigator.verba_active_schedule(driver=driver,
                                                                                         department_name=department_name,
                                                                                         course_number=course_number,
                                                                                         section_code=section_code)

                        if (schedule.split(' - ')[1] == new_end_date):
                            DD_update['Change made in Connect?'][index] = 'Yes'
                            print('OK')

                        elif (schedule != None) & (schedule.split(' - ')[1] != new_end_date):
                            DD_update['Change made in Connect?'][index] = 'No'
                            DD_update['Reason change not made'][index] = 'No Logical Reason'
                            print('OK')

            elif Catalog_active_button == 'NOT FOUND':
                print('Active Catalog Button not found')

    return DD_update, previous_school, previous_catalog


def check_change(row, index, previous_school, previous_catalog, DD_update, driver):

    if row['Type of Change'] == 'new section':

        DD_update, previous_school, previous_catalog = check_new_section \
            (row=row, index=index, previous_school=previous_school, previous_catalog=previous_catalog,
             DD_update=DD_update, driver=driver)

    elif row['Type of Change'] == 'new item':

        DD_update, previous_school, previous_catalog = check_new_item \
            (row=row, index=index, previous_school=previous_school, previous_catalog=previous_catalog,
             DD_update=DD_update, driver=driver)

    elif row['Type of Change'] == 'additional item':

        DD_update, previous_school, previous_catalog = check_add_item \
            (row=row, index=index, previous_school=previous_school, previous_catalog=previous_catalog,
             DD_update=DD_update, driver=driver)

    elif row['Type of Change'] == 'updated item':

        DD_update, previous_school, previous_catalog = check_add_item \
            (row=row, index=index, previous_school=previous_school, previous_catalog=previous_catalog,
             DD_update=DD_update, driver=driver)

    elif row['Type of Change'] == 'new catalog':

        DD_update, previous_school, previous_catalog = check_new_catalog \
            (row=row, index=index, previous_school=previous_school, previous_catalog=previous_catalog,
             DD_update=DD_update, driver=driver)

    elif row['Type of Change'] == 'deactivated section':

        DD_update, previous_school, previous_catalog = check_deact_section \
            (row=row, index=index, previous_school=previous_school, previous_catalog=previous_catalog,
             DD_update=DD_update, driver=driver)

    elif row['Type of Change'] == 'net price change':

        DD_update, previous_school, previous_catalog = check_net_price \
            (row=row, index=index, previous_school=previous_school, previous_catalog=previous_catalog,
             DD_update=DD_update, driver=driver)

    elif row['Type of Change'] == 'student price change':

        DD_update, previous_school, previous_catalog = check_student_price \
            (row=row, index=index, previous_school=previous_school, previous_catalog=previous_catalog,
             DD_update=DD_update, driver=driver)

    elif row['Type of Change'] == 'start date change':

        DD_update, previous_school, previous_catalog = check_start_date \
            (row=row, index=index, previous_school=previous_school, previous_catalog=previous_catalog,
             DD_update=DD_update, driver=driver)

    elif row['Type of Change'] == 'end date change':

        DD_update, previous_school, previous_catalog = check_end_date \
            (row=row, index=index, previous_school=previous_school, previous_catalog=previous_catalog,
             DD_update=DD_update, driver=driver)

    return DD_update, previous_school, previous_catalog


def run(DD_update, driver, total_count=5):

    # Define run parameters
    count = 0
    missing_rows = DD_update['Change made in Connect?'].isna().sum() - \
                   len(DD_update.loc[(DD_update['Type of Change'] == 'new enrollment') &
                                     (DD_update['Change made in Connect?'] != 'Report')]) - \
                   len(DD_update.loc[(DD_update['Type of Change'] == 'deactivated enrollment') &
                                     (DD_update['Change made in Connect?'] != 'Report')]) - \
                   len(DD_update.loc[(DD_update['Type of Change'] == 'new schedule') &
                                     (DD_update['Change made in Connect?'] != 'Report')])
    previous_school = ''
    previous_catalog = ''

    # Check run time
    startTime = datetime.now()
    # Check cases
    while missing_rows and count < total_count:
        case = 0
        for index, row in DD_update.iterrows():
            skip = (type(row['Change made in Connect?']) == str) or (row['Type of Change'] == 'new enrollment') or \
                   (row['Type of Change'] == 'deactivated enrollment') or (row['Type of Change'] == 'new schedule')
            if not skip:
                case += 1
                print('\nCase {} of {}\nTime elapsed: {}'.format(case, missing_rows,
                                                                  str(datetime.now() - startTime).split('.')[0]))
                DD_update, previous_school, previous_catalog = check_change(row=row, index=index,
                                                                            previous_school=previous_school,
                                                                            previous_catalog=previous_catalog,
                                                                            DD_update=DD_update, driver=driver)

        missing_rows = DD_update['Change made in Connect?'].isna().sum() - \
                       len(DD_update.loc[(DD_update['Type of Change'] == 'new enrollment') &
                                         (DD_update['Change made in Connect?'] != 'Report')]) - \
                       len(DD_update.loc[(DD_update['Type of Change'] == 'deactivated enrollment') &
                                         (DD_update['Change made in Connect?'] != 'Report')]) - \
                       len(DD_update.loc[(DD_update['Type of Change'] == 'new schedule') &
                                         (DD_update['Change made in Connect?'] != 'Report')])
        count += 1
        if missing_rows:
            print('\n{}. Waiting to re-run on {} unchecked cases...'.format(count, missing_rows))
            # driver.refresh()
            # time.sleep(5)
            driver.back()
            time.sleep(5)
            previous_school = ''
            previous_catalog = ''
    print('\nTotal run time: {}'.format(str(datetime.now() - startTime).split('.')[0]))

    return DD_update
