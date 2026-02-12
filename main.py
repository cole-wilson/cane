from selenium import webdriver
import selenium
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time
import datetime
import platform
import os
import math
import csv


STEP = 10 # s

DT = 20 # s
INTERFACE = "wlp1s0"

# os.system(f"sudo tc qdisc add dev {INTERFACE} handle ffff: ingress")

options = Options()
# options.add_argument('--no-sandbox')
options.add_argument("--remote-debugging-port=9222")
options.add_argument('--disable-blink-features=AutomationControlled')

def write_data():
    if not os.path.isdir("data"):
        os.mkdir("data")
    filename = "data"+os.sep+datetime.datetime.now().isoformat() + ".csv"
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

def setBandwidth(Kbps):
    op_sys = platform.system()
    bandwidth = Kbps
    # if op_sys == "Darwin":
        # ...
    driver.set_network_conditions(offline=False,latency=0,throughput=bandwidth*1024)
    # else:
        # os.system(f"sudo ../wondershaper/wondershaper -a {INTERFACE} -c  2> err.log") #
        # os.system(f"sudo ../wondershaper/wondershaper -a {INTERFACE} -d {Kbps} 2> err.log")

def bandwidth_from_time(t):
    # https://www.desmos.com/calculator/lcbhf2byjk
    sinfunc = sum([math.sin( t / (10 * i) ) for i in range(1, 20+1)])
    return 500_000 + (70_000*sinfunc)

# def bandwidth_from_time(x):
#     print(x)
#     m = 60
#     if (x % (m*2)) < m:
#         return 200_000
#     else:
#         return 1_000
#     # return (80000 * math.floor((x/1000) % 2)) + 20000

with open("main.js", "r") as f:
    funcjs = f.read()
driver = webdriver.Chrome(options=options)

start = time.time()
last_s = 0
bw = 0

# https://github.com/sharat910/selenium-youtube/blob/master/youtube.py
def stats():
    movie_player = driver.find_elements(By.ID, 'movie_player')[0]
    hover = ActionChains(driver).move_to_element(movie_player)
    hover.perform()
    ActionChains(driver).context_click(movie_player).perform()
    options = driver.find_elements(By.CLASS_NAME, 'ytp-menuitem')
    for option in options:
        option_child = option.find_elements(By.CLASS_NAME, 'ytp-menuitem-label')[0]
        if option_child.text == 'Stats for nerds':
            option_child.click()
            print("Enabled stats collection.")
            return True
    return False
# end ================================================================


def run_for_url(url, skip_yt_ads=False):
    global data
    global bw
    global last_s

    driver.get(url)
    driver.implicitly_wait(0.5)
    time.sleep(2)

    body = driver.find_elements(By.TAG_NAME, "body")[0]
    body.send_keys("Space")

    driver.execute_script("document.getElementsByTagName('video')[0].play()")
    time.sleep(1)

    if skip_yt_ads:
        try:
            skip_ads = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ytp-skip-ad-button")))
            skip_ads.click()
        except selenium.common.exceptions.TimeoutException:
            pass
    start = time.time()

    stats()

    try:
        while True:
            seconds = time.time() - start


            if (round(seconds) % STEP == 0 and (seconds - last_s) > 1):
                bw = max(50, bandwidth_from_time(seconds))
                last_s = seconds
                setBandwidth(bw)
                print(seconds, 'set bandwidth to', bw, "kbps")

            time.sleep(DT)

            output = driver.execute_script(funcjs)
            output["bandwidth"] = bw
            output["t"] = seconds
            # print(seconds, bw, end="                                                         \r")
            data.append(output)
            if output["percent"] is not None and output["percent"] > 0.999 and output["current_time"] > 120:
                print("ENDING VIDEO, STARTING NEXT @@@@@@@@@@@@@@@@@@@@@@@@@")
                return;

    except (Exception, KeyboardInterrupt) as err:
        # input(">>>>>>> ")
        write_data()
        raise err


data = []

video_urls = [
    "https://www.youtube.com/watch?v=KLuTLF3x9sA",
    "https://www.youtube.com/watch?v=-QXrbXYE4jE",
    "https://www.youtube.com/watch?v=aellLMtz3UI",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=ciSNHrKrkeQ",
    "https://www.youtube.com/watch?v=7H7cTSml5zk",
    "https://www.youtube.com/watch?v=LDU_Txk06tM"
    "https://www.youtube.com/watch?v=QCL7VXuO35g",
    "https://www.youtube.com/watch?v=QU-L6_RnaPA",
    "https://www.youtube.com/watch?v=FslCeCp1GqM"
    "https://www.youtube.com/watch?v=yajJ_QVIKwU"
]
# video_urls = ["https://speedtest.net"]
for video in video_urls:
    run_for_url(video, skip_yt_ads=True)

write_data()
