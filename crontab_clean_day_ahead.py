import psycopg2,logging

log_format='%(levelname)s %(asctime)s - (line:%(lineno)d) %(filename)s - %(message)s'
logging.basicConfig(filename='<>/log_day_ahead.log',
                    level=logging.DEBUG,
                    format=log_format)
log=logging.getLogger()



try:
    db_conn=psycopg2.connect(dbname=<db_name>,user=<db_user>,password=<db_pass>,host=<db_host>)
    db_cur=db_conn.cursor()
    log.info('[OK] Successful local DB connection.')
except Exception:
    log.error('Error in connecting to local DB.')



try:
    db_cur.execute('SELECT day_ahead_schema.upload_input_batch_info();')
    db_conn.commit()
    log.info('[OK] day_ahead transformed, uploaded to AWS RDS')
except Exception:
    log.error('Error function "day_ahead_schema.upload_input_batch_info()"')



try:
    db_cur.close()
    db_conn.close()
    log.info('[OK] Successful local DB disconnect.')
except Exception:
    log.error('Error in local DB disconnect.')