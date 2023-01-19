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
playwright = sync_playwright().start()
browser = playwright.chromium.launch(args=['--start-maximized --use-gl=egl'], headless=False) # https://github.com/microsoft/playwright/issues/1086#issuecomment-1027450577
page = browser.new_page()
page.set_viewport_size({"width": 16000, "height": 16000})
page.goto("https://satisfactory-calculator.com/en/interactive-map")



page.locator("#qc-cmp2-ui > div.qc-cmp2-footer.qc-cmp2-footer-overlay.qc-cmp2-footer-scrolled > div > button.css-1litn2c").click()
page.locator("body > div.cc-window.cc-banner.cc-type-info.cc-theme-block.cc-bottom.cc-color-override-688238583 > div > a").click()
page.locator("#patreonModal > div > div > div.modal-header > button > span").click()


page.set_default_timeout(120*1000) # 120 seconds timeout for parsing
page.set_input_files('input[type="file"]', 'save.sav')
page.wait_for_selector("#leafletMap > div.leaflet-control-container > div.leaflet-top.leaflet-left > div:nth-child(6) > a:nth-child(2) > i")


# fullscreen map
page.locator("xpath=/html/body/main/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/a").click()

#zomm out
page.goto("https://satisfactory-calculator.com/en/interactive-map#7;49935;0")


page.screenshot(path='screenshot16k.png')




# import time

# from os import listdir
# from os.path import isfile, join
# import glob

# SAVE_LOCATION = r"C:\Users\doode\AppData\Local\FactoryGame\Saved\SaveGames\76561198048397086"

# onlyfiles = [f for f in listdir(SAVE_LOCATION) if isfile(join(SAVE_LOCATION, f))]
# #print(onlyfiles)

# saves = glob.glob(r"C:\Users\doode\AppData\Local\FactoryGame\Saved\SaveGames\76561198048397086\*.sav")
# print(saves)