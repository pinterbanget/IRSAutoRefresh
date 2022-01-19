import time
from selenium import webdriver

BLACK = "#121212"
USERNAME = "pinterbanget"           # replace with your SIAK-NG username
PASSWORD = "iloveyou"               # replace with your SIAK-NG password
BROWSER_PICK = "Firefox"            # replace with your browser of choice (Edge, Firefox, Chrome)
EXEC_PATH = "C:\geckodriver.exe"    # replace with driver executable and directory


def get_site(site, browser):
    while True:
        try:
            time.sleep(0.3)
            browser.get(site)
            break
        except:
            continue


def login_siak(user, password, browser):
    get_site('http://academic.ui.ac.id', browser)
    try:
        user_field = browser.find_element_by_css_selector('#u')
        user_field.send_keys(user)
        pass_field = browser.find_element_by_css_selector('#login > form:nth-child(3) > p:nth-child(2) > input:nth-child(2)')
        pass_field.send_keys(password)
        login_button = browser.find_element_by_css_selector('#submit > input:nth-child(1)')
        login_button.click()
        time.sleep(3)
        try:
            browser.find_element_by_css_selector('#login > p')
            print('Wrong username or password.')
        except:
            pass

    except:
        login_siak(user, password, browser)


def buka_irs(user, password, browser):
    get_site('http://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit', browser)
    while True:
        try:
            browser.find_element_by_css_selector('#c0')
            break
        except:
            try:
                browser.find_element_by_css_selector('#login > form:nth-child(3) > p:nth-child(2) > input:nth-child(2)')
                login_siak(user, password, browser)
                time.sleep(2)
                get_site('http://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit', browser)
            except:
                time.sleep(20)
                try:
                    browser.refresh()
                except:
                    continue


if __name__ == '__main__':
    username = USERNAME
    password = PASSWORD
    browser_pick = BROWSER_PICK.lower()
    try:
        if browser_pick == 'chrome':
            browser = webdriver.Chrome(executable_path=EXEC_PATH)
        elif browser_pick == 'edge':
            browser = webdriver.Edge(executable_path=EXEC_PATH)
        else:
            browser = webdriver.Firefox(executable_path=EXEC_PATH)

        login_siak(username, password, browser)
        buka_irs(username, password, browser)
        print('Your IRS can now be filled.')

    except Exception as e:
        print('An error has occurred.\n{e}')
