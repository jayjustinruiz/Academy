import json 
import boto3
import io 
from io import StringIO
import pandas as pd

s3_client = boto3.client(s'3)

def lambda_handler(event, context): 
	try: 
		s3_Bucket_Name = ''
		s3_Source_FileName = 'data.csv'


		#read the file from the S3 bucket and create dataframe
		object = s3_client.get_object(Bucket = s3_Bucket_Name, Key= s3_Source_FileName)
		body = object['Body']
		csv_string = body.read().decode('utf-8')
		dataframe = pd.read_csv(StrinIO(csv_string))

		print(dataframe.head(3))
		print('Dataframe created sucessfully')

		#Write the dataframe to a CSV in the S3 bucket
		csv_buffer = StringIO()
		datafrane.to_csv(csv_buffer,index=False)
		csv_buffer.seek(0)

		s3_Target_Filename = 'lamda_data.csv'

		s3= boto3.resource('s3')
		s3.Object(s3_Bucket_Name, s3_Target_FileName).put(Body=csv_buffer.getvalue())
		Print('File sucessfully written to the S3 bucket')

	except Exception as err: 