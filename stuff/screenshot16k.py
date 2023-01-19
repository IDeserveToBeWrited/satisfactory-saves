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

# map load selectors
# grid
selector1 = "#playerGeneratorsLayer > div.row.align-items-center.mb-1 > div > button:nth-child(1) > img"
# lasso
selector2 = "#leafletMap > div.leaflet-control-container > div.leaflet-top.leaflet-left > div:nth-child(6) > a:nth-child(1) > i"
# rectangle
selector3 = "#leafletMap > div.leaflet-control-container > div.leaflet-top.leaflet-left > div:nth-child(6) > a:nth-child(2) > i"
# circle
selector4 = "#leafletMap > div.leaflet-control-container >	 div.leaflet-top.leaflet-left > div:nth-child(6) > a:nth-child(3)"



playwright = sync_playwright().start()
#                                                             --use-gl=desktop or --use-gl=egl
browser = playwright.chromium.launch(args=['--start-maximized --use-gl=egl'], headless=False) # https://github.com/microsoft/playwright/issues/1086#issuecomment-1027450577
page = browser.new_page()
page.set_viewport_size({"width": 16000, "height": 16000})
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

# file upload?
page.set_default_timeout(4*60*1000) # 4 minutes timeout for parsing
page.set_input_files('input[type="file"]', 'save.sav')
print("File uploaded, waiting to parse...")
# wait for map to parse
page.wait_for_selector("#leafletMap > div.leaflet-control-container > div.leaflet-top.leaflet-left > div:nth-child(6) > a:nth-child(2) > i")
print("Parsed?")
# page.set_default_timeout(30000) # return to default timeout
# fullscreen map
#page.locator("#leafletMap > div.leaflet-control-container > div.leaflet-top.leaflet-left > div.leaflet-control-fullscreen.leaflet-bar.leaflet-control > a").click()
#page.get_by_text("View Fullscreen").click()
page.locator("xpath=/html/body/main/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/a").click()
print("Fullscreen")

#zomm out
print("Zooming out")
#for x in range(16):
#	page.locator("#leafletMap > div.leaflet-control-container > div.leaflet-top.leaflet-left > div:nth-child(1) > a.leaflet-control-zoom-out > span").click()
#	time.sleep(2)
#page.mouse.wheel(0, 800)

page.goto("https://satisfactory-calculator.com/en/interactive-map#6.7;49935;0")
# 4.85 for 4k
# 7 za mało na 16k

print("Zoomed out")

print("sleep")
time.sleep(60)
print("sleep done")
page.screenshot(path='screenshot16k.png')
print("Screenshot took")
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