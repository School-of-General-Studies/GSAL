# Import necessary modules
from sf_connection_uat import get_sf_connection
from simple_salesforce import Salesforce, SalesforceMalformedRequest

# Establish Salesforce connection
sf = get_sf_connection()

class SalesforceRemoveGroupManager:
    def __init__(self, group_id, user_field):
        """
        Initialize the SalesforceRemoveGroupManager with group ID and user field.
        """
        self.group_id = group_id
        self.user_field = user_field
        self.sf = get_sf_connection()
        self.remove_count = 0

    def fetch_groupmenber(self):
        """
        Fetch members of the group who are active users and do not meet the criteria specified by user_field.
        """
        querySOQL = f"""
        SELECT Id
        FROM GroupMember
        WHERE GroupId = '{self.group_id}' AND UserOrGroupId IN (
            SELECT ID FROM User WHERE IsActive = true And {self.user_field} = False
        )
        """
        result = self.sf.query(querySOQL)
        return result['records']

    def remove_users_from_group(self, groupmembers):
        """
        Remove the fetched group members from the specified group.
        """
        ids_to_delete = [{'ID': groupmember['Id'], 'GroupId': self.group_id} for groupmember in groupmembers]
        if ids_to_delete:
            print(f"Attempting to remove {len(ids_to_delete)} users.")
            for id_to_delete in ids_to_delete:
                try:
                    res = self.sf.GroupMember.delete(id_to_delete)
                    if 'success' in res and res['success']:
                        print(f"Record deleted successfully, Id: {res['id']}")
                        self.remove_count += 1
                    else:
                        print(f"Error deleting record: {res.get('errors', 'Unknown error')}")
                except SalesforceMalformedRequest as e:
                    print(f"An error occurred: {e}")

    def process_group_members_remove(self):
        """
        Process the group members by fetching them and removing them from the group.
        """
        groupmembers = self.fetch_groupmenber()
        if groupmembers:
            self.remove_users_from_group(groupmembers)
        else:
            print("No records to delete.")
        print(f"Records removed successfully: {self.remove_count}")
        return {
            'records_Removed': self.remove_count
        }
