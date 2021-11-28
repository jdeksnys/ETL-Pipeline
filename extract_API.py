import psycopg2,requests,json,logging
from typing import Text
from psycopg2 import sql

log_format='%(levelname)s %(asctime)s - (line:%(lineno)d) %(filename)s - %(message)s'
logging.basicConfig(filename='<>/log_meteo.log',
                    level=logging.DEBUG,
                    format=log_format)
log=logging.getLogger()



"""
Meteo.lt API request <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
"""
try:
    db_conn=psycopg2.connect(dbname=<db_name>,user=<db_user>,password=<db_pass>,host=<db_host>)
    db_cur=db_conn.cursor()
    log.info('[OK] Successful local DB connection.')
except Exception:
    log.error('Local DB connection error.')

try:
    r=requests.get('https://api.meteo.lt/v1/places/vilnius/forecasts/long-term')
    if r.status_code == 200:
        r=r.json()
        log.info('[OK] Meteo API request made.')
        pass
    else:
        raise Exception
except Exception:
    log.error('Meteo.lt API request error.')

place_list=['code', 'name', 'administrativeDivision', 'country', 'countryCode']
info_list=['forecastType', 'forecastCreationTimeUtc']
forecast_list=['forecastTimeUtc', 'airTemperature', 'windSpeed', 'windGust', 'windDirection', 'cloudCover', 'seaLevelPressure', 'relativeHumidity', 'totalPrecipitation', 'conditionCode']


global input_id

for n in range(0,len(r['forecastTimestamps'])):
    try:
        db_cur.execute('INSERT INTO meteo_schema.meteo_lt_lake (input_id,created_at) VALUES (DEFAULT,DEFAULT)')
        db_conn.commit()
        db_cur.execute('SELECT input_id FROM meteo_schema.meteo_lt_lake ORDER BY input_id DESC LIMIT 1')
        input_id=(db_cur.fetchone())[0]
    except Exception:
        db_conn.rollback()
        log.debug('Error on creating row for meteo_lt_lake')


    for p in place_list:
        try:
            input_val=r['place'][p]
            query=sql.SQL(f"UPDATE meteo_schema.meteo_lt_lake SET {p} = %s WHERE input_id = %s")
            db_cur.execute(query,(input_val,input_id,))
        except Exception:
            db_conn.rollback()
            log.debug('Error on inserting location data into meteo_lt_lake') 


    for i in info_list:
        try:
            input_val=r[i]
            query=sql.SQL(f"UPDATE meteo_schema.meteo_lt_lake SET {i} = %s WHERE input_id = %s")
            db_cur.execute(query,(input_val,input_id,))
            db_conn.commit()
        except Exception:
            db_conn.rollback()
            log.debug('Error on inserting forecast-type information')


    for c in r['place']['coordinates']:
        try:
            input_val=r['place']['coordinates'][c]
            query=sql.SQL(f"UPDATE meteo_schema.meteo_lt_lake SET {c} = %s WHERE input_id = %s")
            db_cur.execute(query,(input_val,input_id,))
            db_conn.commit()
        except Exception:
            db_conn.rollback()
            log.debug('Error on inserting coordinates in meteo_lt_lake')


    for f in forecast_list:
        try:
            input_val=r['forecastTimestamps'][n][f]
            query=sql.SQL(f"UPDATE meteo_schema.meteo_lt_lake SET {f} = %s WHERE input_id = %s")
            db_cur.execute(query,(input_val,input_id,))
            db_conn.commit()
        except Exception:
            db_conn.rollback()
            log.debug('Error on inserting forecast values')

try:
    db_conn.commit()
    db_cur.close()
    db_conn.close()
    log.info('[OK] Successful local DB disconnect.')
except Exception:
    log.error('Local DB diconnect error.')