from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import json
import platform
import os

MAX_BANDWIDTH = 70000 # Kbps
MIN_BANDWIDTH = 500 # Kbps

def setBandwidth(Kbps):
    op_sys = platform.system()
    if op_sys == "Darwin":
        bandwidth = Kbps / 4 * 1024
        driver.set_network_conditions(offline=False,latency=0,download_throughput=bandwidth, upload_throughput=bandwidth)
    else:
        bandwidth = Kbps / 1000
        os.system(f"/usr/sbin/tc qdisc add dev wlp1s0 root tbf rate {bandwidth}")




driver = webdriver.Chrome()

driver.get("https://www.youtube.com/watch?v=KLuTLF3x9sA")
# driver.get("https://vimeo.com/15298502")
# driver.get("https://www.tbs.com/shows/the-big-bang-theory/season-7/episode-8/the-itchy-brain-simulation")
# driver.get("https://www.c-span.org/video/?538521-1/simulcast-cbs-news-vice-presidential-debate")

driver.implicitly_wait(0.5)

with open("main.js", "r") as f:
    funcjs = f.read()


data = []
time.sleep(2)
body = driver.find_elements(By.TAG_NAME, "body")[0]
body.send_keys("Space")

driver.execute_script("document.getElementsByTagName('video')[0].play()")
print('play')
time.sleep(5)

# skip_ads = WebDriverWait(driver, 20*60).until(EC.element_to_be_clickable((By.CLASS_NAME, "ytp-skip-ad-button")))
# skip_ads.click()

start = time.time()

try:
    while True:
        seconds = time.time() - start
        setBandwidth(1000)

        output = driver.execute_script(funcjs)
        # print(output)
        data.append(output)
except:
    ...

with open("data.json", "w+") as f:
    json.dump(data, f)
