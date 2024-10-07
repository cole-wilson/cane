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
        bandwidth = Kbps
        driver.set_network_conditions(offline=False,latency=0,download_throughput=bandwidth, upload_throughput=bandwidth)
    else:
        bandwidth = Kbps
        # burst = 1000
        # max_latency = 1000
        os.system(f"sudo wondershaper eth0 {bandwidth} {bandwidth}")
        # os.system(f"sudo /usr/sbin/tc qdisc add dev wlp1s0 root tbf rate {bandwidth}kbit burst {burst} latency {max_latency}ms")
    return Kbps




driver = webdriver.Chrome()

driver.get("https://www.youtube.com/watch?v=KLuTLF3x9sA")
# driver.get("https://fast.com")
# driver.get("https://vimeo.com/15298502")
# driver.get("https://www.tbs.com/shows/the-big-bang-theory/season-7/episode-8/the-itchy-brain-simulation")

driver.implicitly_wait(0.5)

with open("main.js", "r") as f:
    funcjs = f.read()


data = []
# with open("data.json", "r") as f:
    # data = json.load(f)
time.sleep(2)
body = driver.find_elements(By.TAG_NAME, "body")[0]
body.send_keys("Space")

driver.execute_script("document.getElementsByTagName('video')[0].play()")
print('play')
time.sleep(1)

# skip_ads = webdriver.WebDriverWait(driver, 20*60).until(EC.element_to_be_clickable((By.CLASS_NAME, "ytp-skip-ad-button")))
# skip_ads.click()

start = time.time()

try:
    while True:
        seconds = time.time() - start
        bw = setBandwidth(70000)
        time.sleep(0.1)
        output = driver.execute_script(funcjs)
        output["bandwidth"] = bw
        print(output)
        data.append(output)
except:
    ...

with open("data.json", "w+") as f:
    json.dump(data, f)
