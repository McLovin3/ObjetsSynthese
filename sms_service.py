import smtplib
gmail_utilisateur = "mathieu.ford@gmail.com"
gmail_app_motPasse = "cjer kafl tecy jkie"
de = gmail_utilisateur
vers = gmail_utilisateur
sujet = "URGENT"


def send_sms(reason, time):
    try:
        corps = reason + " - " + time
        leCourriel = """\
From: %s
To: %s
Subject: %s

%s
""" % (de, vers, sujet, corps)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_utilisateur, gmail_app_motPasse)
        server.sendmail(de, vers, leCourriel.encode('utf-8'))
        server.close()
    except Exception as exception:
        print("Erreur: %s!\n\n" % exception)
