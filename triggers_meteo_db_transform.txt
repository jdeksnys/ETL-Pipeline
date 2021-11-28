--trigger (on meteo_lt_lake) <<<<<<<<<<<<<<<<<<<<<<<<<
create or replace trigger meteo_lt_lake_new_entries
	after insert on meteo_schema.meteo_lt_lake
	for each row
	when ( date(new.forecastcreationtimeutc)=date(now()) ) 
	execute procedure meteo_schema.add_to_forecast_batch();



--trigger (on forecast_batch) <<<<<<<<<<<<<<<<<<<<<<<<
create or replace trigger meteo_batch_new_entries
	after insert on meteo_schema.forecast_batch
	for each row
	execute procedure meteo_schema.add_to_forecast_data();



--trigger function (on meteo_lt_lake) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
create or replace function meteo_schema.add_to_forecast_batch()
returns boolean
as
$$
begin
	
	if (select date(forecastcreationtimeutc) from meteo_schema.meteo_lt_lake order by created_at desc limit 1)
		not in (select date(forecast_creation_time_utc) from meteo_schema.forecast_batch) then
			
		insert into meteo_schema.forecast_batch (created_at,location_code,forecast_creation_time_utc,forecast_type_code)
			(select max(created_at),code,max(forecastcreationtimeutc),min(forecasttype)
			from meteo_schema.meteo_lt_lake
			where date(forecastcreationtimeutc) not in (select date(forecast_creation_time_utc) from meteo_schema.forecast_batch)
				and date(forecasttimeutc) not in (select date(forecast_time_utc) from meteo_schema.forecast_data)
				and date(forecasttimeutc)=date(forecastcreationtimeutc)+1
			group by date(forecasttimeutc),code);
		
		return null;
		
	else end if;
end;
$$
language plpgsql;



--function (on forecast_batch) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
create or replace function meteo_schema.add_to_forecast_data()
returns trigger
as
$$
declare
	last_fcast date;
	batch int;
	a varchar(30);
	b date;
	c float;
	d float;
	e float;
	f float;
	g float;
	h float;
	i float;
	j float;
	n float;
	
begin
last_fcast:=date(new.forecast_creation_time_utc);
batch:=new.forecast_batch_id;

insert into meteo_schema.forecast_data (forecast_data_id,forecast_batch_id)
	values (default, batch); --from meteo_schema.forecast_batch));new.forecast_creation_time_utc

execute format('create or replace view meteo_schema.f_view as
	(select * from meteo_schema.meteo_lt_lake
	 where date(forecastcreationtimeutc)=''%s''
	 and date(forecasttimeutc)=''%s'');',last_fcast,date(last_fcast)+1);

a:=(select conditioncode from meteo_schema.f_view group by conditioncode order by count(*) desc limit(1));
b:=(select date(forecasttimeutc) from meteo_schema.f_view limit 1);
c=(select avg(airtemperature) from meteo_schema.f_view);-- group by date(forecasttimeutc));
d:=(select avg(windspeed) from meteo_schema.f_view);
e:=(select avg(windgust) from meteo_schema.f_view);
f:=(select avg(winddirection) from meteo_schema.f_view);
g:=(select avg(cloudcover) from meteo_schema.f_view);
h:=(select avg(sealevelpressure) from meteo_schema.f_view);
i:=(select avg(relativehumidity) from meteo_schema.f_view);
j:=(select sum(totalprecipitation) from meteo_schema.f_view);
n:=new.forecast_batch_id; --(select max(forecast_batch_id) from meteo_schema.forecast_batch);

	execute format('update meteo_schema.forecast_data set 
			condition_code=''%s'',
			forecast_time_utc=''%s'',
			air_temperature=%s,
			wind_speed=%s,
			wind_gust=%s,
			wind_direction=%s,
			cloud_cover=%s,
			sea_level_pressure=%s,
			relative_humidity=%s,
			total_precipitation=%s
			where forecast_batch_id=%s;',a,b,c,d,e,f,g,h,i,j,n);
return null;
-- drop view if exists meteo_schema.f_view;
end;
$$
language plpgsql;