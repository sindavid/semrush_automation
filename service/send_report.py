import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.email import email
from email.mime.base import MIMEBase
from email import encoders


class SendReport:
    def __init__(self, file_path):
        self.__start_conection()
        self.__create_msg()
        self.__adding_file(file_path)
        self.__send_and_quit()

    def __start_conection(self):
        self.__server = smtplib.SMTP(email['host'], email['port'])
        self.__server.ehlo()
        self.__server.starttls()
        self.__server.login(email['user'], email['pwd'])

    def __create_msg(self):
        message = 'Hi!'
        self.__msg = MIMEMultipart()
        self.__msg['From'] = email['user']
        self.__msg['To'] = 'contato.david@outlook.com.br'
        self.__msg['Subject'] = 'Domain Report'
        self.__msg.attach(MIMEText(message, 'plain'))

    def __adding_file(self, file_path):
        attachment = open(file_path, 'rb')
        self.__att = MIMEBase('application', 'octet-stream')
        self.__att.set_payload(attachment.read())
        encoders.encode_base64(self.__att)
        self.__att.add_header('Content-Disposition', f'attachment; filename= {str(file_path).split("/")[-1]}')
        attachment.close()
        self.__msg.attach(self.__att)

    def __send_and_quit(self):
        self.__server.sendmail(self.__msg['From'], self.__msg['To'], self.__msg.as_string())
        self.__server.quit()

