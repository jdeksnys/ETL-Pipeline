create extension postgres_fdw;
select * from pg_extension;

CREATE FOREIGN TABLE day_ahead_schema.aws_day_ahead_prices_fdw (
	price_data_id int,
	input_batch_id int,
	region_id int,
	day_ahead_price float)
SERVER aws_fdw_target_server
OPTIONS (SCHEMA_NAME 'aws_day_ahead_schema', TABLE_NAME 'aws_day_ahead_prices');

create or replace trigger aws_day_ahead_prices_trigger
	after insert on day_ahead_schema.day_ahead_prices
	for each row
	execute procedure day_ahead_schema.insert_into_aws_day_ahead_prices();

create or replace function day_ahead_schema.insert_into_aws_day_ahead_prices()
returns trigger
as
$$
begin
insert into day_ahead_schema.aws_day_ahead_prices_fdw (
	price_data_id,
	input_batch_id,
	region_id,
	day_ahead_price)
values (
	new.price_data_id,
	new.input_batch_id,
	new.region_id,
	new.day_ahead_price);
return null;
end;
$$
language plpgsql;

create or replace trigger aws_day_ahead_prices_trigger_del
	before delete on day_ahead_schema.day_ahead_prices
	for each row
	execute procedure day_ahead_schema.del_from_aws_day_ahead_prices();
	
create or replace function day_ahead_schema.del_from_aws_day_ahead_prices()
returns trigger
as
$$
begin
delete from day_ahead_schema.aws_day_ahead_prices_fdw where price_data_id=old.price_data_id;
return old;
end;
$$
language plpgsql;