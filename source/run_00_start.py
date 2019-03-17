import sys
import time
import config
import pathlib
import selenium
import selenium.webdriver
import selenium.webdriver.common
import selenium.webdriver.common.keys
import selenium.webdriver.common.action_chains
import selenium.webdriver.support
import selenium.webdriver.support.ui
import selenium.webdriver.support.wait
import selenium.webdriver.support.expected_conditions
import pyperclip
import subprocess
class SeleniumMixin(object):
    def __init__(self):
        self._driver=selenium.webdriver.Firefox()
        self._wait=selenium.webdriver.support.wait.WebDriverWait(self._driver, 2)
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
        self.selx("//a[text()='Sign in']").click()
    def get_auth_token(self, fn, newlines=False):
        f=open(fn)
        pw=f.read()
        if ( not(newlines) ):
            pw=pw.replace("\n", "")
        f.close()
        return pw
    def login(self, password_fn="/home/martin/stage/cl_ctl_colab/source/p"):
        pw=self.get_auth_token(password_fn)
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
        self.waitselx("//div[@command='change-runtime-type']").click()
        self.waitselx("//paper-dropdown-menu[@id='accelerators-menu']/paper-menu-button//input").click()
        self.waitselx("//paper-item[@value='GPU']").click()
        self.waitsel("#ok").click()
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
        log("create new code cell.")
        self.selx("//colab-toolbar-button[@command='add-code']").click()
        entry=self._driver.switch_to_active_element()
        log("copy code.")
        log("paste code into cell.")
        pyperclip.copy(code)
        selenium.webdriver.common.action_chains.ActionChains(self._driver).key_down(selenium.webdriver.common.keys.Keys.CONTROL).key_down("v").key_up(selenium.webdriver.common.keys.Keys.CONTROL).perform()
        log("execute code cell.")
        selenium.webdriver.common.action_chains.ActionChains(self._driver).key_down(selenium.webdriver.common.keys.Keys.SHIFT).key_down(selenium.webdriver.common.keys.Keys.ENTER).key_up(selenium.webdriver.common.keys.Keys.ENTER).key_up(selenium.webdriver.common.keys.Keys.SHIFT).perform()
    def call_shell(self, cmd):
        s=cmd.split(" ")
        r=subprocess.call(s)
        log("ran shell command: {} = {}".format(s, r))
        return r
    def call_shellt(self, cmd):
        s=cmd
        r=subprocess.call(s, shell=True)
        log("ran shell command: {} = {}".format(s, r))
        return r
    def start_ssh(self):
        to_here=((pathlib.Path("/dev/shm/"))/(self._config.server.key))
        to_google=((pathlib.Path("/dev/shm/"))/(self._config.gpu.key))
        try:
            to_google.unlink()
            to_here.unlink()
        except Exception as e:
            pass
        self.call_shellt("/usr/bin/ssh-keygen -t ed25519 -N '' -f {}".format(str(to_google)))
        self.call_shellt("/usr/bin/ssh-keygen -t ed25519 -N '' -f {}".format(str(to_here)))
        self.call_shell("scp -P {} {}.pub  {}:/dev/shm/".format(self._config.server.port, str(to_here), self._config.server.hostname))
        self.call_shell("ssh -p {} {} sudo chown {}.users /dev/shm/{}.pub".format(self._config.server.port, self._config.server.hostname, self._config.server.user, self._config.server.key))
        self.call_shell("ssh -p {} {} sudo mv /dev/shm/{}.pub /home/{}/.ssh/authorized_keys".format(self._config.server.port, self._config.server.hostname, self._config.server.key, self._config.server.user))
        cmd=r"""! apt-get install -qq -o=Dpkg::Use-Pty=0 openssh-server > /dev/null
! mkdir -p /var/run/sshd
! echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
! echo 'LD_LIBRARY_PATH=/usr/lib64-nvidia' >> /root/.bashrc
! echo 'export LD_LIBRARY_PATH' >> /root/.bashrc
! mkdir /root/.ssh
! chmod go-rwx /root/.ssh
! echo '''{}''' >> /root/.ssh/authorized_keys
! echo -e '''{}''' > /root/.ssh/id_ed25519
! chmod og-rwx /root/.ssh/id_ed25519
! echo 'starting sshd'
get_ipython().system_raw('/usr/sbin/sshd -D &')
get_ipython().system_raw('ssh -N -A -t -oServerAliveInterval=15  -oStrictHostKeyChecking=no  -l {} -p {} {} -R 2228:localhost:22 -i /root/.ssh/id_ed25519 &')""".format(self.get_auth_token(((str(to_google))+(".pub")), newlines=False), self.get_auth_token(str(to_here), newlines=True).replace("""
""", "\\n"), self._config.server.user, self._config.server.port, self._config.server.hostname)
        self.run(cmd)
    def __init__(self, config):
        SeleniumMixin.__init__(self)
        self._config=config
        self.open_colab()
        self.login()
        self.attach_gpu()
        self.start()
colab=Colaboratory(config.config)
self=colab
colab.start_ssh()