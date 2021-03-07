#!/usr/bin/env python3

import sys
import os
from os import *
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
try:
 from PIL import Image, ImageEnhance, ImageFilter, ImageGrab
except ImportError:
 import Image
from screen_search import *
import psutil


def startChrome():
 for p in psutil.process_iter():
  try:
   if 'Google Chrome' in p.name():
    p.kill()
  except psutil.Error:
   pass
 options = webdriver.ChromeOptions()
 options.add_argument("--user-data-dir=/Users/olivia/Library/Application Support/Google/Chrome Beta/")
 options.add_argument("--profile-directory=Profile 2")
 options.add_argument("--enable-accessibility-tab-switcher")
 driver = webdriver.Chrome('/Users/olivia/chromedriver 2', options=options)
 driver.set_page_load_timeout(10)
 return driver

def startChromeheadless():
 options = webdriver.ChromeOptions()
 options.add_argument("--user-data-dir=/Users/olivia/Library/Application Support/Google/Chrome Beta/")
 options.add_argument("--profile-directory=Profile 2")
 options.add_argument("--enable-accessibility-tab-switcher")
 options.add_argument("--disable-extensions")
 options.add_argument("--headless")
 driver = webdriver.Chrome('/Users/olivia/chromedriver 2', options=options)
 driver.set_page_load_timeout(10)
 return driver

logins = {}

for n in range(1, 6):
 email = "atomic.nmss" + str(n) + "@sickkids.ca"
 password = "atomicnmss" + str(n)
 logins[email] = password

weekdays = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}

def get_fitbit_sync():
 last_sync_times = []
 driver = startChromeheadless()
 for email, password in logins.items():
  driver.get('https://www.fitbit.com/logout')
  element = WebDriverWait(driver, 10000).until(
   EC.presence_of_element_located((By.XPATH, '//*[@id="ember661"]'))
   )
  driver.find_element_by_xpath('//*[@id="ember661"]').send_keys(email)
  driver.find_element_by_xpath('//*[@id="ember662"]').send_keys(password)
  driver.find_element_by_xpath('//*[@id="loginForm"]/div[4]/div').submit()
  element = WebDriverWait(driver, 10000).until(
   EC.presence_of_element_located((By.XPATH, '//*[@id="dash"]/div[1]/div[2]'))
   )
  while driver.find_element_by_xpath('//*[@id="dash"]/div[1]/div[2]').text == "":
   pass
  else:
   last_sync = email + ': ' + driver.find_element_by_xpath('//*[@id="dash"]/div[1]/div[2]').text
   # print(last_sync)
   last_sync_times.append(last_sync)
  time.sleep(3)
 for last_sync_time in last_sync_times:
  t = last_sync_time.split('Last Sync:')
  g = t[1].split()
  if g[0].isalpha():
   # print(' today weekday: ' + str(datetime.today().weekday()) + '; weekday: ' + str(weekdays[g[0]]) + '; time: ' + g[1] + ' ' + g[2] )
   if g[0] == "yesterday":
    days_since = 1
   elif g[0] not in weekdays:
    days_since = ' > 7'
   elif weekdays[g[0]] == datetime.today().weekday():
    days_since = 7
   elif datetime.today().weekday() < weekdays[g[0]]:
    days_since = datetime.today().weekday() - weekdays[g[0]] + 7
   else:
    days_since = datetime.today().weekday() - weekdays[g[0]]
   print(last_sync_time + '; Last Sync: ' + str(days_since) + ' Day(s) Ago')
  else:
   # print('time: ' + g[0] + ' ' + g[1] )
   print(last_sync_time + '; Last Sync: ' + '<24 Hrs Ago')

def exp_fitbit_csv():
 driver = startChrome()
 for email, password in logins.items():
  driver.get('https://www.fitbit.com/logout')
  element = WebDriverWait(driver, 10000).until(
   EC.presence_of_element_located((By.XPATH, '//*[@id="ember661"]'))
   )
  driver.find_element_by_xpath('//*[@id="ember661"]').send_keys(email)
  driver.find_element_by_xpath('//*[@id="ember662"]').send_keys(password)
  driver.find_element_by_xpath('//*[@id="loginForm"]/div[4]/div').submit()
  element = WebDriverWait(driver, 10000).until(
   EC.presence_of_element_located((By.XPATH, '//*[@id="dash"]/div[1]/div[2]'))
   )
  while driver.find_element_by_xpath('//*[@id="dash"]/div[1]/div[2]').text == "":
   pass
  else:
   driver.get('https://www.fitbit.com/settings/data/export')
   element = WebDriverWait(driver, 10000).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="data-export-container"]/div[1]/div/div[3]/div/button'))
    )
   driver.find_element_by_xpath('//*[@id="data-export-container"]/div[1]/div/div[2]/div[1]/div[2]/label').click()
   driver.find_element_by_xpath('//*[@id="data-export-container"]/div[1]/div/div[3]/div/button').click()
   time.sleep(10)
   export_file_path_old = "/Users/olivia/Downloads/fitbit_export_" + str(datetime.today().date()).replace('-', '') + ".csv"
   export_file_path_new = "/Users/olivia/OneDrive - SickKids/Neurology Drive Current MAR 2020/ATOMIC (NMSS) Study 1000065261/Data/Fitbit Data Export by Device/" + password + '_' + "fitbit_export_" + str(datetime.today().date()).replace('-', '_') + ".csv"
   file_exported = path.exists(export_file_path_old)
   print(file_exported)
   while file_exported is False:
    file_exported = path.exists(export_file_path_old)
    pass
   print('ready')
   os.rename(export_file_path_old, export_file_path_new)
   print('this month done')
   if datetime.today().day == 1:
    driver.find_element_by_xpath('//*[@id="data-export-container"]/div[1]/div/div[2]/div[1]/div[4]/label').click()
    driver.find_element_by_xpath('//*[@id="data-export-container"]/div[1]/div/div[3]/div/button').click()
    time.sleep(10)
    export_file_path_old_lm = "/Users/olivia/Downloads/fitbit_export_" + str(datetime.today().date()).replace('-', '') + ".csv"
    export_file_path_new_lm = "/Users/olivia/OneDrive - SickKids/Neurology Drive Current MAR 2020/ATOMIC (NMSS) Study 1000065261/Data/Fitbit Data Export by Device/" + password + '_' + "fitbit_export_" + str(datetime.today().date()).replace('-', '_') + "_prev_month.csv"
    file_exported_lm = path.exists(export_file_path_old_lm)
    print(file_exported_lm)
    while file_exported_lm is False:
     file_exported_lm = path.exists(export_file_path_old_lm)
     pass
    print('ready')
    os.rename(export_file_path_old_lm, export_file_path_new_lm)
    print('last month done')
   time.sleep(2)

def main():
 count_argv = len(sys.argv)
 for n in range(count_argv):  
  if sys.argv[n] == "sync":
   get_fitbit_sync()
  elif sys.argv[n] == "export":
   exp_fitbit_csv()

if __name__ == "__main__":
 main()
