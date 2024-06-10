from cls_add_user_to_group import SalesforceGroupManager
from cls_remove_user_from_group import SalesforceRemoveGroupManager

def main():
    #GS/GN Group
    group_id1 = '00G6e000005ZjEPEA0'
    user_field1 = 'Access_All_Groups__c'
    manager1 = SalesforceGroupManager(group_id1, user_field1)
    manager1.process_group_members()

    #Graduate school Advising Group 
    group_id2 = '00G6e000005ZjEUEA0'
    user_field2 = 'Graduate_School_Advising_Groups__c'
    manager2 = SalesforceGroupManager(group_id2, user_field2)
    manager2.process_group_members()

    # remove users from GS/GN group in UAT
    group_id3 = '00GRT0000015fpx2AA'
    user_field3 = 'Access_All_Groups__c'
    manager3 = SalesforceRemoveGroupManager(group_id3, user_field3)
    manager3.process_group_members_remove()

if __name__ == '__main__':
    main()
