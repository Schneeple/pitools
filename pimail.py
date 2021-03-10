import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class SMTP(object):
    def __init__(self, body="", to=[], subject='Automated Python Email', link="", cc="", bcc=""):
        """
        Make sure your server is setup with SMTP. Change your email/password also update server address and port in the file itself

        """

        self.message = EmailMessage()
        self.contacts = {}
        self.to = to
        self.link = link
        self.body = body
        self.bcc = bcc
        self.cc = cc
        self.ServerAddress = 'Enter Your SMTP server address here'  # e.g. 'UKGWSMTPext.maps.google.com'
        self.ServerPort = 587  # Change if needed
        self.Email = 'ENTER YOUR EMAIL HERE'  # e.g. yourusername@google.com
        self.Password = 'ENTER YOUR PASSWORD HERE'  # e.g. ngfw823@GH@Gh289la
        self.subject = subject

    def get_contacts(self, names):
        self.to = []
        for i in names:
            try:
                self.to.append(self.contacts[i])
            except:
                print(i + ' is not in the address book. Please update the contact list.')

    def create_email(self):
        # Building the mail content
        self.message['From'] = self.Email
        self.message['To'] = self.to
        self.message['Subject'] = self.subject
        self.message['Cc'] = self.cc
        self.message['Bcc'] = self.bcc
        self.message.set_content(self.subject)
        self.message.add_alternative("""\
        <!DOCTYPE html>
        <html>
            <body>
                {bodi}
                {link}
            </body>
        </html>
        """.format(link=self.link, bodi=self.body), subtype='html')

    def send(self, print_status=True, file=None):
        self.create_email()
        if type(file) != type(None):
            # Wasn't working
            attachment = open(file, 'rb')
            obj = MIMEBase('application', 'octet-stream')
            obj.set_payload((attachment).read())
            encoders.encode_base64(obj)
            obj.add_header('Content-Disposition', "attachment; filename= " + file)
            self.message.attach(obj)
            # self.message = self.message.as_string()

        with smtplib.SMTP(self.ServerAddress, self.ServerPort) as mail:
            mail.ehlo()
            mail.starttls()
            mail.login(self.Email, self.Password)
            mail.send_message(self.message)
            self.message = EmailMessage()
        if print_status:
            print('Email sent to: \n')
            for i in self.to:
                print(i)
            print('CC to: \n')
            for j in self.cc:
                print(j)
            print('Bcc to: \n')
            for k in self.bcc:
                print(k)


if __name__ == '__main__':
    SMTP(body=' TEST ', to=[self.Email], bcc=[self.Email])  # .send()
