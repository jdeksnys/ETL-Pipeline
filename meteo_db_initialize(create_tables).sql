create schema meteo_schema;

create table meteo_schema.meteo_lt_lake (
	input_id int serial primary key,
	created_at timestamp not null default now(),
	code varchar(30),
	name varchar(30),
	administrativeDivision varchar(200),
	country varchar(20),
	countryCode varchar(3),
	latitude float,
	longitude float,
	forecasttype varchar(20),
	forecastCreationTimeUtc timestamp,
	forecastTimeUtc timestamp,
	airTemperature float,
	windSpeed int,
	windGust int,
	windDirection int,
	cloudCover int,
	seaLevelPressure float,
	relativeHumidity int,
	totalPrecipitation float,
	conditionCode varchar(20)
	);

create table meteo_schema.forecast_type_list (
	forecast_type_code varchar(30) primary key,
	forecast_type_descr text);

create table meteo_schema.country_list(
	country_code varchar(2) primary key,
	country_name varchar(30) unique);

create table meteo_schema.region_list(
	region_id serial primary key,
	country_code varchar(2) references meteo_schema.country_list(country_code),
	region_name text unique);

create table meteo_schema.city_list(
	location_code varchar(40) primary key,
	region_id int references meteo_schema.region_list(region_id),
	city_name varchar(40) unique,
	latitude float,
	longitude float);

create table meteo_schema.forecast_batch(
	forecast_batch_id serial primary key,
	location_code varchar(20) references meteo_schema.city_list(location_code),
	forecast_type_code varchar(30) references meteo_schema.forecast_type_list(forecast_type_code) default 'long-term',
	created_at timestamp,
	forecast_creation_time_utc timestamp);
		
create table meteo_schema.condition_list(
	condition_code varchar(20) primary key,
	condition_descr text);

create table meteo_schema.forecast_data(
	forecast_data_id serial primary key,
	forecast_batch_id int references meteo_schema.forecast_batch(forecast_batch_id) on delete set null,
	condition_code varchar(20) references meteo_schema.condition_list(condition_code) on delete set null,
	forecast_time_utc timestamp,
	air_temperature float,
	wind_speed float,
	wind_gust float,
	wind_direction int,
	cloud_cover float,
	sea_level_pressure float,
	relative_humidity float,
	total_precipitation float);