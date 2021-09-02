import os
from urllib.parse import urlencode

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

cur.execute("select group_name, layer_name, layer_url from datacrim.layers where updated_at is null")
rows = cur.fetchall()

queryString = {
  #"where":"SUBSTRING(UBIGEO_HECHO FROM 1 FOR 2) = '04'",
  #"where":"SUBSTRING(UBIGEO_HEC FROM 1 FOR 2) = '04'",
  "where":"SUBSTRING(UBIGEO FROM 1 FOR 2) = '04'",
  "text":"",
  "objectIds":"",
  "time":"",
  "geometry":"",
  "geometryType":"esriGeometryEnvelope",
  "inSR":"",
  "spatialRel":"esriSpatialRelIntersects",
  "relationParam":"",
  "outFields":"",
  "returnGeometry":"true",
  "returnTrueCurves":"false",
  "maxAllowableOffset":"",
  "geometryPrecision":"",
  "outSR":"",
  "having":"",
  "returnIdsOnly":"false",
  "returnCountOnly":"false",
  "orderByFields":"",
  "groupByFieldsForStatistics":"",
  "outStatistics":"",
  "returnZ":"false",
  "returnM":"false",
  "gdbVersion":"",
  "historicMoment":"",
  "returnDistinctValues":"false",
  "resultOffset":"",
  "resultRecordCount":"",
  "queryByDistance":"",
  "returnExtentOnly":"false",
  "datumTransformation":"",
  "parameterValues":"",
  "rangeValues":"",
  "quantizationParameters":"",
  "featureEncoding":"esriDefault",
  "f":"pjson"
}

dirBase = "C:/Users/Asus/Desktop/datacrim"

for row in rows:
    group_name = row[0]
    layer_name = row[1]
    layer_url = row[2]
    dirGroup = dirBase + "/" + group_name

    if not os.path.exists(dirGroup):
        os.makedirs(dirGroup)

    driver.get(layer_url + "/query?" + urlencode(queryString))

    if not "error" in driver.find_element_by_xpath("/html/body").text:
        with open(dirGroup + "/" + layer_name + ".json", 'wb') as file:
            file.write(driver.find_element_by_xpath("/html/body").text.encode())
            cur.execute("update datacrim.layers set updated_at = now() where layer_url = %s", (layer_url,))
            con.commit()

    #time.sleep(2)
