create schema day_ahead_schema;

create table day_ahead_schema.day_ahead_lake(
	input_id serial primary key,
	uploaded_at timestamp default now(),
	region varchar(50),
	price_date date,
	day_ahead_price float,
	currency varchar(3));

create table day_ahead_schema.currency_list (
	currency_id serial primary key,
	currency_code varchar(3),
	currency_name varchar(30)
	);

create table day_ahead_schema.input_batch_info (
	input_batch_id int primary key,
	currency_id int references day_ahead_schema.currency_list (currency_id) default 1,
	price_date date,
	uploaded_at date
	);

create table day_ahead_schema.country_list (
	country_id serial primary key,
	country_code varchar(2),
	country_name varchar(30)
	);

create table day_ahead_schema.region_list (
	region_id serial primary key,
	country_id int references day_ahead_schema.country_list (country_id),
	region_code varchar(10),
	region_name varchar(40)
	);

create table day_ahead_schema.day_ahead_prices (
	price_data_id serial primary key,
	input_batch_id int references day_ahead_schema.input_batch_info (input_batch_id),
	region_id int references day_ahead_schema.region_list (region_id),
	day_ahead_price float
	);

select table_name from information_schema.tables where table_schema='public';
select * from country_list;

insert into day_ahead_schema.country_list (country_id,country_code,country_name) values
	(default,'SE','Sweden'),
	(default,'FI','Finland'),
	(default,'DK','Denmark'),
	(default,'NO','Norway'),
	(default,'EE','Estonia'),
	(default,'LV','Latvia'),
	(default,'LT','Lithuania'),
	(default,'AT','Austria'),
	(default,'BE','Belgium'),
	(default,'DE','Germany'),
	(default,'FR','France'),
	(default,'NL','Netherlands');

insert into day_ahead_schema.region_list (region_id,country_id,region_code,region_name) values
	(default,(select country_id from day_ahead_schema.country_list where country_name='Sweden'),'SE1','Luleå'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Sweden'),'SE2','Sundsvall'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Sweden'),'SE3','Stockholm'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Sweden'),'SE4','Malmö'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Finland'),'FI','Finland'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Denmark'),'DK1','Denmark West'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Denmark'),'DK2','Denmark East'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Norway'),'Oslo','Oslo'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Norway'),'Kr_sand','Kristiansand'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Norway'),'Bergen','Bergen'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Norway'),'Molde','Molde'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Norway'),'Tr_heim','Trondheim'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Norway'),'Tromsoe','Tromsø'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Estonia'),'EE','Estonia'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Latvia'),'LV','Latvia'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Lithuania'),'LT','Lithuania'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Austria'),'AT','Austria'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Belgium'),'BE','Belgium'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Germany'),'DE_LU','Germany&Luxembourg'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='France'),'FR','France'),
	(default,(select country_id from day_ahead_schema.country_list where country_name='Netherlands'),'NL','The Netherlands');

insert into day_ahead_schema.currency_list (currency_id,currency_code,currency_name) values (default,'EUR','Euro');