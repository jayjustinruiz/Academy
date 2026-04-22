/***without hierarchy*/

create or replace table db_name.schema_name.table_name as
select
data:name::string as Name,
data:city::string as City,
data:age:: int as Age
from db_name.schema_name.json_table_name;

/*** with hierarchy */

create or replace table db_name.schema_name.table_name as
select
data:name::string as Name,
data:city::string as City,
data:age:: int as Age,
data:address:street::string as Address_Street,
data:address:city::string as Address_City,
data:address:zip::int as Address_Zip
from db_name.schema_name.json_table_name;

/***without hierarchy with array */

create or replace table db_name.schema_name.table_name as
select
data:name::string as Name,
data:city::string as City,
data:age:: int as Age,
hobby.value::string as Hobby
-- data:hobbies::string as Hobbies,
-- Hobby.*,
from db_name.schema_name.json_table_name,
lateral flatten(input=>data:hobbies)as Hobby;

/***with hierarchy with array */

create or replace table db_name.schema_name.table_name as
select
data:student:id::int as Student_ID,
data:student:info:name::string as Name,
data:student:info:age::int as Age,
-- Flatten array and pull hierarchy values like normal (parameter after value is inner json key value pair)
Courses.value:course_name::string as Course_Name,
Courses.value:details:credits::int as Credits,
Courses.value:details:grade::string as Grades,
from db_name.schema_name.json_table_name,
lateral flatten(input=>data:student:courses)as Courses;

/***with hierarchy with multiple array */

create or replace table db_name.schema_name.table_name as
select
data:key1
data:key1:key2:value1
data:key1:key2:value2
data:key3ContainsArray
Alias.value:ArrayKey1
Alias2.value:ArrayKey1
Alias2.value:ArrayKey2
-- Flatten array and pull hierarchy values like normal (parameter after value is inner json key value pair)
from db_name.schema_name.json_table_name,
lateral flatten(input=>data:key3ContainsArray)as Alias
lateral flatten(input=>Alias.value:Array2Key)as Alias2
lateral flatten(input=>Alias2.value:Array3Key)as Alias3;

/*Array Containing Multiple Json */

create or replace table db_name.schema_name.table_name as
select
Alias.value:Key1:Value1::DataType
Alias.value:Key2:Value1::DataType
Alias.value:Key3:Value1::DataType
-- Flatten array and pull hierarchy values like normal (parameter after value is inner json key value pair)
from db_name.schema_name.json_table_name,
lateral flatten(input=>data)as Alias;


/*JSON Containing Multiple Json at a Key (nested JSON)*/

create or replace table db_name.schema_name.table_name as
select
data:JSON1Key
data:JSON1Key2:Value1::DataType
data:JSON1Key3:Value1::DataType
NestedJSONAlias.key::DataType -- Here we want to store the value of the Key i.e. Departments
NestedJSONAlias.value:InnerKey::DataType -- Here the values are JSONS and will need to be flattened before pulling the data i.e. Each Department has a JSON
NestedJSONAlias2.key::DataType -- Here we want to store the value of the Nested JSON Key i.e. Departments Information
NestedJSONAlias2.value:Value::DataType 
NestedJSONAlias2.value:InnerKey2::DataType -- Maybe another nested JSON which will have to be flattened and added
-- Flatten JSON and using the value of key at the start of the nest
from db_name.schema_name.json_table_name,
lateral flatten(input=>data:KeywithNestedJSON)as NestedJSONAlias
lateral flatten(input=>NestedJSONAlias.value:InneryKeywithNestedJSON)as NestedJSONAlias2;
