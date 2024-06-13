#UAT connection
from simple_salesforce import Salesforce

def get_sf_connection():
    sf = Salesforce(
        username='intusergsprod@columbia.edu.uat',
        password='Salesforce@2023',
        security_token='5dZwwfOj6gIf0LtjDccntUba',
        domain='test'   
    )
    return sf
