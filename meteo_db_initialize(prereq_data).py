import psycopg2,requests,json,sys
from psycopg2 import sql



"""
Meteo.lt one-time data insert into local_db <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
"""
# ('administrativeDivision','name' aka city, 'code' aka only EN char.)
import requests
r=requests.get('https://api.meteo.lt/v1/places/vilnius').json()

db_conn=psycopg2.connect(dbname=<db_name>,user=<db_user>,password=<db_pass>,host=<db_host>)
db_cur=db_conn.cursor()



for i in range(0,len(r)):
    try:
        """one-time region name insert"""
        input_val=f"'{r[i]['administrativeDivision']}'"
        country_code='LT'
        query=(f"INSERT INTO meteo_schema.region_list (region_id,country_code,region_name) VALUES (default,%s,{input_val})")
        db_cur.execute(query,(country_code,))
        db_conn.commit()
        """one-time city name insert"""
        name_val=(f"'{r[i]['name']}'")
        code_val=(f"'{r[i]['code']}'")
        region_name=(f"'{r[i]['administrativeDivision']}'")
        db_cur.execute(f"SELECT region_id FROM meteo_schema.region_list WHERE region_name={region_name}")
        region_id=db_cur.fetchone()[0]
        query=(f"INSERT INTO meteo_schema.city_list (location_code,region_id,city_name) VALUES ({code_val},{region_id},{name_val})")
        db_cur.execute(query)
        db_conn.commit()
    except Exception:
        db_conn.rollback()



try:
    r=requests.get('https://api.meteo.lt/v1/places/vilnius/forecasts/long-term')
    if r.status_code == 200:
        pass
        r=r.json()['forecastTimestamps']
    else:
        raise Exception
except Exception:
    print('Error on Meteo.lt API request')

for i in range(0,len(r)):
    try:
        """one-time conditionCode insert"""
        input_val=f"'{r[i]['conditionCode']}'"
        query=(f"INSERT INTO meteo_schema.condition_list (condition_code) VALUES ({input_val})")
        db_cur.execute(query)
        db_conn.commit()
        print('ok')
    except Exception:
        print('error...')
        db_conn.rollback()



db_cur.execute(f"SELECT location_code FROM meteo_schema.city_list")
location_code_list=db_cur.fetchall()
for k in range(0,1):#len(location_code_list)):
    try:
        """one-time location coordinate insert into database"""
        location_code=(location_code_list[k][0])
        print(location_code)
        # location_code='vilnius'
        link=f"https://api.meteo.lt/v1/places/{location_code}"
        location_code=(f"'{location_code_list[k][0]}'")
        print(link)
        print(location_code)
        r=requests.get(link).json()
        
        latitude=r['coordinates']['latitude']
        longitude=r['coordinates']['longitude']
        print(latitude,longitude)
        query=(f"UPDATE meteo_schema.city_list SET (latitude,longitude) = ({latitude},{longitude}) WHERE location_code={location_code}")
        print(query)
        db_cur.execute(query)
        db_conn.commit()
    except Exception:
        db_conn.rollback()
        print('error...')

db_conn.commit()
db_cur.close()
db_conn.close()