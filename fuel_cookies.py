import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import mysql.connector
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_cookies(username, password):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Open the login page
    login_url = "http://37.27.52.55/phpmyadmin/"
    driver.get(login_url)
    time.sleep(2)
    action = ActionChains(driver)
    # acceptTerms = driver.find_element(By.ID,'didomi-notice-agree-button').click()
    # if acceptTerms != None:
    #     action.move_to_element(acceptTerms).click(acceptTerms).perform()
    time.sleep(2)
    EnterMobileNumber = driver.find_element(By.ID, 'input_username')
    action.move_to_element(EnterMobileNumber).click(EnterMobileNumber).send_keys(username).perform()
    EnterMobileNumber = driver.find_element(By.ID, 'select_server').send_keys(Keys.DOWN).send_keys(Keys.ENTER).perform()
    EnterMobileNumber = driver.find_element(By.ID, 'input_password')
    action.move_to_element(EnterMobileNumber).click(EnterMobileNumber).send_keys(password).send_keys(Keys.ENTER).perform()
    time.sleep(2)
    driver.get('http://37.27.52.55/phpmyadmin/')
    time.sleep(2)
    # text = str(driver.get_cookies())
    # text = text.replace("'", '"')
    # my_dict = eval(text)
    # cookies = ''
    # for dict in my_dict:
    #     if dict['name'] == 'MYAS24-JWT':
    #         cookies += (dict['name']+' ='+dict['value'])
    # upload(cookies, username)
    # driver.close()
def upload(cookies, username):
    conn = mysql.connector.connect(
        host='dolvera.hostingas.lt',
        user='dolvera_po',
        password='kJzrCH8cCG7d73sG',
        database='dolvera_po'
    )
    cursor = conn.cursor()
    cookies = '"'+cookies+'"'
    if username == '653983':
        id = 1
    elif username == '665356':
        id = 4
    sql = "UPDATE us_tmsys_table_global_system SET sysval = "+cookies+" WHERE id = "+str(id)
    cursor.execute(sql)

    print(sql)
if __name__ == '__main__':
    get_cookies('653983', '678683')
    get_cookies('665356', '868888')