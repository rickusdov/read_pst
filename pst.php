
import pypff

pst_file = pypff.file()
pst_file.open('test.pst')

root = pst_file.get_root_folder()

# iterate through all subfolders
for folder in root.sub_folders:

    print(f'Folder: {folder.name}')

    # loop through all emails in the folder
    for email in folder.sub_items:

        if email.message_class == 'IPM.Note':

            print(f'Subject: {email.subject}')
            print(f'Sender: {email.sender_name} <{email.sender_email_address}>')
            print(f'To: {email.get_display_to()}')
            print(f'Sent: {email.sent_on}')
            print(f'Received: {email.received_on}')
            print(f'Body: {email.plain_text_body}')

pst_file.close()