# API>local_db>AWS_RDS<br>

![alt text](https://github.com/jdeksnys/ETL-Pipeline/blob/main/diagram_pipeline.png)<br>
ETL pipeline diagram.<br>
<br>

## Aim of project
By creating a fully working pipeline:<br>
- Familiarise with ETL<br>
- Improve python (API,pandas), SQL (triggers&procedures) knowledge<br>
- Work with a cloud storage service<br>

## What does it do?
The data used is electricity prices and weather conditions. The pipeline is fully autonomous: scheduled daily (crontab), electricity price data (.xls) is dowloaded from an url, weather data fetched via an API, and inserted into a local database (Postgres). Next, it is being cleaned and transferred (PL/pgSQL) into 3NF-tables (see ERDs below). Lastly, the clean useful data is migrated to Amazon Web Services' RDS database via the foreign-fata wrapper in PL/pgSQL.<br>

![alt text](https://github.com/jdeksnys/ETL-Pipeline/blob/main/ERD_day_ahead.png)<br>
Price data ERD.<br>

![alt text](https://github.com/jdeksnys/ETL-Pipeline/blob/main/ERD_meteo_png.png)<br>
Weather data ERD<br>

## Further improvements/future learnings
- Switch from time to event based triggers<br>
- Upload data in batches, not 'for each row'<br>
- Prevent SQL injection<br>
