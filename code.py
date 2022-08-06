import os
import sys
import time
from tkinter import *
from tkinter import messagebox, ttk, Button
from selenium import webdriver
from selenium.webdriver.common.by import By

BLACK = "#121212"
ISI_IRS_URL = 'https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit'
REFRESH_TIME = 20
WAIT_TIME = 3


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_site(site, browser):
    while True:
        try:
            time.sleep(WAIT_TIME/10)
            browser.get(site)
            break
        except:
            continue


def relog_siak(user, password, browser, url):
    browser.find_element(By.CSS_SELECTOR, '#login > form:nth-child(3) > p:nth-child(2) > input:nth-child(2)')
    login_siak(user, password, browser)
    time.sleep(WAIT_TIME)
    get_site(url, browser)


def login_siak(user, password, browser):
    get_site('http://academic.ui.ac.id', browser)
    try:
        user_field = browser.find_element(By.CSS_SELECTOR, '#u')
        user_field.send_keys(user)
        pass_field = browser.find_element(By.CSS_SELECTOR, '#login > form:nth-child(3) > p:nth-child(2) > input:nth-child(2)')
        pass_field.send_keys(password)
        login_button = browser.find_element(By.CSS_SELECTOR, '#submit > input:nth-child(1)')
        login_button.click()
        time.sleep(WAIT_TIME)
        try:
            browser.find_element(By.CSS_SELECTOR, '#login > p')
            messagebox.showerror(title='Data Incorrect',
                                 message='Username and/or Password incorrect.\nPlease check your data.')
            sys.exit()
        except:
            pass

    except:
        time.sleep(WAIT_TIME)
        login_siak(user, password, browser)


def buka_irs(user, password, browser):
    get_site(ISI_IRS_URL, browser)
    while True:
        try:
            browser.find_element(By.CSS_SELECTOR, '#c0')
            break
        except:
            try:
                relog_siak(user, password, browser, url=ISI_IRS_URL)
            except:
                time.sleep(REFRESH_TIME)
                try:
                    browser.refresh()
                except:
                    continue


def main():
    browser_pick = dropdown_selection.get()
    username = username_entry.get()
    password = password_entry.get()
    if username != '' and password != '' and browser_pick != '(Select your browser...)':
        try:
            if browser_pick == 'Chrome':
                from webdriver_manager.chrome import ChromeDriverManager
                from selenium.webdriver.chrome.service import Service as ChromeService
                browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            elif browser_pick == 'Edge':
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                from selenium.webdriver.edge.service import Service as EdgeService
                browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            else:
                from webdriver_manager.firefox import GeckoDriverManager
                from selenium.webdriver.firefox.service import Service as FirefoxService
                browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

            login_siak(username, password, browser)
            buka_irs(username, password, browser)
            messagebox.showinfo(title='IRS Ready', message='Your IRS can now be filled.\n')

        except Exception as e:
            messagebox.showerror(title='Error', message=f'An error has occurred.\n\n{e}')

    else:
        messagebox.showerror(title='Form Incomplete', message='Please complete your form.')


if __name__ == '__main__':
    window = Tk()

    logo = PhotoImage(file=resource_path("Logo.png"))
    icon = PhotoImage(file=resource_path("Icon.png"))

    window.title(f'IRS Auto Refresh 0.9.5')
    window.configure(padx=30, pady=30, background=BLACK)
    window.iconphoto(False, icon)
    window.maxsize(width=319, height=430)
    window.minsize(width=319, height=430)

    canvas = Canvas(width=256, height=256, background=BLACK, highlightthickness=0)
    canvas.create_image(128, 128, image=logo)
    canvas.grid(column=0, row=0, columnspan=3, sticky='w')

    username_label = Label(text='Username:', font=('Arial', 12, 'normal'), foreground='White', background=BLACK, anchor='e')
    username_label.grid(column=0, row=1, sticky='w', padx=2, pady=2)

    password_label = Label(text='Password:', font=('Arial', 12, 'normal'), foreground='White', background=BLACK, anchor='e')
    password_label.grid(column=0, row=2, sticky='w', padx=2, pady=2, columnspan=1)

    browser_label = Label(text='Browser:', font=('Arial', 12, 'normal'), foreground='White', background=BLACK, anchor='e')
    browser_label.grid(column=0, row=3, sticky='w', padx=2, pady=2, columnspan=1)

    username_entry = Entry(width=27)
    username_entry.grid(column=1, row=1, columnspan=2, sticky='w', padx=2, pady=2)

    password_entry = Entry(width=27, show='*')
    password_entry.grid(column=1, row=2, sticky='w', padx=2, pady=2, columnspan=2)

    dropdown_value = StringVar(window)
    dropdown_value.set('(Select your browser...)')

    current_data = {'Firefox (recommended)': 'C:\geckodriver.exe', 'Chrome': 'C:\chromedriver.exe',
                    'Edge': 'C:\msedgedriver.exe'}

    dropdown_selection = ttk.Combobox(window, textvariable=dropdown_value)
    dropdown_selection['values'] = list(current_data.keys())
    dropdown_selection['state'] = 'readonly'
    dropdown_selection.configure(width=24, height=1)
    dropdown_selection.grid(column=1, row=3, sticky='w', padx=2, pady=2, columnspan=2)

    submit_button = Button(text='Run', command=main, highlightthickness=0, width=23)
    submit_button.grid(column=1, row=4, sticky='w', padx=2, pady=2, columnspan=2)

    window.mainloop()
