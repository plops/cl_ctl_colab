import sys
import time
import selenium
import selenium.webdriver
import selenium.webdriver.support
import selenium.webdriver.support.ui
import selenium.webdriver.support.wait
driver=selenium.webdriver.Chrome()
driver.get("https://colab.research.google.com/")
def sel(css):
    return driver.find_element_by_css_selector()
def wait_css_clickable(css):
    wait.until(selenium.webdriver.support.expected_conditions.element_to_be_clickable((selenium.webdriver.common.by.By.CSS_SELECTOR,css,)))
def waitsel(css):
    wait_css_clickable(css)
    return sel(css)
def current_milli_time():
    return int(round(((1000)*(time.time()))))
global g_last_timestamp
g_last_timestamp=current_milli_time()
def milli_since_last():
    global g_last_timestamp
    current_time=current_milli_time()
    res=((current_time)-(g_last_timestamp))
    g_last_timestamp=current_time
    return res
class bcolors():
    OKGREEN="\033[92m"
    WARNING="\033[93m"
    FAIL="\033[91m"
    ENDC="\033[0m"
def log(msg):
    print(((bcolors.OKGREEN)+("{:8d} LOG ".format(milli_since_last()))+(msg)+(bcolors.ENDC)))
    sys.stdout.flush()
def fail(msg):
    print(((bcolors.FAIL)+("{:8d} FAIL ".format(milli_since_last()))+(msg)+(bcolors.ENDC)))
    sys.stdout.flush()
def warn(msg):
    print(((bcolors.WARNING)+("{:8d} WARNING ".format(milli_since_last()))+(msg)+(bcolors.ENDC)))
    sys.stdout.flush()
sel(".gb_gb").click()
f=open("/dev/shm/p")
pw=f.read().replace("\n", "")
f.close()
log("enter login name.")
waitsel("#identifierId").send_keys("martinkielhorn@effectphotonics.nl")
sel("#identifierNext").click()
log("enter password.")
waitsel("input[type='password']").send_keys(pw)
sel("#passwordNext").click()