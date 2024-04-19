from pprint import pprint
import json
import os
import requests
import pandas as pd
from simple_salesforce import Salesforce, SalesforceLogin, SFType

# Salesforce credentialsS
username='intusergsprod@columbia.edu.uat'
password='Salesforce@2023'
security_token='5dZwwfOj6gIf0LtjDccntUba'
domain='test'


# Login to Salesforce
sf = Salesforce(username=username, password=password, security_token=security_token, domain=domain)

# Query to get ContentDocumentLinks for a specific object (e.g., a custom object or any other object)
query = """
SELECT ContentDocumentId, LinkedEntityId, ContentDocument.Title
FROM ContentDocumentLink
WHERE LinkedEntityId IN (SELECT Id FROM GS_Workflow__c  WHERE RecordTypeId = '0126e000001NcgaAAC' and CreatedDate  =YESTERDAY ) 
and IsDeleted = FALSE
"""
print(query)
# Executing the query
try:
    documents = sf.query_all(query)
    print(f"Total documents found: {documents['totalSize']}")
except Exception as e:
    print(f"Failed to query Salesforce: {e}")
    exit()

# Folder to save documents
output_folder = 'C:/Users/yl3627/downloads/folder'
os.makedirs(output_folder, exist_ok=True)
print(f"Documents will be saved in: {output_folder}")


 
# Download each document
for doc_link in documents['records']:
    content_document_id = doc_link['ContentDocumentId']
    try:
        # Fetching document details
        content_document = sf.ContentDocument.get(content_document_id)
        latest_version_id = content_document['LatestPublishedVersionId']

        # Fetching the actual file data
        content_version = sf.ContentVersion.get(latest_version_id)
        file_content_url = content_version['VersionData']

        # Check if the URL is complete; if not, prepend the base URL
        if not file_content_url.startswith('http'):
            file_content_url = 'https://' + sf.sf_instance + file_content_url

        # Authenticate and fetch the file content
        response = requests.get(file_content_url, headers={'Authorization': 'Bearer ' + sf.session_id})
        file_content = response.content if response.ok else None

        # Handle cases where the file could not be downloaded
        if file_content is None:
            raise ValueError(f"Failed to download content for {content_document_id}")

        file_path = os.path.join(output_folder, content_document['Title'])
        
        # Writing file to disk
        with open(file_path, 'wb') as file:
            file.write(file_content)
        print(f"Saved {content_document['Title']} to {file_path}")
    except Exception as e:
        print(f"Failed to download document {content_document_id}: {e}")
