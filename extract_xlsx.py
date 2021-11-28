import os, time, random, pandas,openpyxl,xlrd,psycopg2, datetime,requests,json,sys,logging
from selenium.webdriver.common import by
from datetime import datetime
from typing import Text
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from psycopg2 import sql

log_format='%(levelname)s %(asctime)s - (line:%(lineno)d) %(filename)s - %(message)s'
logging.basicConfig(filename='<>/log_day_ahead.log',
                    level=logging.DEBUG,
                    format=log_format)
log=logging.getLogger()



"""
Download data (.xls) available on website via selenium <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
"""
s=round(random.uniform(130,15000),3)
try:
    # time.sleep(s)
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "<>/Downloads"}
    options.add_experimental_option("prefs",prefs)
    options.headless=True
    driver=webdriver.Chrome(executable_path='<>/chromedriver',chrome_options=options)
    driver.get('<url>')
    s=round(random.uniform(1,5),3)
    time.sleep(s)
    downloadcsv= driver.find_element(By.CLASS_NAME,'<div>')
    downloadcsv.click()
    s=round(random.uniform(15,20),3)
    time.sleep(s)
    driver.quit()
    log.info('[OK] .xlsx file dowloaded.')
except Exception:
    log.error('Chromedriver/.xlsx file dowload error.')



"""
Import data (.xls) to local database via pandas <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
"""
dayahead_html=pandas.read_html('<>/Day-ahead prices.xls')
dayahead_df=pandas.DataFrame(dayahead_html[1])
dayahead_df.rename(columns={'Unnamed: 0':'price_date'},inplace=True)
dayahead_df['price_date']=pandas.to_datetime(dayahead_df['price_date'],format='%d-%m-%Y').dt.date
dayahead_df.sort_values(by='price_date',ascending=False,inplace=True)



try:
    db_conn=psycopg2.connect(dbname=<db_name>,user=<db_user>,password=<db_pass>,host=<db_host>)
    db_cur=db_conn.cursor()
    log.info('[OK] Successful local DB connection.')
except Exception:
    log.error('Local DB connection error.')



try:
    db_cur.execute('SELECT price_date FROM day_ahead_schema.day_ahead_lake WHERE price_date IS NOT NULL ORDER BY price_date DESC LIMIT 1')
    try:
        latest_rec=(db_cur.fetchone())[0]
    except Exception:
        latest_rec=None
        log.info("[OK] Table 'day_ahead_schema.day_ahead_lake' is empty.")
except Exception:
    db_conn.rollback()
    log.debug("Error in sql query.")



std_list=['SYS', 'SE1', 'SE2', 'SE3', 'SE4', 'FI', 'DK1', 'DK2', 'Oslo', 'Bergen', 'Molde', 'EE', 'LV', 'LT', 'AT', 'BE', 'FR', 'NL']
non_std_list=['DE-LU', 'TromsÃ¸','Kr.sand', 'Tr.heim'] # order sensitive
db_dayahead_non_std_list=['DE_LU','Tromsoe','Kr_sand','Tr_heim'] # order sensitive
currency="EUR"
# dat_list=['SYS', 'SE1', 'SE2', 'SE3', 'SE4', 'FI', 'DK1', 'DK2', 'Oslo', 'Bergen', 'Molde', 'EE', 'LV', 'LT', 'AT', 'BE', 'FR', 'NL', 'DE-LU', 'TromsÃ¸','Kr.sand', 'Tr.heim']
# insert_list=['SYS', 'SE1', 'SE2', 'SE3', 'SE4', 'FI', 'DK1', 'DK2', 'Oslo', 'Bergen', 'Molde', 'EE', 'LV', 'LT', 'AT', 'BE', 'FR', 'NL', 'DE_LU','Tromsoe','Kr_sand','Tr_heim']

for n in range(0,dayahead_df.shape[0]-1):

    new_date=dayahead_df.loc[n,'price_date']
    if latest_rec==new_date:
        break

    for i in std_list:
        try:
            input_val=dayahead_df.loc[n,i]
            query=sql.SQL(f"INSERT INTO day_ahead_schema.day_ahead_lake (input_id, uploaded_at,region,price_date,day_ahead_price,currency) VALUES (DEFAULT,DEFAULT,%s,%s,{input_val},%s)")
            db_cur.execute(query,(i, new_date, "EUR"))
            db_conn.commit()
        except Exception:
            db_conn.rollback()
            print(dayahead_df)
            print('error a')
            log.debug('SQL query error.')

    for i in range(0,len(non_std_list)):
        try:
            input_val=dayahead_df.loc[n,non_std_list[i]]
            query=sql.SQL(f"INSERT INTO day_ahead_schema.day_ahead_lake (input_id, uploaded_at,region,price_date,day_ahead_price,currency) VALUES (DEFAULT,DEFAULT,%s,%s,{input_val},%s)")
            db_cur.execute(query,(db_dayahead_non_std_list[i], new_date, "EUR"))
            db_conn.commit()
        except Exception:
            db_conn.rollback()
            print('error')
            log.debug('SQL query error.')



try:
    db_cur.close()
    db_conn.close()
    log.info('[OK] Successful local DB diconnect')
except Exception:
    log.error('Local DB disconnect error.')

if os.path.exists('<>/Day-ahead prices.xls'):
    try:
        os.remove('<>/Day-ahead prices.xls')
        log.info('[OK] .xlsx deleted.')
    except Exception:
        log.error('.xlsx delete error')