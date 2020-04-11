# -*- coding: UTF-8 -*-
import codecs
import importlib
import json
import smtplib
import sys
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
importlib.reload(sys)


# 发送邮件
def send_mail(mail_config, mail_port, to, subject, msg, image_path):
    smtpserver = smtplib.SMTP(mail_config['server'], mail_port)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()  # extra characters to permit edit
    username = mail_config['username']
    password = mail_config['password']
    smtpserver.login(mail_config['username'], password)

    emsg = MIMEMultipart('related')
    # emsg = MIMEText(content, 'plain', 'utf-8')
    content = MIMEText('<html><h3>' + msg + '</h3><body><img src="cid:imageid" alt="imageid"></body></html>', 'html',
                       'utf-8')  # 正文
    emsg.attach(content)
    file = open(image_path, "rb")
    img_data = file.read()
    file.close()
    img = MIMEImage(img_data)
    img.add_header('Content-ID', 'imageid')
    emsg.attach(img)
    emsg['From'] = username
    emsg['To'] = to
    emsg['Subject'] = Header(subject, 'utf-8').encode()
    smtpserver.sendmail(username, to, emsg.as_string())
    print('done!')
    smtpserver.quit()


def fast_send(to, subject, msg, image_path):
    useremail_json = "useremail.json"
    mail_config = json.load(open(useremail_json, "rb"))
    mail_port = 25
    send_mail(mail_config[0], mail_port, to, subject, msg, image_path)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('命令格式有误@')
        exit(1)
    to = sys.argv[1]
    subject = sys.argv[2]
    msg = sys.argv[3]
    if len(sys.argv) < 5:
        n = 1
    else:
        n = int(sys.argv[4])
    for i in range(1, n + 1):
        fast_send(to, subject, msg)
