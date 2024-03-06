print('start this')

from flask import Flask, render_template, request, redirect, url_for
from sms import *
import random
import datetime
import pytz
import webbrowser

users = {}
f = open('/home/pi/Desktop/sms_flask/contacts.txt', 'r').read().strip('\n').split('\n')
for line in f:
    line = line.split(';')
    users[line[0]] = line[1]

app = Flask(__name__, template_folder='sms_flask')

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        user = request.form.get('user')
        print(user)
        return redirect(f'/user/{user}')
    else:
        return render_template('home.html', users=users)

@app.route('/user/<user>', methods=['GET', 'POST'])
def user(user):
    prev_texts=[]
    try:
        f = open(f'/home/pi/Desktop/sms_flask/users/{user}.txt', 'r').read().strip('\n').split('\n')
        for line in f:
            prev_texts.append(line)
    except:
        pass
    start_up()
    if request.method == 'POST':
        text = request.form['message']
        if not text:
            text = 'place_holder'
        print(f'trying to send "{text}" to {user}')
        send_text(user, text)
        current = datetime.datetime.now(pytz.timezone('Australia/Sydney'))
        date_info = f'{current.day}/{current.month}/{current.year} {current.hour}:{current.minute}'
        f = open(f'/home/pi/Desktop/sms_flask/users/{user}.txt', 'a')
        f.writelines([f'\n{date_info} You: {text}'])
        f.close()
    all_texts = read_all()
    while not all_texts:
        start_up()
        all_texts = read_all()
    if all_texts:
        texts = all_texts.split('\n')
        for text_n in range(len(texts)):
            if '+CMGL: ' in texts[text_n]:
                info = texts[text_n][7:]
                info = info.split(',')
                description = f'{info[4][1:]} {info[5][:-5]} {users.get(info[2][1:-1], "Unknown")} ({info[2]})'
                f = open(f'/home/pi/Desktop/sms_flask/users/{info[2][1:-1]}.txt', 'a')
                f.writelines([f'{description}: {texts[text_n+1]}'])
                f.close()
                if user in texts[text_n]:
                    prev_texts.append(f'{description}: {texts[text_n+1]}')
        send_at('AT+CMGD=1,4', '', 5)
    power_off(6)
    return render_template('user.html', prev_texts=prev_texts, user=user, name=users[user])

@app.route('/unread')
def unread():
    texts=[]
    start_up()
    new_texts = read_unread()
    while not new_texts:
        start_up()
        new_texts = read_unread()
    power_off(6)
    if new_texts:
        new_texts = new_texts.split('\n')
        for text_n in range(len(new_texts)):
            if '+CMGL: ' in new_texts[text_n]:
                try:
                    info = new_texts[text_n][7:]
                    info = info.split(',')
                    description = f'{info[4][1:]} {info[5][:-5]} {users.get(info[2][1:-1], "Unknown")} ({info[2]})'
                    texts.append(f'{description}: {new_texts[text_n+1]}')
                    f = open(f'/home/pi/Desktop/sms_flask/users/{info[2][1:-1]}.txt', 'a')
                    f.writelines([f'{description}: {texts[text_n+1]}'])
                    f.close()
                except:
                    break
        send_at('AT+CMGD=1,4', '', 5)
    return render_template('unread.html', texts=texts)

@app.route('/every')
def every_text():
    texts=[]
    start_up()
    all_texts = read_all()
    while not all_texts:
        start_up()
        all_texts = read_all()
    power_off(6)
    if all_texts:
        all_texts = all_texts.split('\n')
        for text_n in range(len(all_texts)):
            if '+CMGL: ' in all_texts[text_n]:
                try:
                    info = all_texts[text_n][7:]
                    info = info.split(',')
                    print(info[2][1:-1])
                    description = f'{info[4][1:]} {info[5][:-5]} {users.get(info[2][1:-1], "Unknown")} ({info[2]})'
                    texts.append(f'{description}: {all_texts[text_n+1]}')
                except:
                    break
    return render_template('unread.html', texts=texts)

if __name__ == '__main__':
    port = random.randint(0, 9999)
    webbrowser.open(f'http://127.0.0.1:{port}')
    app.run(debug=True, port=port)
    
    print('help')