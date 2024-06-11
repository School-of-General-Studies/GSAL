# Import necessary modules
#UAT Connection
#from sf_connection_uat import get_sf_connection
#Prod Connection
from sf_connection import get_sf_connection
from simple_salesforce import Salesforce, SalesforceMalformedRequest

# Import custom classes and email modules
from cls_add_user_to_group import SalesforceGroupManager
from cls_remove_user_from_group import SalesforceRemoveGroupManager
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to send email
def send_email(subject, body, to_email):
    from_email = "gsdevteam@columbia.edu"  # Replace with your email address 

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the SMTP server
        with smtplib.SMTP('send.columbia.edu') as s:
            s.sendmail(msg['From'], msg['To'], msg.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    # GS/GN Group - Add new users into the group
    group_id1 = '00G6e000005ZjEPEA0'
    user_field1 = 'Access_All_Groups__c'
    manager1 = SalesforceGroupManager(group_id1, user_field1)
    result1 = manager1.process_group_members()

    # Graduate school Advising Group - Add new grads to the group
    group_id2 = '00G6e000005ZjEUEA0'
    user_field2 = 'Graduate_School_Advising_Groups__c'
    manager2 = SalesforceGroupManager(group_id2, user_field2)
    result2 = manager2.process_group_members()

    # Remove users from GS/GN group
    group_id3 = '00G6e000005ZjEPEA0'
    user_field3 = 'Access_All_Groups__c'
    manager3 = SalesforceRemoveGroupManager(group_id3, user_field3)
    result3 = manager3.process_group_members_remove()

    # Prepare email content
    email_subject = "Salesforce Group Management Results"
    email_body = (
        "Add/Remove Pools Results:\n"
        f"Group: {user_field1}\n"
        f"Records inserted successfully: {result1['records_inserted']}\n\n"
        f"Group: {user_field2}\n"
        f"Records inserted successfully: {result2['records_inserted']}\n\n"
        f"Group: {user_field3}\n"
        f"Records removed successfully: {result3['records_Removed']}\n"
    )

    # Send the email
    send_email(email_subject, email_body, "yl3627@columbia.edu")  # Replace with the recipient's email address

if __name__ == '__main__':
    main()

 
