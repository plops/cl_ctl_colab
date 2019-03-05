import sys
import time
import selenium
import selenium.webdriver
import selenium.webdriver.support
import selenium.webdriver.support.ui
import selenium.webdriver.support.wait
import selenium.webdriver.support.expected_conditions
class SeleniumMixin(object):
    def __init__(self):
        self._driver=selenium.webdriver.Chrome()
        self._wait=selenium.webdriver.support.wait.WebDriverWait(self._driver, 5)
    def sel(self, css):
        log("sel css={}".format(css))
        return self._driver.find_element_by_css_selector(css)
    def selx(self, xpath):
        log("sel xpath={}".format(xpath))
        return self._driver.find_element_by_xpath(xpath)
    def wait_css_clickable(self, css):
        self._wait.until(selenium.webdriver.support.expected_conditions.element_to_be_clickable((selenium.webdriver.common.by.By.CSS_SELECTOR,css,)))
    def wait_css_gone(self, css):
        self._wait.until(selenium.webdriver.support.expected_conditions.invisibility_of_element_located((selenium.webdriver.common.by.By.CSS_SELECTOR,css,)))
    def wait_css_clickable(self, css):
        self._wait.until(selenium.webdriver.support.expected_conditions.element_to_be_clickable((selenium.webdriver.common.by.By.CSS_SELECTOR,css,)))
    def wait_xpath_clickable(self, xpath):
        self._wait.until(selenium.webdriver.support.expected_conditions.element_to_be_clickable((selenium.webdriver.common.by.By.XPATH,xpath,)))
    def waitsel(self, css):
        self.wait_css_clickable(css)
        return self.sel(css)
    def waitselx(self, xpath):
        self.wait_xpath_clickable(xpath)
        return self.selx(xpath)
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
class Colaboratory(SeleniumMixin):
    def open_colab(self):
        log("open website.")
        self._driver.get("https://colab.research.google.com/notebooks/welcome.ipynb")
        self.sel(".gb_gb").click()
    def login(self, password_fn="/dev/shm/p"):
        f=open(password_fn)
        pw=f.read().replace("\n", "")
        f.close()
        log("enter login name.")
        self.waitsel("#identifierId").send_keys("martinkielhorn@effectphotonics.nl")
        self.sel("#identifierNext").click()
        log("enter password.")
        self.waitsel("input[type='password']").send_keys(pw)
        self.sel("#passwordNext").click()
    def attach_gpu(self):
        log("enable gpu.")
        time.sleep(1)
        self.selx("(.//*[normalize-space(text()) and normalize-space(.)='Insert'])[1]/following::div[5]").click()
        self._driver.find_element_by_id(":1z").click()
        self.selx("//paper-dropdown-menu[@id='accelerators-menu']/paper-menu-button//input").send_keys("\n")
        self.selx("//paper-item[@value='GPU']").send_keys("\n")
        self.waitsel("#ok").send_keys("\n")
    def start(self):
        log("start vm instance.")
        self.waitsel("#connect .colab-toolbar-button").click()
    def stop(self):
        log("stop vm instance.")
        self.waitsel("#runtime-menu-button .goog-menu-button-caption").click()
        self.waitsel("css=#3A 21 > .goog-menuitem-content").click()
        self.waitsel("css=.button-action-column > .style-scope").click()
        self.waitsel("#ok").click()
    def __init__(self):
        SeleniumMixin.__init__(self)
        self.open_colab()
        self.login()
        self.attach_gpu()
colab=Colaboratory()