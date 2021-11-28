create extension postgres_fdw;
select * from pg_extension;

CREATE SERVER aws_fdw_target_server Foreign Data Wrapper postgres_fdw OPTIONS (DBNAME '<dbname>', HOST '<host>', SSLMODE 'require');

CREATE USER MAPPING FOR jonas_deksnys SERVER aws_fdw_target_server OPTIONS (user '<user>',password '<pass>');

CREATE FOREIGN TABLE meteo_schema.aws_forecast_data_fdw (
	forecast_data_id int,
	forecast_batch_id int,
	condition_code varchar(20),
	forecast_time_utc timestamp,
	air_temperature float,
	wind_speed float,
	wind_gust float,
	wind_direction int,
	cloud_cover float,
	sea_level_pressure float,
	relative_humidity float,
	total_precipitation float)
SERVER aws_fdw_target_server OPTIONS (SCHEMA_NAME 'aws_mateo_schema', TABLE_NAME 'aws_forecast_data');
delete from meteo_schema.aws_forecast_data_fdw;



create or replace trigger aws_forecast_data_trigger 
	after insert on meteo_schema.forecast_data
	for each row
	execute procedure meteo_schema.insert_into_aws_forecast_data_fdw()

create or replace function meteo_schema.insert_into_aws_forecast_data_fdw()
returns trigger
as
$$
begin
insert into meteo_schema.aws_forecast_data_fdw (
	forecast_data_id,
	forecast_batch_id,
	condition_code,
	forecast_time_utc,
	air_temperature,
	wind_speed,
	wind_gust,
	wind_direction,
	cloud_cover,
	sea_level_pressure,
	relative_humidity,
	total_precipitation)
values (
	new.forecast_data_id,
	new.forecast_batch_id,
	new.condition_code,
	new.forecast_time_utc,
	new.air_temperature,
	new.wind_speed,
	new.wind_gust,
	new.wind_direction,
	new.cloud_cover,
	new.sea_level_pressure,
	new.relative_humidity,
	new.total_precipitation);
return null;
end;
$$
language plpgsql;




create or replace trigger aws_forecast_data_trigger_del
	before delete on meteo_schema.forecast_data
	for each row
	execute procedure meteo_schema.del_from_aws_forecast_data_fdw();

create or replace function meteo_schema.del_from_aws_forecast_data_fdw()
returns trigger
as
$$
begin
delete from meteo_schema.aws_forecast_data_fdw where forecast_data_id=old.forecast_data_id;
return old;
end;
$$
language plpgsql;