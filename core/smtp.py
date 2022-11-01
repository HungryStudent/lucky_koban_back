import smtplib

user = "n1kitos1337@yandex.ru"
passwd = "bqemztyqhywbdgca"
server = "smtp.yandex.ru"
port = 587
subject = "Lucky Koban - Подтверждение почты "
charset = 'Content-Type: text/plain; charset=utf-8'
mime = 'MIME-Version: 1.0'
text = "Здравствуйте, Ваш код для подтверждения почты - {code}. Крутите кейсы и получайте крутые игры"


def send_code(code, email):
    body = "\r\n".join((f"From: {user}", f"To: {email}",
                        f"Subject: {subject}", mime, charset, "", text.format(code=code)))

    try:
        smtp = smtplib.SMTP(server, port)
        smtp.starttls()
        smtp.ehlo()
        smtp.login(user, passwd)
        smtp.sendmail(user, email, body.encode('utf-8'))
    except smtplib.SMTPException as err:
        print('Что - то пошло не так...')
        raise err
    finally:
        smtp.quit()
