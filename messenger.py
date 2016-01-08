import smtplib
import mimetypes
import email
import email.mime.application

from settings import SETTINGS


# http://stackoverflow.com/a/8243031/979255
def send_file(filename):
    m = email.mime.Multipart.MIMEMultipart()
    m['Subject'] = ''
    m['From'] = SETTINGS['GMAIL_EMAIL']
    m['To'] = SETTINGS['KINDLE_EMAIL']

    fp = open(filename, 'rb')
    att = email.mime.application.MIMEApplication(fp.read(),
                                                 _subtype="x-mobipocket-ebook")
    fp.close()
    att.add_header('Content-Disposition', 'attachment', filename=filename)
    m.attach(att)

    s = smtplib.SMTP('smtp.gmail.com')
    s.starttls()
    s.login(SETTINGS['GMAIL_EMAIL'], SETTINGS['GMAIL_PASSWORD'])
    s.sendmail(
        SETTINGS['GMAIL_EMAIL'],
        [SETTINGS['KINDLE_EMAIL']],
        m.as_string())
    s.quit()
