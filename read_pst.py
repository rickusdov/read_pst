from libratom.lib.pff import PffArchive
from email import generator
import pypff
from pathlib import Path
import time
import mysql.connector
#import pymysql

# def connect_to_db():
#     return 1
def save_eml(pstName):
    archive = PffArchive(pstName)
    eml_out = Path(Path.cwd() / "emls")
    if not eml_out.exists():
        eml_out.mkdir()
    for folder in archive.folders():
        if folder.get_number_of_sub_messages() != 0:
            for message in folder.sub_messages:
                name = message.subject.replace(" ", "_")
                name = name.replace("/", "-")
                filename = eml_out / f"{message.identifier}_{name}.eml"
                filename.write_text(archive.format_message(message))
                emailId = (message.identifier)

def extract_attachments_from_message(message, folder_name):
    attachments_info = []
    attachment_names = []

    for attachment in message.attachments:
        attachment_name = attachment.name or "Unknown"
        attachment_names.append(attachment_name)

    if attachment_names:
        info = f"{message.get_identifier()}^{folder_name}^{'____'.join(attachment_names)+'____'}"
        attachments_info.append(info)

    return attachments_info


def get_attachments_info(folder, folder_name, depth=0):
    attachments_info = []

    for message in folder.sub_messages:
        #print('id '+ message.entry_identifier)
        attachments_info.extend(extract_attachments_from_message(message, folder_name))

    for sub_folder in folder.sub_folders:
        attachments_info.extend(get_attachments_info(sub_folder, f"{folder_name}^{sub_folder.name}", depth + 1))

    return attachments_info

def read_pst_main(pst):
    #save_eml(pst)
    time.sleep(5)
    pst_file_path = pst
    pst = pypff.file()
    pst.open(pst_file_path)
    root_folder = pst.get_root_folder()
    attachments_info = get_attachments_info(root_folder, root_folder.name)

    # Traverse through the folders and subfolders
    for folder in root_folder.sub_folders:
        for sub in folder.sub_folders:
            # Traverse through the messages in the subfolder
            for message in sub.sub_messages:
                # Print the message_id
                print(message.entry_identifier)
    # for info in attachments_info:
    #     info = info.split('^')
    #     print(info[0] + ' ' + info[2] + ' ' + info[3])
    pst.close()
    return attachments_info