from sf_connection import get_sf_connection
from simple_salesforce import Salesforce, SalesforceMalformedRequest
from datetime import datetime


sf = get_sf_connection()

class SalesforceGroupManager:
    def __init__(self, group_id, user_field):
        self.group_id = group_id
        self.user_field = user_field
        self.sf = get_sf_connection()
        self.insert_count = 0

    def fetch_users(self):
        querySOQL = f"""
        SELECT Id
        FROM User
        WHERE IsActive = true AND {self.user_field} = True AND Id NOT IN (
            SELECT UserOrGroupId FROM GroupMember WHERE GroupId = '{self.group_id}'
        )
        """
        result = self.sf.query(querySOQL)
        return result['records']

    def add_users_to_group(self, users):
        new_records = [{'UserOrGroupId': user['Id'], 'GroupId': self.group_id} for user in users]
        if new_records:
            print(f"Attempting to insert {len(new_records)} users.")
            for new_record in new_records:
                try:
                    res = self.sf.GroupMember.create(new_record)
                    if 'success' in res and res['success']:
                        print(f"Record inserted successfully, Id: {res['id']}")
                        self.insert_count += 1
                    else:
                        print(f"Error inserting record: {res.get('errors', 'Unknown error')}")
                except SalesforceMalformedRequest as e:
                    print(f"An error occurred: {e}")

    def process_group_members(self):
        users = self.fetch_users()
        if users:
            self.add_users_to_group(users)
        else:
            print("No records to insert.")
        print(f"Records inserted successfully: {self.insert_count}")
