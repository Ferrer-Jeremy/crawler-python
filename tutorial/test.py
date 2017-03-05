import time
from selenium import webdriver
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
display.start()

driver = webdriver.Firefox(executable_path='docker/application/geckodriver')
driver.get('http://www.google.com/xhtml')
time.sleep(5)  # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5)  # Let the user actually see something!
driver.quit()
