import smtplib

def send_mail(email, message):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("python.coinbit2023@gmail.com", "dtcx ojkr zuvv yvpd")
    body = "Please keep this secure. If lost, it cannot be recovered." + '\n\n\n' + message
    s.sendmail("python.coinbit2023@gmail.com",email, body)
    s.quit()