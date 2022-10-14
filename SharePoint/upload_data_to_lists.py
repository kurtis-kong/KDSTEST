import sys
import os
import time
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
import pandas as pd
sys.path.append(os.getcwd())

# add proxy if needed
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''


# Get sharepoint credentials
sharepoint_url = "https://xxx.sharepoint.com/personal/kurtis_kong"
# Initialize the client credentials
user_credentials = UserCredential("<username>", "<password>")
# create client context object
ctx = ClientContext(sharepoint_url).with_credentials(user_credentials)

# 0. download excel from remote folder
# local_file_path = download_excel_for_install_result(remote_path='test_result')
local_file_path = ''

# 1. Load existing list items
target_list = ctx.web.lists.get_by_title("test")
# 2. delete all items
all_items = target_list.items.get_all().execute_query()
for item in all_items:
    item.delete_object()
ctx.execute_batch()
print("Items deleted count: {0}".format(len(all_items)))
# wait 1 min for deleting
time.sleep(60)

# 3. load data from excel
df1 = pd.read_excel(local_file_path)
# get total line number
line_num = len(df1.index.values)
# transfer to dic
all_data = df1.to_dict('list')

# 4. add item to lists
contacts_list = ctx.web.lists.get_by_title("test")
for num in range(line_num):
    add_data = {
        'Title': all_data['Title'][num],
        'installer_version': all_data['installer_version'][num],
        'physical_machine': all_data['physical_machine'][num],
        'vm_os': all_data['vm_os'][num],
        'vm_configuration': all_data['vm_configuration'][num],
        'success': all_data['success'][num],
        'failed': all_data['failed'][num],
        'install_mins': all_data['install_mins'][num],
        'error_log': all_data['error_log'][num],
        'testing_date': all_data['testing_date'][num]
    }
    contact_item = contacts_list.add_item(add_data)
    print('line+++', num, '/', line_num, contact_item.properties["Title"])
ctx.execute_batch()
# wait 2 mins for uploading in backend
time.sleep(120)
