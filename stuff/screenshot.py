#pip install pytest-playwright
#playwright install
#pip install playwright-dompath

# START
# https://stackoverflow.com/questions/21886233/time-sleepx-not-working-as-it-should

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

import sys
sys.stdout = Unbuffered(sys.stdout)
# END

from playwright.sync_api import sync_playwright
import time

from datetime import datetime

import glob
import os
saves = glob.glob(r"C:\Users\doode\AppData\Local\FactoryGame\Saved\SaveGames\76561198048397086\*.sav")

# map load selectors
# grid
selector1 = "#playerGeneratorsLayer > div.row.align-items-center.mb-1 > div > button:nth-child(1) > img"
# lasso
selector2 = "#leafletMap > div.leaflet-control-container > div.leaflet-top.leaflet-left > div:nth-child(6) > a:nth-child(1) > i"
# rectangle
selector3 = "#leafletMap > div.leaflet-control-container > div.leaflet-top.leaflet-left > div:nth-child(6) > a:nth-child(2) > i"
# circle
selector4 = "#leafletMap > div.leaflet-control-container >   div.leaflet-top.leaflet-left > div:nth-child(6) > a:nth-child(3)"


def start_browser_and_load_site():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(args=['--start-maximized'], headless=False) # https://github.com/microsoft/playwright/issues/1086#issuecomment-1027450577
    page = browser.new_page()
    page.set_viewport_size({"width": 4000, "height": 4000})
    print("Waiting for site to load...")
    page.goto("https://satisfactory-calculator.com/en/interactive-map")
    page.wait_for_load_state('domcontentloaded')
    page.wait_for_load_state('networkidle')
    print("Site loaded")
    
    # cookies 1
    if page.locator("#qc-cmp2-ui > div.qc-cmp2-footer.qc-cmp2-footer-overlay.qc-cmp2-footer-scrolled > div > button.css-1litn2c"):
        page.locator("#qc-cmp2-ui > div.qc-cmp2-footer.qc-cmp2-footer-overlay.qc-cmp2-footer-scrolled > div > button.css-1litn2c").click()
        print("click 1")
    
    # cookies 2
    if page.locator("body > div.cc-window.cc-banner.cc-type-info.cc-theme-block.cc-bottom.cc-color-override-688238583 > div > a"):
        page.locator("body > div.cc-window.cc-banner.cc-type-info.cc-theme-block.cc-bottom.cc-color-override-688238583 > div > a").click()
        print("click 2")
    
    # patreon
    if page.locator("#patreonModal > div > div > div.modal-header > button > span"):    
        page.locator("#patreonModal > div > div > div.modal-header > button > span").click()
        print("click 3")
    
    time.sleep(2)

# "extraction session" from current time
EXTRACTION_SESSION = "screenshots/" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
if not os.path.exists(EXTRACTION_SESSION): os.makedirs(EXTRACTION_SESSION)

# metadata file for session and hours
metadata = open(EXTRACTION_SESSION + '/metadata.csv', "a")
metadata.write("filename, session_name, time_played, time_played_h, time_played_m, time_played_s\n")
metadata.close()
# csv table

# filename - name of the file
# session_name - name of the session
# time played - time played
# time played_h - time played, only hours
# time played_m - time played, only minutes
# time played_s - time played, only seconds

for file in saves:
    start_browser_and_load_site()

    # file upload?
    page.set_default_timeout(5*60*1000) # 5 minute timeout for parsing
    print("uploading", os.path.basename(file), "file")
    page.set_input_files('input[type="file"]', file)
    print("File uploaded, waiting to parse...")
    # wait for map to parse
    page.wait_for_selector("#leafletMap > div.leaflet-control-container > div.leaflet-top.leaflet-left > div:nth-child(6) > a:nth-child(2) > i")
    print("Parsed?")
    # page.set_default_timeout(30000) # return to default timeout
    # fullscreen map
    #page.locator("#leafletMap > div.leaflet-control-container > div.leaflet-top.leaflet-left > div.leaflet-control-fullscreen.leaflet-bar.leaflet-control > a").click()
    #page.get_by_text("View Fullscreen").click()

    # get session name and time?
    time_played = page.locator("#saveGameInformation > em:nth-child(2) > small:nth-child(1)").inner_text()[1:-1]
    print("time:", time_played)
    x = time_played.split()
    h=x[0][:-1]
    m=x[1][:-1]
    s=x[2][:-1]



    session_name = page.locator("#saveGameInformation > strong:nth-child(1)").inner_text()
    print("session:", session_name)

    metadata = open(EXTRACTION_SESSION + '/metadata.csv', "a")
    metadata.write(os.path.basename(file) + "," + session_name + "," + time_played + "," + h + "," + m + "," + s +"\n")
    metadata.close()

    page.locator("xpath=/html/body/main/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/a").click()
    print("Fullscreen")
    time.sleep(3)
    #zomm out
    print("Zooming out")
    #for x in range(16):
    #   page.locator("#leafletMap > div.leaflet-control-container > div.leaflet-top.leaflet-left > div:nth-child(1) > a.leaflet-control-zoom-out > span").click()
    #   time.sleep(2)
    #page.mouse.wheel(0, 800)
    
    page.goto("https://satisfactory-calculator.com/en/interactive-map#4.85;49935;0")
    # 4.85 for 4k
    print("Zoomed out")
    
    print("sleep")
    time.sleep(10)
    print("sleep done")
    screenshot_path = EXTRACTION_SESSION + "/" + datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d_%H-%M-%S') + '+' + os.path.basename(file)[:-4] + '.png'
    print("path: ", screenshot_path)
    page.screenshot(path=screenshot_path)
    print("Screenshot took")
    time.sleep(3)
    # exit fullscreen
    page.locator("xpath=/html/body/main/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/a").click()
    print("Fullscreen exited")
    time.sleep(3)
    browser.close()


metadata.close()
browser.close()

# cookies 1 selector
#qc-cmp2-ui > div.qc-cmp2-footer.qc-cmp2-footer-overlay.qc-cmp2-footer-scrolled > div > button.css-1litn2c

# cookies 2
# /html/body/div[2]/div/a
# cookies 2 selector
# body > div.cc-window.cc-banner.cc-type-info.cc-theme-block.cc-bottom.cc-color-override-688238583 > div > a
# patreon selector
# #patreonModal > div > div > div.modal-header > button > span
# fullscreen selector
# #leafletMap > div.leaflet-control-container > div.leaflet-top.leaflet-left > div.leaflet-control-fullscreen.leaflet-bar.leaflet-control > a
# exit fullscreen selector
# #leafletMap > div.leaflet-control-container > div.leaflet-top.leaflet-left > div.leaflet-control-fullscreen.leaflet-bar.leaflet-control > a


#/html/body/div[5]/div/div/div[1]/button/span
#/html/body/div[1]/div/div/div/div[2]/div/button[2]



## cookies 1
#page.get_by_text("AGREE").click()
##cookies 2
#page.get_by_text("Got it!").click()