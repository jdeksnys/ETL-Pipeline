create schema aws_meteo_schema;

create schema aws_day_ahead_schema;

create table aws_meteo_schema.aws_forecast_data(
	forecast_data_id int,
	forecast_batch_id int ,
	condition_code varchar(20),
	forecast_time_utc timestamp,
	air_temperature float,
	wind_speed float,
	wind_gust float,
	wind_direction int,
	cloud_cover float,
	sea_level_pressure float,
	relative_humidity float,
	total_precipitation float);
	
create table aws_day_ahead_schema.aws_day_ahead_prices (
	price_data_id int,
	input_batch_id int,
	region_id int,
	day_ahead_price float);