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

	 	 (def sel (css)
	   (return (driver.find_element_by_css_selector css)))
	 (def wait_css_clickable (css)
	   (wait.until (selenium.webdriver.support.expected_conditions.element_to_be_clickable
			(tuple selenium.webdriver.common.by.By.CSS_SELECTOR
			       css))))
	 (def waitsel (css)
	   (wait_css_clickable css)
	   (return (sel css)))
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



	 (do0
	  (log (string "start browser."))
	  (setf driver (selenium.webdriver.Chrome)
		wait (selenium.webdriver.support.wait.WebDriverWait driver 30)))
	 (do0
	  (log (string "open website."))
	  (driver.get (string "https://colab.research.google.com/notebooks/welcome.ipynb")))

	 
	 (dot (sel (string .gb_gb))	      (click))
	 (do0
	  (setf f (open (string "/dev/shm/p"))
		pw (dot (f.read)
			(replace (string "\\n")
				 (string ""))))
	  (f.close))
	 (do0
	  (log (string "enter login name."))
	  (dot (waitsel (string "#identifierId"))
	       (send_keys (string "martinkielhorn@effectphotonics.nl")))
	  (dot (sel (string "#identifierNext"))
	       (click)))
	 (do0
	  (log (string "enter password."))
	  (dot (waitsel (string "input[type='password']"))
	       (send_keys pw))
	  (dot (sel (string "#passwordNext"))
	       (click)))
	 #+nil(do0
	  (log (string "dismiss initial notebook choice widget."))
	  (dot (waitsel (string ".dismiss"))
	       (click)))
	 (do0
	  (log (string "enable gpu."))
	  (dot (waitsel (string "#runtime-menu-button .goog-menu-button-caption"))
	       (click))
	  (dot (waitsel (string "[command='change-runtime-type']"))
	       (click)))
	 )))
  (write-source "/home/martin/stage/cl_ctl_colab/source/run_00_start" code))
