from pprint import pprint
import json
import os
import requests
import pandas as pd
from simple_salesforce import Salesforce, SalesforceLogin, SFType

username='intusergsprod@columbia.edu.uat'
password='Salesforce@2023'
security_token='5dZwwfOj6gIf0LtjDccntUba'
domain='test'


session_id, instance = SalesforceLogin(username=username, password=password, security_token=security_token, domain=domain)
sf = Salesforce(instance=instance, session_id=session_id) 


querySOQL = """
           SELECT Id, Name, ParentId, Body 
           From Attachment 
           WHERE IsDeleted = false AND Parent.RecordTypeId = '0126e000001NcgaAAC'  and CreatedDate  = YESTERDAY
           """

response = sf.query(querySOQL)
lstRecords = response.get('records')
nextRecordsUrl = response.get('nextRecordsUrl')

while not response.get('done'):
    response = sf.query_more(nextRecordsUrl, identifier_is_url=True)
    lstRecords.extend(response.get('records'))
    nextRecordsUrl = response.get('nextRecordsUrl')

print (lstRecords)
df_records = pd.DataFrame(lstRecords)
instance_name = sf.sf_instance
folder_path = '//eos-cifs-1/obtest_share/Export/GS/WDLOA/SF_to_OB/SupportingDocs'

for row in df_records.iterrows():
    record_id = row[1]['ParentId']
    file_name = row[1]['Name']
    attachment_path = row[1]['Body']

    # Construct full URL for the attachment
    attachment_url = f'https://{instance_name}{attachment_path}'

    # Download attachment content
    request = sf.session.get(attachment_url, headers=sf.headers)

    if request.status_code == 200:
        # Specify the file path
        file_path = os.path.join(folder_path, file_name)

        # Save the attachment content to a file
        with open(file_path, 'wb') as f:
            f.write(request.content)
        print(f"Attachment '{file_name}' saved to '{file_path}'")
    else:
        print(f"Failed to download attachment '{file_name}'")
