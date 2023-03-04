from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cryptography.fernet import Fernet
from dotenv import dotenv_values
import undetected_chromedriver as uc 
import time 
import re 


class ImageFetcher:
  def __init__(self):
    self.sauce = ""
    self.images = []
    self.index = 1
    self.config = dotenv_values(".env")

    raw = self.config.get("FERNET_KEY")
    key = raw.encode("utf-8")
    fernet = Fernet(key)

    self.fernet = fernet
    
  def setSauce(self, sauce):
    self.sauce = sauce

  def setupDriver(self):
    options = webdriver.ChromeOptions() 
    options.add_argument("--headless=new")
    driver = uc.Chrome(use_subprocess=True, options=options)
    self.driver = driver

  def getImages(self):
    if (self.sauce == ""):
      print("No sauce provided")
      return []
    else:
      wait = WebDriverWait(self.driver, 20)

      firstSecret = self.config.get("FIRST_SECRET").encode("utf-8")
      firstDec = self.fernet.decrypt(firstSecret).decode()

      self.driver.get(f"{firstDec}{self.sauce}/1/")
      wait.until(EC.visibility_of_element_located((By.ID, 'image-container')))

      time.sleep(2)

      secondSec = self.config.get("SECOND_SECRET").encode("utf-8")
      thirdSec = self.config.get("THIRD_SECRET").encode("utf-8")
      secondDec = self.fernet.decrypt(secondSec).decode()
      thirdDec = self.fernet.decrypt(thirdSec).decode()

      s = self.driver.page_source 
      matches = re.search(rf"(.*?)({thirdDec})([0-9]+)(.*?)", s)
      imageCode = matches.groups()[2]

      try:  
        while (self.index < 500):
          self.driver.get(f"{secondDec}{thirdDec}{imageCode}/{self.index}.jpg")
          image = self.driver.find_element(By.TAG_NAME, 'img')
          src = image.get_attribute('src')
          self.images.append(src)
          self.index += 1
        self.driver.quit()
      except NoSuchElementException:
        if (len(self.images) == 0):
          print("No such element found")
        else:
          print("Finished fetching images")
        self.driver.quit()
        return self.images 
  
  def quit(self):
    self.driver.quit()
