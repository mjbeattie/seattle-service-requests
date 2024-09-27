create materialized view pre_encamp_value_reqs_reclass
as
select
	servreqid as "Service Request ID",
	text as alldetails,
	case when newlabel = 9 then newid
		else id
	end as "Service Request Type"
from
	pre_encamp_value_reclass_reqs;
	
select count(*) from pre_encamp_value_reqs_reclass;