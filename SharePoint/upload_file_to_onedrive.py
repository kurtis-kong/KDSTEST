from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
import sys
import os
sys.path.append(os.getcwd())


def get_sharepoint_context_using_user(url: str, username: str, password: str):
    """
    Auth by username and password
    args:
        url: sharepoint url for yourself or your team. 
        username: Your username or email. 
        password: Your password for your account.
    returns:
        ctx: Authentication
    """
    # Get sharepoint credentials
    sharepoint_url = url
    # Initialize the client credentials
    user_credentials = UserCredential(username, password)
    # create client context object
    ctx = ClientContext(sharepoint_url).with_credentials(user_credentials)
    return ctx


def create_sharepoint_directory(ctx: str, dir_name: str):
    """
    Creates a folder in the sharepoint directory even if the dir was exist.
    args:
        ctx: Authentication. You can got it from get_sharepoint_context_using_user().
        dir_name: The folder name in the OneDrive or SharePont Documents.
    Returns:
        relative_url: The path of file in the OneDrive. 
    """
    if dir_name:
        # add dir under your sharepoint -> Documents
        result = ctx.web.folders.add(f'Documents/{dir_name}').execute_query()
        if result:
            # documents is titled as Documents for relative URL in SP
            relative_url = f'Documents/{dir_name}'
            return relative_url


def upload_to_sharepoint(ctx: str, file_name: str, sp_relative_url: str):
    """
    Upload your file to sharepoint
    args:
        ctx: Authentication. You can got it from get_sharepoint_context_using_user().
        file_name: the local file path that you want to upload.
        sp_relative_url: Remote file path. You can got it from create_sharepoint_directory().
    returns:
        target_file: Remote file, Just for printing(logging).
    """
    # get remote folder path
    target_folder = ctx.web.get_folder_by_server_relative_url(sp_relative_url)
    # open local file
    with open(file_name, 'rb') as content_file:
        file_content = content_file.read()
        target_file = target_folder.upload_file(file_name, file_content).execute_query()
    return target_file


if __name__ == "__main__":
    import os
    os.environ['http_proxy'] = 'http://15.85.199.199:8080'
    os.environ['https_proxy'] = 'http://15.85.199.199:8080'

    url = '<url>'
    username = '<username>'
    password = '<password>'
    one_drive_dir_name = 'Install_result'
    local_file_name = 'install_result_1659598985.xlsx'

    # Auth by username and password
    ctx = get_sharepoint_context_using_user(url=url, username=username, password=password)
    # create dir on OneDrive
    relative_url = create_sharepoint_directory(ctx=ctx, dir_name=one_drive_dir_name)
    # upload file to OneDrive
    target_file = upload_to_sharepoint(ctx=ctx, file_name=local_file_name, sp_relative_url=relative_url)
    full_path = url + target_file.serverRelativeUrl
    print("File has been uploaded to url: {0}".format(full_path))
