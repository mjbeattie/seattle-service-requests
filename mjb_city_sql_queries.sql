/*
Seattle FindIt-FixIt Project
University of Oklahoma
March 3, 2024
*/

/*
Create a materialized view that shows activites in order for each service request
*/
create materialized view seattle_city_data.public.activity_order as
select
	*,
	MAX(activity_order) OVER (PARTITION BY "Service Request ID") AS max_activity_number
from
(
	select
		sr."Service Request ID",
		sr."Service Request Type",
		sr."Created Date",
		sr."Status",
		act."Activity ID", 
		act."Activity Type", 
		act."Outcome",
		act."Activity Details",
		act."Activity Created Date", 
		act."Activity Completed Date",
		ROW_NUMBER() OVER (PARTITION BY sr."Service Request ID" ORDER BY "Activity ID" asc) AS activity_order
	from
		(select
			"Service Request ID",
			"Service Request Type",
			"Created Date",
			"Status"
		from service_request_table) as sr
	join
		(select 
			"Service Request ID", 
			"Activity ID", 
			"Activity Type", 
			"Outcome",
		 	"Activity Details",
			"Activity Created Date", 
			"Activity Completed Date"
		from activity_table) as act
	on sr."Service Request ID" = act."Service Request ID"
	order by sr."Service Request ID", act."Activity ID"
) as t1;
	
select * from activity_order;

/*
Create a view that calculates the elapsed time in hours from when an issue was
reported to when its final activity was recorded as complete.
*/
create materialized view elapsed_time as
select
	*,
	ROUND(EXTRACT(EPOCH FROM ("Activity Completed Date" - "Created Date"))/3600, 4) AS duration_hours
from activity_order
where activity_order = max_activity_number
order by "Service Request ID" asc;

select * from elapsed_time;


/* Cleanup the views if necessary */
--drop materialized view activity_order cascade;
--drop materialized view elapsed_time;

/* Calculate the average time to complete a request by service type */
select "Service Request Type", avg(duration_hours)
from elapsed_time
group by "Service Request Type"
order by "Service Request Type";
