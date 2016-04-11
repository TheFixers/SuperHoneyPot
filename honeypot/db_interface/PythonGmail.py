import smtplib

# Specifying the from and to addresses

fromaddr = 'honeypot4260@gmail.com'
toaddrs  = 'svoluch@gmail.com'

# Writing the message (this message will appear in the email)

msg = 'Failed a connection to MongoDB server'

# Gmail Login

username = 'honeypot4260@gmail.com'
password = 'Teddybearfood'

# Sending the mail  

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()