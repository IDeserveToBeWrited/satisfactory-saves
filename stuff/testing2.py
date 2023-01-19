import time

import os
import glob
from datetime import datetime

SAVE_LOCATION = r"C:\Users\doode\AppData\Local\FactoryGame\Saved\SaveGames\76561198048397086"

saves = glob.glob(r"C:\Users\doode\AppData\Local\FactoryGame\Saved\SaveGames\76561198048397086\*.sav")
#print(saves)

for file in saves:
    #print(file)
    print(os.path.basename(file))
    screenshot_path = 'screenshots/' + datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d_%H-%M-%S') + '+' + os.path.basename(file)[:-4] + '.png'
    #print("creatin time: ", datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d_%H-%M-%S'))
    print(screenshot_path)