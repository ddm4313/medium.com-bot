import selenium
import time, threading
import datetime, random, sys
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import names, bs4
from bs4 import BeautifulSoup
from html import unescape
lock = threading.Lock()
print("[#] MediumBot")
story = input("[#] Story Link: ")
threads = int(input("[#] Threads (Recommended 5): "))
def steve():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        while 3 > 1:
            running = ["[#] Running...", "[#] Running.", "[#] Running..", "[#] Running.....", "[#] Running......", "[#] Running...."]
            sys.stdout.write(f"\r{random.choice(running)}")
            a = requests.post(
                "http://api.guerrillamail.com/ajax.php?f=get_email_address&ip=127.0.0.1&agent=Mozilla_foo_bar")
            response = (a.json())
            email = response["email_addr"]
            ehh = requests.post("https://medium.com/_/graphql", json={"operationName": "SendAcctAuthEmail",
                                                                      "variables": {"email": f"{str(email)}",
                                                                                    "redirect": f"{story}"},
                                                                      "query": "mutation SendAcctAuthEmail($email: String!, $redirect: String, $fullName: String, $captchaValue: String) {\n  sendAcctAuthEmail(email: $email, redirect: $redirect, fullName: $fullName, captchaValue: $captchaValue)\n}\n"})
            time.sleep(20)
            sid_token = response["sid_token"]
            get = requests.post(
                f"https://api.guerrillamail.com/ajax.php?f=get_email_list&offset=0&sid_token={sid_token}")
            email = (get.json())
            mail_id = email["list"][0]["mail_id"]
            fetch_mail = requests.post(
                f"https://api.guerrillamail.com/ajax.php?f=fetch_email&offset=0&sid_token={sid_token}&email_id={mail_id}")
            content = (fetch_mail.json())
            body = unescape(content["mail_body"])
            soup = BeautifulSoup(body, "html.parser")
            email_link = soup.find('a', href=True)
            driver.get(email_link["href"])
            element1 = WebDriverWait(driver, 800).until(
                EC.presence_of_element_located((By.XPATH, "//button[@data-action='submit-registration']")))
            lock.acquire()
            driver.find_element_by_xpath("//button[@data-action='submit-registration']").click()
            lock.release()
            element0 = WebDriverWait(driver, 800).until(
                EC.presence_of_element_located((By.XPATH, "//button[@title='Follow True Crime']")))
            driver.find_element_by_xpath("//button[@title='Follow True Crime']").click()
            driver.find_element_by_xpath("//button[@title='Follow Immigration']").click()
            driver.find_element_by_xpath("//button[@title='Follow Cryptocurrency']").click()
            driver.find_element_by_xpath("//button[@data-action='onboarding-next']").click()
            time.sleep(3.5)
            driver.find_element_by_xpath('//*[@id="root"]/div/article/div/section/div/div/div[2]/div/div[2]/div/div/span/div/div').click()
            driver.execute_script('window.scrollBy(0,200)')
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="root"]/div/div[4]/div/div[1]/div/div[1]/div/button').click()
            sys.stdout.write(f"\r[#] Clapped...")
            driver.delete_all_cookies()
    except Exception as e:
        print(e)
        time.sleep(20000)

for i in range(threads):
    t = threading.Thread(target=steve)
    t.start()
