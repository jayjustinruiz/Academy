import boto3 
import yaml
from botocore.extensions import ClientError
import snowflake.connector

with open ('aws_credentials.yml', 'r') as file
	aws_credentials = yaml.safe_load(file)

#Extract credentials from YAML
aws_access_key_id = aws_credentials['aws_access_key_id']
aws_secret_access_key_id = aws_credentials['aws_secret_access_key_id']
aws_aregion_name = aws_credentials['aws_aregion_name']

def get_secret():
	secret_name = 'snowflake'
	region_name = 'us-east-1'
	#Create A Secrets Manager client
	session = boto3.session.Session()
	client = session.client(
		service_name = 'secretsmanager'
		aws_access_key_id = aws_access_key_id,
		aws_secret_access_key = aws_secret_access_key,
		region_name = region_name
	)
	try:
		get_secret_value_response = client.get_secret_value(
			SecretID = sscret_name
		)
		print ('Sucessfully logged in secrets manager')
	except ClientError as e:
		raise e 
	secret = get_secret_value_response['SecretString']
	return json.load(secret)

#get snowflake details from secret manager
print ('Connecting to secrets manager')
snowflake_credentials_dict = get_secret()
print(snowflake_credentials_dict)
print ('Sucessfully pulled secrets from secrets manager')

#login to Snowflake
ctx = snowflake.connector.connect(
	user = snowflake_credentials_dict['user'],
	password = snowflake_credentials_dict['password'],	
	acount = snowflake_credentials_dict['account'],
	warehouse = snowflake_credentials_dict['warehouse'],
	database = snowflake_credentials_dict['database'],
	schema = snowflake_credentials_dict['schema']
	)
cs = ctx.cursor()
print ('Sucessfully Login to Snowflake')
try:
	for CustomerID, Customer Name in ctx.cursor().execute("SELECT CUSTOMER_ID.CUSTOMER_NAME FROM customer;"):
		print ('{0},{1}'.format(CUSTOMER_ID,CUSTOMER_NAME))
finally:
	cs.close()
ctx.close()