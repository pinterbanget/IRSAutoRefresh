# IRSAutoRefresh

Making refreshing your SIAK NG IRS page a one-clicker ;)

## Download

In the <a href="https://github.com/pinterbanget/irsautorefresh/releases/latest">releases</a> page.

## Usage

### Prerequisites

Make sure you have either Mozilla Firefox (I highly recommend this), Google Chrome, or Microsoft Edge (Chromium-based) installed.

### Steps

1. Unzip the .zip file you just downloaded. <b>Do not attempt to run without unzipping.</b>
2. <a href="https://support.microsoft.com/en-us/windows/add-an-exclusion-to-windows-security-811816c0-4dfd-af4a-47e4-c301afe13b26">Add the IRS Auto Refresh folder as an exclusion</a>. This is because sometimes Windows detects the program as a virus.
3. Run the `IRSAutoRefresh.exe` file.
4. Input/select:
   - your SIAK NG username and password
   - a time to start the auto-refresher
   - a browser of your choice (that you've installed)
5. Click `"Run"`. A browser will automatically open. Don't interfere. Let the program run; it might look like the program is not responding, but it is normal.
6. When you get a "Your IRS can now be filled" message... well... go fill it.
7. You're welcome!

## Changelog

v0.9.7

- changed paradigm to OOP
- added a term-checking function
- replaced the "Starting Time" field into a dropdown field
- more refined logic

v0.9.6

- added "Starting Time" field to start IRS Auto Refresh on a selected time

v0.9.5

- utilization of webdriver-manager, now you don't need to install anything before usage!
  (except the browsers, duh)

v0.9.4

- new, revamped UI with MUCH less bugs than prev version
- better message handling

v0.9.3

- fixed error on 'high load' SIAK message

v0.9.2

- added Microsoft Edge support :)
- new theme! (still basic as fuck tho)
- only one program for all 3 browsers

v0.9.1

- fixed refreshing when website can't be reached

v0.9

- it's released!

## Compiling

`nuitka --enable-plugin=tk-inter --onefile --windows-icon-from-ico=Icon.ico --include-package-data=assets --disable-console main.py`

## Known Bugs

- random 'Anda tidak mempunyai hak akses' bug, fix unknown at this time
  - This is the reason I deliberately didn't catch any specific exceptions.

## Special Thanks

- Sifra for letting me borrow her SIAKNG account (Alhamdulillah ga keban)
- Adim for making me release this instead of SIAKWIN (which is unusable as of now... unless? 😳)
  - <u>2024-01-10 Update</u>: Jokes aside, apparently there's now an actual program called SIAKWIN that (I guess) will not only refresh the page, but also fill your classes. Maybe give it a try if you have spare money and report back to me 🤣
- TERSESAT, JASTTH, and Reka for testing this program

## Donate

I accept donations through:

- <a href="https://saweria.co/pinterbanget">saweria</a> (accepting IDR)
- ETH address (accepting Polygon and ERC-20 tokens): 0x148479efcC499CC11D142194FB348007a0357010
- BSC address (accepting Binance Smart Chain tokens): 0xC8d5B444c66bf8d641BB6b6902533a41418d7B6e
