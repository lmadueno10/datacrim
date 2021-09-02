import psycopg2
import time
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

con = psycopg2.connect(database="colaboraccion", user="postgres", password="sasa", host="127.0.0.1", port="5432")
cur = con.cursor()

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")
options.add_argument('disable-infobars')
driver = webdriver.Chrome(chrome_options=options, executable_path=r'../chromedriver.exe')

driver.get("https://arcgis4.inei.gob.pe:6443/arcgis/rest/services/Datacrim/DATACRIM002_AGS_PUNTOSDELITOS/MapServer")

pathLayers = "(//div[@class='rbody']/ul)[1]/li"

WebDriverWait(driver, 60).until(
    EC.visibility_of_all_elements_located((By.XPATH, pathLayers))
)

groups = driver.find_elements_by_xpath((pathLayers))

for group in groups:
    groupName = group.find_element_by_xpath(".//a").text
    layersGroup = group.find_elements_by_xpath(".//ul/li/a")

    for layer in layersGroup:
        print(
            layer.text,
            layer.get_attribute('href')
        )
        cur.execute(
            "INSERT INTO datacrim.layers(group_name, layer_name, layer_url) VALUES(%s, %s, %s)",
            (groupName, layer.text, layer.get_attribute('href'), ))
        con.commit()
