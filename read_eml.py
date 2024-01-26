import eml_parser
import os
import email
from email import policy
from email.utils import parsedate_to_datetime
from email.header import decode_header
import base64
from email.parser import BytesParser
from email import message_from_file
import re
import chardet
from read_pst import read_pst_main, save_eml

def get_list_of_eml():
    path = 'emlss'
    dir_list = os.listdir(path)
    # prints all files
    return (dir_list)

def get_mail_id():
    temp = ''
    files = get_list_of_eml()
    for file in files:
        file = file.split('_')
        emailId = file[0]
        temp += emailId + '^'
    idList = temp.split('^')
    return idList
def json_serial(obj):
  if isinstance(obj, datetime.datetime):
      serial = obj.isoformat()
      return serial
def read_eml_body(eml_path):
    eml_path = 'emlss/'+eml_path
    with open(eml_path) as email_file:
        email_message = email.message_from_file(email_file)
        return (email_message.get_payload())
def message_to_dict(msg):
    data = {}
    data['subject'] = msg['subject']
    data['from'] = msg['from']
    data['to'] = msg['to']
    if msg.is_multipart():
        data['body'] = [part.get_payload() for part in msg.iter_parts()]
    else:
        data['body'] = msg.get_payload()
    return data
def get_data(eml_path,type):
    eml_path = 'emlss/'+eml_path
    with open(eml_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    data = message_to_dict(msg)
    return data[type]
def get_date(eml_path):
    eml_path = 'emlss/'+eml_path
    with open(eml_path, 'r', encoding='utf-8') as eml_file:
        msg = email.message_from_file(eml_file)
        date_str = msg.get('Date')
        if date_str:
            date_obj = parsedate_to_datetime(date_str)
            date = str(date_obj).split('+')
            date = date[0]
            return date
def get_imap_uid_from_eml(eml_file_path):
    eml_file_path = 'emlss/'+eml_file_path
    with open(eml_file_path, 'r', encoding='utf-8') as eml_file:
        msg = email.message_from_file(eml_file)
        message_id = msg.get('Message-ID')

        if message_id:
            match = re.search(r'\d+', message_id)
            if match:
                imap_uid = match.group()
                return imap_uid


def get_attachment_name(eml_file_path):
    eml_file_path = 'emlss/'+ eml_file_path
    with open(eml_file_path, 'rb') as eml_file:
        msg = BytesParser(policy=policy.default).parse(eml_file)

        attachment_names = []
        for part in msg.iter_parts():
            content_disposition = part.get('Content-Disposition')
            if content_disposition and 'filename' in content_disposition:
                filename, encoding = decode_header(content_disposition)[0]
                if isinstance(filename, bytes):
                    attachment_names.append(filename.decode(encoding or 'utf-8'))
                else:
                    attachment_names.append(filename)

        return attachment_names
def get_message_id(eml_file_path):
    eml_file_path = 'emlss/'+eml_file_path
    with open(eml_file_path, 'rb') as eml_file:
        msg = BytesParser(policy=policy.default).parse(eml_file)
        message_id = msg.get('Message-ID')
        return message_id


def detect_encoding(text):
    result = chardet.detect(text)
    #print(result)
    return result['encoding']
if __name__ == '__main__':
    pst = 'dummy.pst'
    pstData = read_pst_main(pst)
    # save_eml(pst)
    files = get_list_of_eml()
    id = get_mail_id()
    for i in range(0,len(files)):
        eml = files[i]

        for line in pstData:
            line = line.split('^')
            #print(line[2] + ' // '+ line[3])
            if line[0] == id[i]:
                date = (get_date(eml))
                sender = get_data(eml,'from')
                reciever = get_data(eml, 'to')
                subject = str(get_data(eml, 'subject')).replace('Ä…', 'ą').replace('ÄÆ', 'į').replace('Ä®',
                                                                                                      'Į').replace('Å',
                                                                                                                   'š').replace(
                    'Å¾', 'ž')
                message_id = str(get_message_id(eml))
                print(message_id + ' // '+ id[i] + ' // '+subject+' // '+sender+' // '+reciever +'// // // '+date+ ' // '+ ' // body // '+ line[2] + ' // ' + eml + ' // ' + line[3] ) 