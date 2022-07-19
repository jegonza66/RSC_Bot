import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime


def verba_connect_login(Credentials):
    Verba_Username = Credentials['Verba_Username']
    Verba_Password = Credentials['Verba_Password']

    # Open driver
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # Open the website
    driver.get('https://verbaconnect.com/auth/vst/login')

    # Login to Verba Connect
    # Select the id box
    id_box = driver.find_element_by_id('username')
    # Send id information
    id_box.send_keys(Verba_Username)

    # Find password box
    pass_box = driver.find_element_by_id('password')
    # Send password
    pass_box.send_keys(Verba_Password)

    # Find login button
    login_button_css = 'button[type="submit"]'
    login_button = driver.find_element_by_css_selector(login_button_css)
    # Click login
    login_button.click()

    # Check if successfull login
    try:
        Dashboard_xpath = '/ html / body / div[1] / div / nav / div[1] / a[2]'
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, Dashboard_xpath)))
        time.sleep(3)
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, Dashboard_xpath))).click()
    except:
        input('\nVerification step needed to complete login.\n'
              'Please complete verification and press Enter to continue.')
    driver.maximize_window()

    return driver


def verba_open_school(driver, Verba_School):
    School_Selected = False
    # select school
    try:
        # Open school menu
        drop_down_xpath = '/ html / body / div[1] / div / nav / div[2] / div[1] / div[1]'
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, drop_down_xpath)))
        drop_down_menu = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, drop_down_xpath)))
        drop_down_menu.click()

        school_menu_xpath = '/ html / body / div[1] / div / nav / div[2] / div[1] / div[2] / div / div[1] / div / select'
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, school_menu_xpath)))
        school_menu = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, school_menu_xpath)))
        school_menu_select = Select(school_menu)
        school_menu_select.select_by_visible_text(Verba_School)
        School_Selected = True
        print('School Selected')
    except:
        # Try Again
        time.sleep(2)
        try:
            # Open school menu
            drop_down_xpath = '/ html / body / div[1] / div / nav / div[2] / div[1] / div[1]'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, drop_down_xpath)))
            drop_down_menu = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, drop_down_xpath)))
            drop_down_menu.click()

            school_menu_xpath = '/ html / body / div[1] / div / nav / div[2] / div[1] / div[2] / div / div[1] / div / select'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, school_menu_xpath)))
            school_menu = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, school_menu_xpath)))
            school_menu_select = Select(school_menu)
            school_menu_select.select_by_visible_text(Verba_School)
            School_Selected = True
            print('School Selected')
        except:
            print('Could not Open School')
            driver.refresh()
            time.sleep(3)

    return School_Selected


def verba_open_catalog(driver, Catalog):

    Catalog_Selected = False
    # Select Catalog
    try:
        # Find and click on list of catalogs
        catalog_menu_xpath = '/ html / body / div[1] / div / nav / div[1] / div[1] / div[1]'
        # Click catalog drop down menu
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, catalog_menu_xpath)))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, catalog_menu_xpath))).click()
        # Select catalog
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.LINK_TEXT, str(Catalog).upper())))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, str(Catalog).upper()))).click()

        Catalog_Selected = True
        print('Catalog Selected')
    except:
        # Try Again
        time.sleep(2)
        try:
            # Find and click on list of catalogs
            catalog_menu_xpath = '/ html / body / div[1] / div / nav / div[1] / div[1] / div[1]'
            # Click catalog drop down menu
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, catalog_menu_xpath)))
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, catalog_menu_xpath))).click()
            # Select catalog
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.LINK_TEXT, str(Catalog).upper())))
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, str(Catalog).upper()))).click()

            Catalog_Selected = True
            print('Catalog Selected')
        except:
            print('Could not find Catalog name')
            driver.refresh()
            time.sleep(3)

    return Catalog_Selected


def verba_open_item_menu(driver):
    Items_Menu_Open = False
    # Open Items Menu
    try:
        Items_xpath = '/ html / body / div[1] / div / nav / div[1] / div[2] / a / div'
        Items_tab = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, Items_xpath)))
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Items_xpath))).click()
        ActionChains(driver).move_to_element(Items_tab).perform()
        # click connect items tab
        connect_tab_xpath = '/ html / body / div[1] / div / nav / div[1] / div[2] / div / div / a[1]'
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, connect_tab_xpath)))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, connect_tab_xpath))).click()
        # Click search bar to chek if open
        search_bar_xpath = '/ html / body / div[1] / div / div[1] / div[3] / div / div / div[1] / div[1] / input'
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, search_bar_xpath)))
        search_item = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, search_bar_xpath)))
        search_item.click()
        Items_Menu_Open = True
        print('Items Menu Open')
    except:
        time.sleep(1)
        # Try again
        try:
            Items_xpath = '/ html / body / div[1] / div / nav / div[1] / div[2] / a / div'
            Items_tab = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, Items_xpath)))
            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Items_xpath))).click()
            ActionChains(driver).move_to_element(Items_tab).perform()
            # click connect items tab
            connect_tab_xpath = '/ html / body / div[1] / div / nav / div[1] / div[2] / div / div / a[1]'
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, connect_tab_xpath)))
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, connect_tab_xpath))).click()
            # Click search bar to chek if open
            search_bar_xpath = '/ html / body / div[1] / div / div[1] / div[3] / div / div / div[1] / div[1] / input'
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, search_bar_xpath)))
            search_item = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, search_bar_xpath)))
            search_item.click()
            Items_Menu_Open = True
            print('Items Menu Open')
        except:
            print('Could not Open Items Menu')
            driver.refresh()
            time.sleep(3)
   
    return Items_Menu_Open


def verba_open_item(driver, sku):
    Item_Open = False
    # Search and open Item
    try:
        search_bar_xpath = '/ html / body / div[1] / div / div[1] / div[3] / div / div / div[1] / div[1] / input'
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, search_bar_xpath)))
        search_item = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, search_bar_xpath)))
        search_item.clear()
        search_item.send_keys(sku)

        search_button = '/ html / body / div[1] / div / div[1] / div[3] / div / div / div[1] / div[2] / button'
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, search_button)))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, search_button))).click()

        # Search all items matching SKU, and open first
        item = driver.find_elements(By.XPATH, "//span[text() = '{}']".format(sku))[0]
        div = item.find_element(By.XPATH, '..')
        div2 = div.find_element(By.XPATH, '..')
        h3 = div2.find_element(By.XPATH, './/h3[@class = "src-library-ItemInfo-View-title"]')
        a = h3.find_element(By.XPATH, './/a').click()

        Item_Open = True
        print('Item Open')
    except:
        time.sleep(1)
        # Try Again
        try:
            search_bar_xpath = '/ html / body / div[1] / div / div[1] / div[3] / div / div / div[1] / div[1] / input'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, search_bar_xpath)))
            search_item = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, search_bar_xpath)))
            search_item.clear()
            search_item.send_keys(sku)

            search_button = '/ html / body / div[1] / div / div[1] / div[3] / div / div / div[1] / div[2] / button'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, search_button)))
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, search_button))).click()

            # Search all items matching SKU, and open first
            item = driver.find_elements(By.XPATH, "//span[text() = '{}']".format(sku))[0]
            div = item.find_element(By.XPATH, '..')
            div2 = div.find_element(By.XPATH, '..')
            h3 = div2.find_element(By.XPATH, './/h3[@class = "src-library-ItemInfo-View-title"]')
            a = h3.find_element(By.XPATH, './/a').click()

            Item_Open = True
            print('Item Open')
        except:
            time.sleep(2)
            try:
                search_bar_xpath = '/ html / body / div[1] / div / div[1] / div[3] / div / div / div[1] / div[1] / input'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, search_bar_xpath)))
                search_item = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, search_bar_xpath)))
                search_item.clear()
                search_item.send_keys(sku)

                search_button = '/ html / body / div[1] / div / div[1] / div[3] / div / div / div[1] / div[2] / button'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, search_button)))
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, search_button))).click()

                # Search all items matching SKU, and open first
                item = driver.find_elements(By.XPATH, "//span[text() = '{}']".format(sku))[0]
                div = item.find_element(By.XPATH, '..')
                div2 = div.find_element(By.XPATH, '..')
                h3 = div2.find_element(By.XPATH, './/h3[@class = "src-library-ItemInfo-View-title"]')
                a = h3.find_element(By.XPATH, './/a').click()

                Item_Open = True
                print('Item Open')
            except:
                print('Could not Open Item')

    return Item_Open


def verba_active_schedule(driver, department_name, course_number, section_code):
    Course_Status = 'NOT FOUND'
    schedule = None

    try:
        time.sleep(1)
        # Find department and course
        WebDriverWait(driver, 2).until(
            EC.visibility_of_all_elements_located((
                By.XPATH, '//a[text()= "{}"]'.format(' '.join([department_name, course_number])))))
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((
                By.XPATH, '//a[text()= "{}"]'.format(' '.join([department_name, course_number])))))
        h3s = driver.find_elements(By.XPATH, '//a[text()= "{}"]'.format(' '.join([department_name, course_number])))

        if len(h3s):
            print('Course found')
            Section_found = False
            for h3 in h3s:
                if not Section_found:
                    # Get div containing 'Active/Inactive' Button
                    div_course = h3.find_element(By.XPATH, '..').find_element(By.XPATH, '..')
                    try:
                        # Find section within dpt and course
                        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, './/h4[text()= "{}"]'.format(section_code))))
                        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, './/h4[text()= "{}"]'.format(section_code))))
                        h4 = div_course.find_element(By.XPATH, './/h4[text()= "{}"]'.format(section_code))
                        # Get div containing group and schedule info
                        div_div = div_course.find_element(By.XPATH, '..').find_element(By.XPATH, '..')
                        # Get group name
                        try:
                            Group_name = div_div.find_element(By.XPATH, './/h3[contains(text(), "Group")]'.format(section_code)).text
                        except:
                            Group_name = div_div.find_element(By.XPATH, './/h3[contains(text(), "Non-Participating")]'.format(
                                section_code)).text
                        Section_found = True
                        print('Section found:')
                        # Get schedule
                        try:
                            schedules_menu = Select(WebDriverWait(div_div, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, "select"))))
                            schedule = schedules_menu.first_selected_option.text
                            print(Group_name + '\n' + schedule)
                        except:
                            print(Group_name + '\nCould not get schedule')
                    except:
                        pass

        if not Section_found:
            print('Section not found')
        elif Section_found:
            # Check if Active
            div = h4.find_element(By.XPATH, '..')
            li = div.find_element(By.XPATH, '..')
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, './/div[@class = "src-shared-Badge-wrapper"]')))
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, './/div[@class = "src-shared-Badge-wrapper"]')))
            button = li.find_elements(By.XPATH, './/div[@class = "src-shared-Badge-wrapper"]')[0]
            button.click()
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, './/span[@class = "src-shared-Badge-value"]')))
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, './/span[@class = "src-shared-Badge-value"]')))
            Course_Status = button.find_elements(By.XPATH, './/span[@class = "src-shared-Badge-value"]')[0].get_attribute("textContent")
            print(Course_Status)

            if schedule == None:
                # Check Schedule again just in case
                try:
                    ul = li.find_element(By.XPATH, '..')
                    div1 = ul.find_element(By.XPATH, '..')
                    div2 = div1.find_element(By.XPATH, '..')
                    div3 = div2.find_element(By.XPATH, '..')

                    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, "select")))
                    schedules_menu = Select(WebDriverWait(div3, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, "select"))))
                    schedule = schedules_menu.first_selected_option.text
                except:
                    print('Could not get schedule')
    except:
        time.sleep(2)
        try:
            time.sleep(1)
            # Find department and course
            WebDriverWait(driver, 2).until(
                EC.visibility_of_all_elements_located((By.XPATH, '//a[text()= "{}"]'.format(' '.join([department_name, course_number])))))
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, '//a[text()= "{}"]'.format(' '.join([department_name, course_number])))))
            h3s = driver.find_elements(By.XPATH, '//a[text()= "{}"]'.format(' '.join([department_name, course_number])))

            if len(h3s):
                print('Course found')
                Section_found = False
                for h3 in h3s:
                    if not Section_found:
                        # Get div containing 'Active/Inactive' Button
                        div_course = h3.find_element(By.XPATH, '..').find_element(By.XPATH, '..')
                        try:
                            # Find section within dpt and course
                            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, './/h4[text()= "{}"]'.format(section_code))))
                            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, './/h4[text()= "{}"]'.format(section_code))))
                            h4 = div_course.find_element(By.XPATH, './/h4[text()= "{}"]'.format(section_code))
                            # Get div containing group and schedule info
                            div_div = div_course.find_element(By.XPATH, '..').find_element(By.XPATH, '..')
                            # Get group name
                            try:
                                Group_name = div_div.find_element(By.XPATH, './/h3[contains(text(), "Group")]'.format(
                                    section_code)).text
                            except:
                                Group_name = div_div.find_element(By.XPATH,
                                                                  './/h3[contains(text(), "Non-Participating")]'.format(
                                                                      section_code)).text
                            Section_found = True
                            print('Section found:')
                            # Get schedule
                            try:
                                schedules_menu = Select(WebDriverWait(div_div, 3).until(
                                    EC.element_to_be_clickable((By.CLASS_NAME, "select"))))
                                schedule = schedules_menu.first_selected_option.text
                                print(Group_name + '\n' + schedule)
                            except:
                                print(Group_name + '\nCould not get schedule')
                        except:
                            pass

            if not Section_found:
                print('Section not found')
            elif Section_found:
                # Check if Active
                div = h4.find_element(By.XPATH, '..')
                li = div.find_element(By.XPATH, '..')
                WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, './/div[@class = "src-shared-Badge-wrapper"]')))
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, './/div[@class = "src-shared-Badge-wrapper"]')))
                button = li.find_elements(By.XPATH, './/div[@class = "src-shared-Badge-wrapper"]')[0]
                button.click()
                WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, './/span[@class = "src-shared-Badge-value"]')))
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, './/span[@class = "src-shared-Badge-value"]')))
                Course_Status = button.find_elements(By.XPATH, './/span[@class = "src-shared-Badge-value"]')[0].get_attribute("textContent")
                print(Course_Status)
                if schedule == None:
                    # Check Schedule again just in case
                    try:
                        ul = li.find_element(By.XPATH, '..')
                        div1 = ul.find_element(By.XPATH, '..')
                        div2 = div1.find_element(By.XPATH, '..')
                        div3 = div2.find_element(By.XPATH, '..')

                        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, "select")))
                        schedules_menu = Select(WebDriverWait(div3, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, "select"))))
                        schedule = schedules_menu.first_selected_option.text
                    except:
                        print('Could not get schedule')
        except:
            print('Section not found')

    return Course_Status, schedule


def verba_price(driver):
    net_price = None
    student_price = None
    time.sleep(1)
    try:
        pricing_xpath = '/ html / body / div[1] / div / div[1] / div / div[3] / div / ul / li[2] / a'
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, pricing_xpath)))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, pricing_xpath))).click()

        try:
            net_price_xpath = '/ html / body / div[1] / div / div[1] / div / div[3] / div / div / div / div / div[2] / div[1] / div[2]'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, net_price_xpath)))
            net_price = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, net_price_xpath))).text.split('$')[1]
            net_price = float(net_price)
        except:
            net_price_xpath = '/ html / body / div[1] / div / div[1] / div / div[3] / div / div / div / div / div[2] / div[1] / div[2] / div / input'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, net_price_xpath)))
            net_price = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, net_price_xpath))).get_attribute('value')
            net_price = float(net_price)

        student_price_xpath = '/ html / body / div[1] / div / div[1] / div / div[3] / div / div / div / div / div[1] / div / div / h3 / span'
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, student_price_xpath)))
        student_price = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, student_price_xpath))).text.split('$')[1]

        print('Net Price: {}\n'
              'Student Price: {}'.format(float(net_price), float(student_price)))
        print('Price checked correctly')
        Price_checked = True

        return Price_checked, float(net_price), float(student_price)

    except:
        time.sleep(2)
        try:
            pricing_xpath = '/ html / body / div[1] / div / div[1] / div / div[3] / div / ul / li[2] / a'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, pricing_xpath)))
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, pricing_xpath))).click()

            try:
                net_price_xpath = '/ html / body / div[1] / div / div[1] / div / div[3] / div / div / div / div / div[2] / div[1] / div[2]'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, net_price_xpath)))
                net_price = \
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, net_price_xpath))).text.split('$')[
                    1]
                net_price = float(net_price)
            except:
                net_price_xpath = '/ html / body / div[1] / div / div[1] / div / div[3] / div / div / div / div / div[2] / div[1] / div[2] / div / input'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, net_price_xpath)))
                net_price = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, net_price_xpath))).get_attribute('value')
                net_price = float(net_price)

            student_price_xpath = '/ html / body / div[1] / div / div[1] / div / div[3] / div / div / div / div / div[1] / div / div / h3 / span'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, student_price_xpath)))
            student_price = \
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, student_price_xpath))).text.split('$')[
                1]

            print('Net Price: {}\n'
                  'Student Price: {}'.format(float(net_price), float(student_price)))
            Price_checked = True
            print('Price checked correctly')

            return Price_checked, float(net_price), float(student_price)

        except:
            Price_checked = False
            print('Could not get prices')
            driver.refresh()
            time.sleep(3)
            return Price_checked, net_price, student_price


def verba_dashboard_schedule(driver, start_date, end_date):
    opt_out_date = 'NOT FOUND'
    invoice_date = 'NOT FOUND'
    schedule_start_date = 'NOT FOUND'
    time.sleep(1)
    count = 0
    while type(opt_out_date) == str or type(invoice_date) == str or type(schedule_start_date) == str and count < 2:
        count += 1
        try:
            # Open Dashboard
            Dashboard_xpath = '/ html / body / div[1] / div / nav / div[1] / a[2]'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, Dashboard_xpath)))
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, Dashboard_xpath))).click()

            # Find schedule
            h3 = driver.find_element(By.XPATH, '//h3[text()= "{}"]'.format(' - '.join([start_date, end_date])))
            div = h3.find_element(By.XPATH, '..')

            # Find shcedule start
            schedule_start_text = div.find_element(By.XPATH, './/h5[text()= "Schedule Start"]')
            # Find opt out date
            div_schedule_start = schedule_start_text.find_element(By.XPATH, '..')
            schedule_start_date_text = div_schedule_start.find_element(By.CLASS_NAME, "src-dashboard-page-ScheduleStats-DateDot-View-date").text.split('\n')

            # Find opt out
            opt_out_text = div.find_element(By.XPATH, './/h5[text()= "Opt-Outs End"]')
            #Find opt out date
            div_opt_out = opt_out_text.find_element(By.XPATH, '..')
            opt_out_date_text = div_opt_out.find_element(By.CLASS_NAME, "src-dashboard-page-ScheduleStats-DateDot-View-date").text.split('\n')

            # Find invoice
            invoice_text = div.find_element(By.XPATH, './/h5[text()= "Invoice Issued"]')
            # Find Invoice date
            div_invoice = invoice_text.find_element(By.XPATH, '..')
            invoice_date_text = div_invoice.find_element(By.CLASS_NAME,
                                                         "src-dashboard-page-ScheduleStats-DateDot-View-date").text.split('\n')
            # Take start date year asuming invoice date is the same year.
            year = datetime.strptime(start_date, '%Y-%m-%d').year
            schedule_start_date = datetime.strptime('-'.join([str(year), schedule_start_date_text[0], schedule_start_date_text[1]]), "%Y-%B-%d")
            opt_out_date = datetime.strptime('-'.join([str(year), opt_out_date_text[0], opt_out_date_text[1]]), "%Y-%B-%d")
            invoice_date = datetime.strptime('-'.join([str(year), invoice_date_text[0], invoice_date_text[1]]), "%Y-%B-%d")
            # If opt out or invoice dates are earlier than start date, add one year
            if opt_out_date < schedule_start_date:
                opt_out_date = datetime.strptime('-'.join([str(year+1), opt_out_date_text[0], opt_out_date_text[1]]), "%Y-%B-%d")
                invoice_date = datetime.strptime('-'.join([str(year+1), invoice_date_text[0], invoice_date_text[1]]), "%Y-%B-%d")
            elif invoice_date < schedule_start_date:
                invoice_date = datetime.strptime('-'.join([str(year+1), invoice_date_text[0], invoice_date_text[1]]),"%Y-%B-%d")
            print('Invoice date: {}'.format(invoice_date))
            print('Opt out date: {}'.format(opt_out_date))
        except:
            time.sleep(2)
            continue
    if type(opt_out_date) == str or type(invoice_date) == str or type(schedule_start_date) == str:
        print('Could not find Opt Out and Invoice Dates')
        driver.refresh()
        time.sleep(3)

    return schedule_start_date, opt_out_date, invoice_date


def verba_active_catalog(driver):
    div_button_text = 'NOT FOUND'

    try:
        # Open Dashboard
        Dashboard_xpath = '/ html / body / div[1] / div / nav / div[1] / a[2]'
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, Dashboard_xpath)))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, Dashboard_xpath))).click()
        # Check if Active Catalog:
        div_button_text = driver.find_element(By.CLASS_NAME, 'src-dashboard-page-Activation-View-activation').text

    except:
        time.sleep(2)
        try:
            # Open Dashboard
            Dashboard_xpath = '/ html / body / div[1] / div / nav / div[1] / a[2]'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, Dashboard_xpath)))
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, Dashboard_xpath))).click()
            # Check if Active Catalog:
            div_button_text = driver.find_element(By.CLASS_NAME, 'src-dashboard-page-Activation-View-activation').text

        except:
            print('Could not check if Catalog Active')
            driver.refresh()
            time.sleep(3)

    return div_button_text

def verba_ask_report(driver, tenant_id, Catalog):
    Asked_for_report = False

    try:
        # Open Reports
        Reports_xpath = '/ html / body / div[1] / div / nav / div[1] / a[6]'
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, Reports_xpath)))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, Reports_xpath))).click()

        # Click email report button
        '/ html / body / div[1] / div / div[1] / div / div[2] / div / div / div[3] / div[2] / div / button'
        email_report_button_xpath = '/ html / body / div[1] / div / div[1] / div / div[2] / div / div / div[3] / div[2] / div / button'
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, email_report_button_xpath)))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, email_report_button_xpath))).click()

        Asked_for_report = True
    except:
        time.sleep(2)
        try:
            # Open Reports
            Reports_xpath = '/ html / body / div[1] / div / nav / div[1] / a[6]'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, Reports_xpath)))
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, Reports_xpath))).click()

            # Click email report button
            '/ html / body / div[1] / div / div[1] / div / div[2] / div / div / div[3] / div[2] / div / button'
            email_report_button_xpath = '/ html / body / div[1] / div / div[1] / div / div[2] / div / div / div[3] / div[2] / div / button'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, email_report_button_xpath)))
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, email_report_button_xpath))).click()

            Asked_for_report = True
        except:
            print('Could not Ask for report')
            driver.refresh()
            time.sleep(3)

    return Asked_for_report



# def verba_connect_attempt_login(Credentials):
#     Verba_Username = Credentials['Verba_Username']
#     Verba_Password = Credentials['Verba_Password']
#
#     # Login to Verba Connect
#     driver = webdriver.Chrome(ChromeDriverManager().install())
#     # Open the website
#     driver.get('https://verbaconnect.com/auth/vst/login')
#
#     # Select the id box
#     id_box = driver.find_element(By.ID, 'username')
#     # Send id information
#     id_box.send_keys(Verba_Username)
#
#     # Find password box
#     pass_box = driver.find_element(By.ID, 'password')
#     # Send password
#     pass_box.send_keys(Verba_Password)
#
#     # Find login button
#     login_button_css = 'button[type="submit"]'
#     login_button = driver.find_element(By.CSS_SELECTOR, login_button_css)
#     # Click login
#     login_button.click()
#
#     return driver
#
#
# def verba_connect_login(Credentials):
#     # Check if successful login
#     Login = False
#     count = 0
#     total_count = 5
#     while not Login and count < total_count:
#         count += 1
#         driver = verba_connect_attempt_login(Credentials)
#         Dashboard_xpath = '/ html / body / div[1] / div / nav / div[1] / a[2]'
#         try:
#             WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, Dashboard_xpath)))
#             time.sleep(2)
#             WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, Dashboard_xpath))).click()
#             print('Successful login')
#             driver.maximize_window()
#             Login = True
#         except:
#             pass
#             try:
#                 print('\nVerification step needed to complete login.\n'
#                       'Please complete verification to continue.')
#                 # Check if successful manual login
#                 WebDriverWait(driver, 2*60).until(EC.visibility_of_element_located((By.XPATH, Dashboard_xpath)))
#                 time.sleep(2)
#                 WebDriverWait(driver, 2*60).until(EC.element_to_be_clickable((By.XPATH, Dashboard_xpath))).click()
#                 print('\nSuccessful login')
#                 driver.maximize_window()
#                 Login = True
#             except:
#                 if count < total_count:
#                     print('\nTimed out. Retrying login')
#                     driver.close()
#                     time.sleep(2 * 60)
#     if not Login:
#         # wait to complete captcha and press enter
#         input('Once verification completed, press Enter to continue')
#         # Check if successful manual login
#         WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, Dashboard_xpath)))
#         time.sleep(2)
#         WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, Dashboard_xpath))).click()
#         print('Successful login')
#         driver.maximize_window()
#
#     return driver