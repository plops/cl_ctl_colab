import sys
import time
import selenium
import selenium.webdriver
import selenium.webdriver.common
import selenium.webdriver.common.keys
import selenium.webdriver.common.action_chains
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
        site="https://colab.research.google.com/notebooks/welcome.ipynb"
        log("open website {}.".format(site))
        self._driver.get(site)
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
        self.sel("#runtime-menu-button").click()
        self.selx("//div[@command='change-runtime-type']").click()
        self.selx("//paper-dropdown-menu[@id='accelerators-menu']/paper-menu-button//input").send_keys("\n")
        self.selx("//paper-item[@value='GPU']").send_keys("\n")
        self.waitsel("#ok").send_keys("\n")
    def start(self):
        log("start vm instance.")
        self.waitsel("#connect .colab-toolbar-button").click()
    def stop(self):
        log("stop vm instance.")
        self.sel("#runtime-menu-button").click()
        self.selx("//div[@command='manage-sessions']").click()
        self.waitselx("//paper-button[text()[contains(.,'Terminate')]]").send_keys("\n")
        self.waitselx("//paper-button[@id='ok']").send_keys("\n")
        self.selx("//paper-button[@class='dismiss style-scope colab-sessions-dialog']").send_keys("\n")
    def run(self, code):
        self.selx("//colab-toolbar-button[@command='add-code']").click()
        entry=self._driver.switch_to_active_element()
        entry.send_keys(code)
        selenium.webdriver.common.action_chains.ActionChains(self._driver).key_down(selenium.webdriver.common.keys.Keys.SHIFT).key_down(selenium.webdriver.common.keys.Keys.ENTER).key_up(selenium.webdriver.common.keys.Keys.ENTER).key_up(selenium.webdriver.common.keys.Keys.SHIFT).perform()
    def start_ssh(self, password):
        cmd="""
import random, string
password = {}
! wget -q -c -nc https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
! unzip -qq -n ngrok-stable-linux-amd64.zip
! apt-get install -qq -o=Dpkg::Use-Pty=0 openssh-server pwgen > /dev/null
! echo root:$password | chpasswd
! mkdir -p /var/run/sshd
! echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
! echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
! echo 'LD_LIBRARY_PATH=/usr/lib64-nvidia' >> /root/.bashrc
! echo 'export LD_LIBRARY_PATH' >> /root/.bashrc
get_ipython().system_raw('/usr/sbin/sshd -D &')
print('Copy authtoken from https://dashboard.ngrok.com/auth')
import getpass
authtoken = getpass.getpass()
get_ipython().system_raw('./ngrok authtoken $authtoken && ./ngrok tcp 22 &')
! curl -s http://localhost:4040/api/tunnels | python3 -c 
'import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])'
""".format(password)
        self.run(cmd)
    def __init__(self):
        SeleniumMixin.__init__(self)
        self.open_colab()
        self.login()
        self.start()
colab=Colaboratory()