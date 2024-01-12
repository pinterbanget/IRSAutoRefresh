import os
import sys
import time
import tkinter as tk
from tkinter import messagebox, ttk, Button
from datetime import date, datetime, timedelta
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.common.by import By

VERSION_NAME = "IRS Auto Refresh 0.9.7"
BASE_COLOR = "#121212"

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(CURR_DIR, "assets", "Icon.png")
LOGO_PATH = os.path.join(CURR_DIR, "assets", "Logo.png")

MONTH = date.today().month
CORRECT_TERM = 2 if MONTH > 6 else 1

MAIN_URL = 'https://academic.ui.ac.id'
ISI_IRS_URL = f'{MAIN_URL}/main/CoursePlan/CoursePlanEdit'
LOGOUT_URL = f'{MAIN_URL}/main/Authentication/Logout'

REFRESH_TIME = 20
WAIT_TIME = 3

class AutoRefresh:
    def __init__(self, root):
        '''
        Initializes the IRS Auto Refresh application.

        Parameters
        ----------
        root : tk.Tk
            The root window of the application.

        Returns
        -------
        None
        '''
        self.root = root
        
        self.username = None
        self.password = None
        self.starting_time = None
        self.driver = None

        self.labels = []

        self.config_gui()

    def config_gui(self):
        '''
        Configures the GUI layout and components.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        # Set the title and configure the root window
        self.root.title(VERSION_NAME)
        self.root.configure(padx=30, pady=30, bg=BASE_COLOR)
        self.root.maxsize(width=338, height=500)
        self.root.minsize(width=338, height=500)

        # Set the icon for the root window
        self.icon_photo = ImageTk.PhotoImage(Image.open(ICON_PATH))
        self.root.iconphoto(True, self.icon_photo)

        # Set the logo image for the GUI
        self.logo_photo = ImageTk.PhotoImage(Image.open(LOGO_PATH))
        self.logo_label = tk.Label(self.root, image=self.logo_photo,
                        bg=BASE_COLOR, highlightthickness=0)
        self.logo_label.grid(column=0, row=0, columnspan=3, padx=10,
                            pady=10, sticky='n')

        # Labels for user input fields
        input_labels = ['Username:', 'Password:', 'Starting Time:', 'Browser']

        # Create labels and store them in a list for potential further use
        for row, label_text in enumerate(input_labels):
            label = self.create_label(label_text, row+1)
            self.labels.append(label)

        # Entry field for username
        self.username_entry = tk.Entry(width=27)
        self.username_entry.grid(column=2, row=1, columnspan=2, sticky='w', padx=2, pady=2)

        # Entry field for password with masking
        self.password_entry = tk.Entry(width=27, show='*')
        self.password_entry.grid(column=2, row=2, sticky='w', padx=2, pady=2, columnspan=2)

        # Time selection dropdown
        self.time_options = [f'{str(h).zfill(2)}:{str(m).zfill(2)}' for h in range(
            24) for m in range(60)]
        self.time_options = ['Now'] + self.time_options[540:] + self.time_options[:540]

        self.time_value = tk.StringVar(self.root)
        self.time_value.set('(Choose starting time...)')

        self.time_selection = ttk.Combobox(
            self.root, values=self.time_options, textvariable=self.time_value, state='readonly', width=24)
        self.time_selection.grid(column=2, row=3, sticky='w', padx=2, pady=2)

        # Browser selection dropdown
        self.browser_value = tk.StringVar(self.root)
        self.browser_value.set('(Choose browser...)')

        self.browser_selection = ttk.Combobox(
            self.root, textvariable=self.browser_value, width=24, state='readonly')
        self.browser_selection['values'] = ['Firefox', 'Edge', 'Chrome']
        self.browser_selection.grid(column=2, row=4, sticky='w', padx=2, pady=2)

        # Run button to initiate the main process
        self.submit_button = Button(text='Run', command=self.main, highlightthickness=0, width=23)
        self.submit_button.grid(column=2, row=5, sticky='w', padx=2, pady=2, columnspan=2)

    def create_label(self, text, row):
        '''
        Creates and configures a Label widget for the GUI.

        Parameters
        ----------
        text : str
            The text content for the label.
        row : int
            The row in the grid where the label will be placed.

        Returns
        -------
        tk.Label
            The created Label widget.
        '''
        # Create a Label widget with specified text and styling
        label = tk.Label(text=text, font=('Arial', 12, 'normal'), foreground='white', background=BASE_COLOR, anchor='e')

        # Place the label in the grid with specified settings
        label.grid(column=0, row=row, sticky='w', padx=2, pady=2, columnspan=2)

        # Return the created label for potential further use
        return label

    def get_site(self, url):
        '''
        Opens a site with the webdriver.

        Parameters
        ----------
        url: str
            The url to open.
        
        Returns
        -------
        None
        '''
        while True:
            try:
                # Waits for a short amount of time before retrieving the site
                time.sleep(WAIT_TIME/10)
                self.driver.get(url)
                break
            except:
                continue

    def login_siak(self):
        '''
        Logs into the SIAK system using provided credentials.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        # Navigate to the main URL
        self.get_site(MAIN_URL)

        try:
            # Find and fill the username field
            user_field = self.driver.find_element(By.CSS_SELECTOR, '#u')
            user_field.send_keys(self.username)

            # Find and fill the password field
            pass_field = self.driver.find_element(By.CSS_SELECTOR, '#login > form:nth-child(3) > p:nth-child(2) > input:nth-child(2)')
            pass_field.send_keys(self.password)

            # Click the login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, '#submit > input:nth-child(1)')
            login_button.click()

            # Wait for a short period to allow the login process to complete
            time.sleep(WAIT_TIME)

            try:
                # Check if there is an error message after login attempt
                self.driver.find_element(By.CSS_SELECTOR, '#login > p')
                messagebox.showerror(title='Data Incorrect',
                                    message='Username and/or Password incorrect.\nPlease check your data.')
                sys.exit()
            except:
                pass

        except:
            # If an exception occurs, wait and try logging in again (recursive call)
            time.sleep(WAIT_TIME)
            self.login_siak()

    def check_term_siak(self):
        '''
        Checks if the current term on the SIAK system matches the expected term.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            True if the current term matches the expected term, False otherwise.
        '''
        try:
            # Find the element representing the current term, extract and parse the term information
            term = self.driver.find_element(By.CSS_SELECTOR, '#m_b1 > div:nth-child(1)').text.split('Term ')[1][0]
            
            # Compare the extracted term with the expected term (CORRECT_TERM)
            return term == str(CORRECT_TERM)
        except:
            # Return False if an exception occurs (element not found or parsing error)
            return False

    def check_if_logged_out(self):
        '''
        Checks if the user is logged out based on the presence of a password form.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            True if the specified element is found (indicating logout), False otherwise.
        '''
        try:
            # Attempt to find the password form
            self.driver.find_element(By.CSS_SELECTOR, '#login > form:nth-child(3) > p:nth-child(2) > input:nth-child(2)')
            
            # Return True if the element is found (user is logged out)
            return True
        except:
            # Return False if the element is not found (user is not logged out)
            return False

    def open_irs(self):
        '''
        Opens the IRS system and ensures that the necessary page elements are loaded.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        # Open the IRS system site
        self.get_site(ISI_IRS_URL)

        while True:
            try:
                # Check if the required element '#c0' is present
                self.driver.find_element(By.CSS_SELECTOR, '#c0')
                
                # Break the loop if the element is found (indicating successful load)
                break
            except:
                # Check if the user is logged out, attempt to log in if needed
                if self.check_if_logged_out():
                    self.login_siak()
                    self.get_site(ISI_IRS_URL)
                else:
                    # Wait for a short period and refresh the page
                    time.sleep(REFRESH_TIME)
                    self.driver.refresh()

    def main(self):
        '''
        The main function to automate the IRS process.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        # Step 0: Get all user information
        browser_pick = self.browser_selection.get()
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.starting_time = self.time_selection.get()

        # Step 1: Initialize the browser
        if self.username != '' and self.password != '' and browser_pick != '(Choose browser...)':
            try:
                # Initialize the webdriver based on the selected browser
                if browser_pick == 'Chrome':
                    from webdriver_manager.chrome import ChromeDriverManager
                    from selenium.webdriver.chrome.service import Service as ChromeService
                    self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                elif browser_pick == 'Edge':
                    from webdriver_manager.microsoft import EdgeChromiumDriverManager
                    from selenium.webdriver.edge.service import Service as EdgeService
                    self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
                else:
                    from webdriver_manager.firefox import GeckoDriverManager
                    from selenium.webdriver.firefox.service import Service as FirefoxService
                    self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

                # Step 2: Check if the time is correct before logging in and refreshing
                current_time = 'Now'
                while current_time != self.starting_time:
                    current_time = (datetime.now() + timedelta(minutes=1)).strftime('%H:%M')
                    time.sleep(REFRESH_TIME)

                # Step 3: Try to log in
                self.login_siak()

                # Step 4: Loop until the term is correct
                while not self.check_term_siak():
                    time.sleep(REFRESH_TIME)
                    self.get_site(LOGOUT_URL)
                    self.login_siak()

                # Step 5: Refresh the IRS page over and over again
                self.buka_irs()
                messagebox.showinfo(title='IRS Ready', message='Your IRS can now be filled.\n')

            except Exception as e:
                messagebox.showerror(title='Error', message=f'An error has occurred.\n\n{e}')

        else:
            messagebox.showerror(title='Form Incomplete', message='Please complete your form.')


if __name__ == '__main__':
    root = tk.Tk()
    app = AutoRefresh(root)
    root.mainloop()