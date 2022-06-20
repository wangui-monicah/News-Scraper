
from http import server
import requests # http requests

from bs4 import BeautifulSoup #web scraping

import smtplib #send the mail

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime #system date and time maipulation


now = datetime.datetime.now() #extrats current datetime which is the system's datetime
content = '' #email content placeholder

#extracting Hacker News Stories

def extract_news(url):
    print("Extracting Hacker News Stories...")
    cnt = ''
    cnt +=("<b>HN Top Stories:</b>\n" + "<br>" + "-"*50 + "<br>")#written in bold; line breaks; 50 stars
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content,'html.parser')

    for i, tag in enumerate(soup.find_all('td', attrs={'class':'title','valign':''})):#td refers to the actual cell in the 
        cnt += ((str(i+1) + ' :: ' + tag.text + "\n" + '<br>') if tag.text != 'More' else '')
        #print(tag.prettify) #find all('span'.attrs = {'class' : 'sitestr'}))
    return(cnt)

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>------<br>')
content += ('<br><br>End of Message')

#Sending email
print('Composing Email.......')

# ************ EMAIL AUTHENTICATION *******************
#update your email details
SERVER = 'smtp.gmail.com' #'your smtp server'
PORT = 587 #port number
FROM = 'writeyours@gmail.com' #your from email ID
TO = 'writeyours@gmail.com' #your to email Ids; could be a list
PASS = 'yourpassword123' #your email ID's password

# fp = open(file_name, 'rb')
# Create a text/plain message
#msg = MIMEText('')
msg = MIMEMultipart()

#msg.add_header('Content-Disposition', 'attachment', filename = 'empty.txt')
msg['Subject'] = 'Your Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
#fp.close()

print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)
#server = smtplib.SMTP SSL('smtp.gmail.com' 465)
server.set_debuglevel(1)#this one is for if you want to see error messages or not.. 0--> no error message; 1 ---> error message will get diplayed
server.ehlo()
server.starttls()#sets up a secure location
#server.ehlo
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email sent....')

server.quit()
