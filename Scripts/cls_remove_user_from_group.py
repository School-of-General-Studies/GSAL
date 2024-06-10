from sf_connection_uat import get_sf_connection
from simple_salesforce import Salesforce, SalesforceMalformedRequest
from datetime import datetime


sf = get_sf_connection()

class SalesforceRemoveGroupManager:
    def __init__(self, group_id, user_field):
        self.group_id = group_id
        self.user_field = user_field
        self.sf = get_sf_connection()
        self.remove_count = 0

    def fetch_groupmenber(self):
       
        querySOQL = f"""
        SELECT Id
        FROM  GroupMember
        WHERE  GroupId = '{self.group_id}' AND  UserOrGroupId IN (
            SELECT ID FROM User WHERE  IsActive = true And  {self.user_field} = False
        )
        """

        print (querySOQL )
        result = self.sf.query(querySOQL)
        return result['records']

    def remove_users_from_group(self, groupmembers):
        new_records = [{'ID': groupmember['Id'], 'GroupId': self.group_id} for groupmember in groupmembers]
        if new_records:
            print(f"Attempting to remove {len(new_records)} users.")
            for new_record in new_records:
                try:
                    res = self.sf.GroupMember.delete(new_record)
                    if 'success' in res and res['success']:
                        print(f"Record inserted successfully, Id: {res['id']}")
                        self.insert_count += 1
                    else:
                        print(f"Error inserting record: {res.get('errors', 'Unknown error')}")
                except SalesforceMalformedRequest as e:
                    print(f"An error occurred: {e}")

    def process_group_members_remove(self):
        users = self.fetch_groupmenber()
        if users:
            self.remove_users_from_group(users)
        else:
            print("No records to insert.")
        print(f"Records remove successfully: {self.remove_count}")
