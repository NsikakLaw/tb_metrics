-- Assumptions
-- 1. More than 24 hours work time is allowed, as far as the start time is 12 hours prior to the window start time i.e. '2022-04-15 09:00:00.000'
-- 2. For clarity and cleaner results, we are calculating just the integer full hours worked i.e. (10.34 -> 10)
with time_calculations as (
  select employee_id,
  first_name,
  last_name,
  hourly_wage,
  start_time,
  end_time,

  case
  	when start_time >= '2022-04-15 09:00:00.000' and start_time <= '2022-04-17 17:00:00.000' then start_time
  	when start_time <= '2022-04-15 09:00:00.000' then '2022-04-15 09:00:00.000'
  else null
  	end as calculate_start_time,

  case
  	when end_time >= '2022-04-17 17:00:00.000' then '2022-04-17 17:00:00.000'
  	when end_time <= '2022-04-17 17:00:00.000' and end_time >= '2022-04-15 09:00:00.000' then end_time
  	when end_time is null then
  		case
  			when start_time > '2022-04-15 09:00:00.000' then '2022-04-17 17:00:00.000'
  		  	when start_time < '2022-04-15 09:00:00.000' and EXTRACT(EPOCH FROM CAST('2022-04-15 09:00:00.000' AS TIMESTAMP) - start_time)/60/60 <= 12 then CAST('2022-04-15 09:00:00.000' AS TIMESTAMP)
  		else null
  		end
  end as calculate_end_time

  from employee_activity)

,
  hourly_calculations as (
      select employee_id,
 		first_name,
		last_name,
		hourly_wage,
		start_time,
		end_time,
 		TRUNC(EXTRACT(EPOCH FROM calculate_end_time - calculate_start_time)/60/60 )as hours_worked,
		calculate_end_time,
 		calculate_start_time

    from time_calculations)

  select employee_id, first_name, last_name,
  sum(hourly_wage * hours_worked) as total_amount from hourly_calculations
  group by employee_id, first_name, last_name
