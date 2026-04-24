import boto3

# Create session using AWS profile
session = boto3.Session(profile_name="dea-scd2-user")

# Connecting to AWS S3 using that session
s3_resource = session.resource('s3', region_name='us-east-1')


# Function to upload file in S3
def s3_upload(file_name, fold, bkt):

    s3_bucket = s3_resource.Bucket(name=bkt)

    s3_bucket.upload_file(
        Filename=file_name,
        Key=fold + '/' + file_name
    )

    return True


if __name__ == '__main__':

    file_name = 'Product_Dim.csv'
    s3_folder = 'raw_data'
    bucket = 'dea-scd2project-277361137027-us-east-1-an'

    status = s3_upload(file_name, s3_folder, bucket)

    if status:
        print('Data is saved')
    else:
        print('Error while loading data...')