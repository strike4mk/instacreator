import argparse

# Define ArgumentParser
parser = argparse.ArgumentParser(description='Instagram Account Creation Bot')
# parser.add_argument('--example', help='An example argument')
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import accountInfoGenerator as account
import getVerifCode as verifiCode
from selenium import webdriver
import fakeMail as email
import time
import argparse
from selenium.webdriver.support.ui import Select

#args = parser.parse_args()
#ua = UserAgent(use_cache_server=False, verify_ssl=False)
#userAgent = ua.random
#print(userAgent)


options = webdriver.ChromeOptions()
# Sabit bir kullanıcı ajanı ayarlayın (örneğin, Chrome tarayıcıya ait bir kullanıcı ajanı)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome(r'chromedriver.exe')

#saves the login & pass into accounts.txt file.
acc = open("accounts.txt", "a")

driver.get("https://www.instagram.com/accounts/emailsignup/")
time.sleep(8)
try:
    cookie = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                         '/html/body/div[3]/div/div/button[1]'))).click()
except:
	pass
name = account.username()
time.sleep(5)
#Fill the email value
email_field = driver.find_element_by_name('emailOrPhone')
fake_email = email.getFakeMail()
email_field.send_keys(fake_email)
print(fake_email)

# Fill the fullname value
fullname_field = driver.find_element_by_name('fullName')
fullname_field.send_keys(account.generatingName())
print(account.generatingName())

# Fill username value
username_field = driver.find_element_by_name('username')
username_field.send_keys(name)
print(name)
time.sleep(3)
# Fill password value
password_field = driver.find_element_by_name('password')
acc_password = account.generatePassword()
password_field.send_keys(acc_password) # You can determine another password here.

print(name+":"+acc_password, file=acc)

acc.close()

WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()



time.sleep(8)

#Birthday verification
# Doğum ayı seçimi
select_elements = driver.find_elements(By.CSS_SELECTOR, "._aau-._ap32")

# Ay seçimi (örneğin Mart ayı)
Select(select_elements[0]).select_by_value("3")  # 3, Mart için `value`

# Gün seçimi (örneğin 16. gün)
Select(select_elements[1]).select_by_value("16")  # 16. gün için `value`

# Yıl seçimi (örneğin 2000 yılı)
Select(select_elements[2]).select_by_value("2000")  # 2000 yılı için `value`
# İleri butonuna tıklama
next_button = driver.find_element(By.CSS_SELECTOR,"._acan._acap._acaq._acas._aj1-._ap30")
next_button.click()

time.sleep(3)
#
fMail = fake_email[0].split("@")
mailName = fMail[0]
domain = fMail[1]
instCode = verifiCode.getInstVeriCode(mailName, domain, driver)
driver.find_element_by_name('email_confirmation_code').send_keys(instCode, Keys.ENTER)
time.sleep(10)

#accepting the notifications.
driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
time.sleep(2)

#logout
driver.find_element_by_xpath(
    "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img").click()
driver.find_element_by_xpath(
    "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/div[2]/div").click()

try:
    not_valid = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[4]/div')
    if(not_valid.text == 'That code isn\'t valid. You can request a new one.'):
      time.sleep(1)
      driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div[1]/div[2]/div/button').click()
      time.sleep(10)
      instCodeNew = verifiCode.getInstVeriCodeDouble(mailName, domain, driver, instCode)
      confInput = driver.find_element_by_name('email_confirmation_code')
      confInput.send_keys(Keys.CONTROL + "a")
      confInput.send_keys(Keys.DELETE)
      confInput.send_keys(instCodeNew, Keys.ENTER)
except:
      pass

time.sleep(5)
driver.quit()
