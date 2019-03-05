(eval-when (:compile-toplevel :execute :load-toplevel)
  (ql:quickload :cl-py-generator))

(in-package :cl-py-generator)

(let ((code
       `(do0
	 (imports (sys
		   time
		   selenium
		   selenium.webdriver
		   selenium.webdriver.support
		   selenium.webdriver.support.ui
		   selenium.webdriver.support.wait
		   selenium.webdriver.support.expected_conditions
					;selenium.webdriver.firefox
		   ))

	 (class SeleniumMixin (object)
		(def __init__ (self)
		  (setf self._driver (selenium.webdriver.Chrome)
			self._wait (selenium.webdriver.support.wait.WebDriverWait self._driver 5) ))
	 	(def sel (self css)
		  (log (dot (string "sel css={}")
			    (format css)))
		  (return (self._driver.find_element_by_css_selector css)))
		(def selx (self xpath)
		  (log (dot (string "sel xpath={}")
			    (format xpath)))
		  (return (self._driver.find_element_by_xpath xpath)))
		(def wait_css_clickable (self css)
		  (self._wait.until (selenium.webdriver.support.expected_conditions.element_to_be_clickable
			       (tuple selenium.webdriver.common.by.By.CSS_SELECTOR
				      css))))
		(def wait_css_gone (self css)
		  (self._wait.until (selenium.webdriver.support.expected_conditions.invisibility_of_element_located
                               (tuple selenium.webdriver.common.by.By.CSS_SELECTOR
                                      css))))
		(def wait_css_clickable (self css)
		  (self._wait.until (selenium.webdriver.support.expected_conditions.element_to_be_clickable
                               (tuple selenium.webdriver.common.by.By.CSS_SELECTOR
                                      css))))

		(def wait_xpath_clickable (self xpath)
		  (self._wait.until (selenium.webdriver.support.expected_conditions.element_to_be_clickable
			       (tuple selenium.webdriver.common.by.By.XPATH xpath))))
		(def waitsel (self css)
		  (self.wait_css_clickable css)
		  (return (self.sel css)))
		(def waitselx (self xpath)
		  (self.wait_xpath_clickable xpath)
		  (return (self.selx xpath))))
	 (def current_milli_time ()
           (return (int (round (* 1000 (time.time))))))
	 

         (do0
          "global g_last_timestamp"
          (setf g_last_timestamp (current_milli_time))
          (def milli_since_last ()
            "global g_last_timestamp"
            (setf current_time (current_milli_time)
                  res (- current_time g_last_timestamp)
                  g_last_timestamp current_time)
            (return res)))

	 (class bcolors ()
                (setf OKGREEN (string "\\033[92m")
                      WARNING (string "\\033[93m")
                      FAIL (string "\\033[91m")
                      ENDC (string "\\033[0m")))
	 
         (def log (msg)
           (print (+ bcolors.OKGREEN
                     (dot (string "{:8d} LOG ")
                          (format (milli_since_last)))
                     msg
                     bcolors.ENDC))
           (sys.stdout.flush))
         (def fail (msg)
           (print (+ bcolors.FAIL
                     (dot (string "{:8d} FAIL ")
                          (format (milli_since_last)))
                     msg
                     bcolors.ENDC))
           (sys.stdout.flush))
         



         (def warn (msg)
           (print (+ bcolors.WARNING
                     (dot (string "{:8d} WARNING ")
                          (format (milli_since_last)))
                     msg
                     bcolors.ENDC))
           (sys.stdout.flush))


	 (class
	  Colaboratory (SeleniumMixin)
	  
	  (def open_colab (self)
	    (do0
	     (setf site (string "https://colab.research.google.com/notebooks/welcome.ipynb"))
	     (log (dot (string "open website {}.")
		       (format site)))
	       (self._driver.get site)
	       
	       (dot (self.sel (string ".gb_gb"))  (click))))
	  (def login (self &key (password_fn (string "/dev/shm/p")))
	    (do0
	     (setf f (open password_fn)
		   pw (dot (f.read)
			   (replace (string "\\n")
				    (string ""))))
	     (f.close)
	     (do0
	      (log (string "enter login name."))
	      (dot (self.waitsel (string "#identifierId"))
		   (send_keys (string "martinkielhorn@effectphotonics.nl")))
	      (dot (self.sel (string "#identifierNext"))
		   (click))))
	    (do0
	     (log (string "enter password."))
	     (dot (self.waitsel (string "input[type='password']"))
		  (send_keys pw))
	     (dot (self.sel (string "#passwordNext"))
		  (click))))

	  (def attach_gpu (self)
	    (do0
	    ;; i used css selector gadget (chromium) and selenium ide in firefox
	    (log (string "enable gpu."))
	    (time.sleep 1)
					;(dot (self.selx (string "(.//*[normalize-space(text()) and normalize-space(.)='Insert'])[1]/following::div[5]")) (click))
	    
					;(dot (self._driver.find_element_by_id (string ":1z")) (click))
	    (dot (self.sel (string "#runtime-menu-button")) (click))
	    (dot (self.selx (string "//div[@command='change-runtime-type']")) (click))
	    
	    (dot (self.selx (string "//paper-dropdown-menu[@id='accelerators-menu']/paper-menu-button//input"))
		 (send_keys (string "\\n")))
	    (dot (self.selx (string "//paper-item[@value='GPU']"))
		 (send_keys (string "\\n")))
	    (dot (self.waitsel (string "#ok")) (send_keys (string "\\n")))
	    ))
	  (def start (self)
	    (do0
	     (log (string "start vm instance."))
	     (dot (self.waitsel (string "#connect .colab-toolbar-button")) (click))))
	  (def stop (self)
	    (do0
	     (log (string "stop vm instance."))
	     (dot (self.sel (string "#runtime-menu-button")) (click))
	     (dot (self.selx (string "//div[@command='manage-sessions']")) (click))
	     
	     ;; click terminate on the vm
	     (dot (self.waitselx (string "//paper-button[text()[contains(.,'Terminate')]]")) (send_keys (string "\\n")))
	     (dot (self.waitselx (string "//paper-button[@id='ok']")) (send_keys (string "\\n")))
	     (dot (self.selx (string "//paper-button[@class='dismiss style-scope colab-sessions-dialog']"))
		  (send_keys (string "\\n")))))
	  
	  (def __init__ (self)
	    (SeleniumMixin.__init__ self)
	    (self.open_colab)
	    (self.login)
	    (self.attach_gpu)))


	 (setf colab (Colaboratory))
	 
	 )))
  (write-source "/home/martin/stage/cl_ctl_colab/source/run_00_start" code)
  (write-source "/dev/shm/s"
		`(do0
		  )))
