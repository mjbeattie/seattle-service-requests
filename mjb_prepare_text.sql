/*
mjb_prepare_text.sql
April 13, 2024
University of Oklahoma

This script examines the number of service requests that have answers to the question
'What is the nature of your request?'  It then creates a materialized view that
concatenates customer detail from the service request with the answer into one field.
The view is then downloaded into two files - one with requests prior to the create of
the Unauthorized Encampment value and one after.  These files will be used for
categorization using an LLM.
*/
--Clean up old files
DROP MATERIALIZED VIEW IF EXISTS flex_question_count;
DROP MATERIALIZED VIEW IF EXISTS alldetail_text;
DROP MATERIALIZED VIEW IF EXISTS flex_analysis;

--Check what is the nature of your inquiry results.  Note a materialized view was
--required to overcome memory constraints on the server.
CREATE MATERIALIZED VIEW flex_analysis AS
SELECT
	t1."Service Request ID",
	t1."Service Request Type",
	t2."Flex Question"
FROM service_request_table t1
JOIN custom_attributes_table t2
ON t1."Service Request ID" = t2."Service Request ID";

CREATE MATERIALIZED VIEW flex_question_count AS
SELECT t2."Service Request Type", t2."Flex Question", COUNT(*) AS t2cnt
FROM flex_analysis t2
WHERE t2."Flex Question" = 'What is the nature of your inquiry?'
GROUP BY t2."Service Request Type", t2."Flex Question";

SELECT t3."Service Request Type", t4."Flex Question", t3.t1cnt, t4.t2cnt
FROM
	(
		SELECT t1."Service Request Type", COUNT(*) AS t1cnt
		FROM flex_analysis t1
		GROUP BY t1."Service Request Type"
	) t3
LEFT JOIN flex_question_count t4
ON t3."Service Request Type" = t4."Service Request Type";


-- Create the view with the concatenated details
CREATE MATERIALIZED VIEW alldetail_text AS
SELECT
    t1."Service Request ID",
    t1."Created Date",
    t1."Service Request Type",
    t1."Details",
    t3."Flex Question Answer",
	CONCAT(t1."Details", ' ', t3."Flex Question Answer") AS alldetails
FROM
    service_request_table t1
LEFT JOIN
	(
		SELECT
			t2."Service Request ID", 
			t2."Flex Question Answer"
		FROM
			custom_attributes_table t2
		WHERE
			t2."Flex Question" = 'What is the nature of your inquiry?'
			AND t2."Flex Question Answer" IS NOT NULL
	) t3
ON
    t1."Service Request ID" = t3."Service Request ID";

SELECT * FROM alldetail_text;


--Find the date range for Unauthorized Encampment
SELECT MIN(t1."Created Date"), MAX(t1."Created Date")
FROM alldetail_text t1
WHERE t1."Service Request Type" LIKE '%Unauthorized Encampment';


--Create view of post-encampment data for download
CREATE MATERIALIZED VIEW post_encamp_value_reqs AS
	SELECT t1."Service Request ID", t1."Service Request Type", t1."alldetails"
	FROM alldetail_text t1
	WHERE t1."Created Date" > '2022-06-26'
	AND t1."alldetails" IS NOT NULL
	AND t1."alldetails" <> ' ';


--Create view of pre-encampment data for download
CREATE MATERIALIZED VIEW pre_encamp_value_reqs AS
	SELECT t1."Service Request ID", t1."Service Request Type", t1."alldetails"
	FROM alldetail_text t1
	WHERE t1."Created Date" < '2022-06-27'
	AND t1."alldetails" IS NOT NULL
	AND t1."alldetails" <> ' ';


--Clean up files
DROP MATERIALIZED VIEW IF EXISTS flex_question_count;
DROP MATERIALIZED VIEW IF EXISTS flex_analysis;

