from selenium import webdriver
import selenium
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time
import datetime
import platform
import os
import math
import csv


STEP = 6 # s

DT = 0.2 # s
INTERFACE = "enp0s3"

# os.system(f"sudo tc qdisc add dev {INTERFACE} handle ffff: ingress")

options = Options()
# options.add_argument('--no-sandbox')
options.add_argument("--remote-debugging-port=9222")

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
    if op_sys == "Darwin":
        driver.set_network_conditions(offline=False,latency=0,download_throughput=bandwidth, upload_throughput=bandwidth)
    else:
        bandwidth = Kbps
        os.system(f"sudo ../wondershaper/wondershaper -a {INTERFACE} -c 2> err.log")
        os.system(f"sudo ../wondershaper/wondershaper -a {INTERFACE} -d {Kbps} 2> err.log")

def bandwidth_from_time(t):
    t = (t / 500) + 100
    # https://www.desmos.com/calculator/byou3zc63w
    sinfunc = sum([0.15 * math.sin((0.5 / i) * t) for i in range(20)])
    return 50000 + (60000*sinfunc)

with open("main.js", "r") as f:
    funcjs = f.read()
driver = webdriver.Chrome(options=options)

def run_for_url(url, skip_yt_ads=False):
    global data
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

    try:
        start = time.time()
        while True:
            seconds = time.time() - start

            bw = bandwidth_from_time(seconds)

            if (seconds % STEP) == 0:
                setBandwidth(bw)
                print(seconds, 'set bandwidth to', bw/1000, "mbps")

            time.sleep(DT)

            output = driver.execute_script(funcjs)
            output["bandwidth"] = bw
            output["t"] = seconds
            print(seconds, bw, end="                                                         \r")
            data.append(output)
            if output["percent"] is not None and output["percent"] > 0.999 and output["current_time"] > 120:
                print("ENDING VIDEO, STARTING NEXT @@@@@@@@@@@@@@@@@@@@@@@@@")
                return;

    except Exception as err:
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

for video in video_urls:
    run_for_url(video, skip_yt_ads=True)

write_data()
