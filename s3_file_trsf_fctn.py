import boto3
from simple_salesforce import Salesforce
import datetime

def send_attachment_to_s3(attachment_id, case_id):
    # Connect to Salesforce
    sf = Salesforce(username='your_username', password='your_password', security_token='your_token')

    # Retrieve the attachment data from Salesforce
    attachment = sf.query("SELECT Id, Body, LastModifiedDate FROM Attachment WHERE Id = '" + attachment_id + "'")['records'][0]

    # Get the last accessed date
    last_accessed_date = datetime.datetime.strptime(attachment['LastModifiedDate'], '%Y-%m-%dT%H:%M:%S.%fZ')

    # check if the last accessed date is older than 1 year
    if last_accessed_date < (datetime.datetime.now() - datetime.timedelta(days=365)):
      # Bundle the attachment data with the case object ID
      bundle = {'attachment_data': attachment['Body'], 'case_id': case_id}

      # Connect to the S3 bucket
      s3 = boto3.client('s3')

      # Send the bundled payload to the S3 bucket
      s3.put_object(Bucket='your_bucket_name', Key='attachment_' + attachment_id, Body=bundle)
    else:
      print("Attachment is not older than 1 year, it will not be sent to S3.")
