-- Sets up tables for reclassification.  Requires recrods with Detail text.

drop materialized view if exists post_unauth_encamp_value;
drop materialized view if exists pre_unauth_encamp_value;

select min("Created Date")
from service_request_table t1
where t1."Service Request Type" like '%Unauthorized Encampment';

create materialized view post_unauth_encamp_value as
select "Service Request ID" as servreqid, "Service Request Type" as servreqtype
	   "Created Date" as createdate, "Details" as detailtext
from service_request_table
where "Details" is not null
and "Created Date" >= '2022-06-27';

create materialized view pre_unauth_encamp_value as
select "Service Request ID" as servreqid, "Service Request Type" as servreqtype
	   "Created Date" as createdate, "Details" as detailtext
from service_request_table
where "Details" is not null
and "Created Date" < '2022-06-27';

select count(*) from post_unauth_encamp_value;
select count(*) from pre_unauth_encamp_value;
