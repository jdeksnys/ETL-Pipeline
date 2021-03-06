create or replace trigger input_batch_info_new_entries
	after insert on day_ahead_schema.input_batch_info
	for each row
	execute procedure day_ahead_schema.upload_day_ahead_prices();



--function for batch_info update <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
create or replace function day_ahead_schema.upload_input_batch_info()
returns boolean
as
$$
declare 
	list_val date;
begin

	for list_val in (select distinct(date(price_date)) from day_ahead_schema.day_ahead_lake order by price_date desc) loop
	
		if (list_val not in (select date(price_date) from day_ahead_schema.input_batch_info)) then
			insert into day_ahead_schema.input_batch_info (
				input_batch_id,
				currency_id,
				price_date,
				uploaded_at)
			values(
				default,
				(select currency_id from day_ahead_schema.currency_list where currency_code=
					(select currency from day_ahead_schema.day_ahead_lake where price_date=list_val limit 1)),
				(list_val),
				(select date(uploaded_at) from day_ahead_schema.day_ahead_lake where price_date=list_val
				 	order by uploaded_at desc limit 1));
		end if;
		
	end loop;
return null;
end;
$$
language plpgsql;



create or replace function day_ahead_schema.upload_day_ahead_prices()
returns trigger
as
$$
declare
	region varchar;
begin
for region in (select region_code from day_ahead_schema.region_list) loop
	execute format('insert into day_ahead_schema.day_ahead_prices (
						   price_data_id,
						   input_batch_id,
						   region_id,
						   day_ahead_price)
					values (
				   			default,
							%s,
							(select region_id from day_ahead_schema.region_list where region_code=''%s''),
							(select day_ahead_price/100 from day_ahead_schema.day_ahead_lake
							where region=''%s'' and price_date=''%s''));',new.input_batch_id,region,region,new.price_date);
end loop;
return null;
end;
$$
language plpgsql;