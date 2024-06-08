import smtplib
import email
import email.mime.application

try:
    import email.mime.Multipart
except Exception as exc:
    import email.mime.multipart
import getpass

BLANK_SETTINGS = {
    "from_email": None,
    "to_email": None,
    "smtp_password": None,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
}


def send_file(filename, contents=None, from_email=None, to_email=None, settings=None):
    settings = settings or {}
    cleanups = []
    # http://stackoverflow.com/a/8243031/979255
    if from_email is None:
        if "from_email" not in settings:
            raise ValueError("No from_email supplied.")
        from_email = settings["from_email"]

    if to_email is None:
        if "to_email" not in settings:
            raise ValueError("No to_email supplied.")
        to_email = settings["to_email"]

    try:
        m = email.mime.Multipart.MIMEMultipart()
    except Exception as exc:
        m = email.mime.multipart.MIMEMultipart()
    m["Subject"] = ""
    m["From"] = from_email
    m["To"] = to_email

    if contents:
        att = email.mime.application.MIMEApplication(
            contents.read(), _subtype="x-mobipocket-ebook"
        )
    elif isinstance(filename, str):
        fp = open(filename, "rb")
        att = email.mime.application.MIMEApplication(
            fp.read(), _subtype="x-mobipocket-ebook"
        )
        fp.close()
    else:
        raise ValueError("Must specify filename, or filename and contents")
    att.add_header("Content-Disposition", "attachment", filename=filename)
    m.attach(att)

    cleanups.append(filename)

    while True:
        try:
            if ("smtp_password" not in settings) or (
                settings["smtp_password"] in [None, ""]
            ):
                passwd = getpass.getpass("SMTP password for {}: ".format(from_email))
            else:
                passwd = settings["smtp_password"]

            # pretty_print([CYAN], "Beginning send...")
            s = smtplib.SMTP(
                settings.get("smtp_server", "smtp.gmail.com"),
                settings.get("smtp_port", 587),
            )
            s.starttls()
            s.login(from_email, passwd)
            s.sendmail(from_email, [to_email], m.as_string())
            s.quit()
            # pretty_print([CYAN], "Send complete.")
            return cleanups
        except Exception as e:
            print(e)
