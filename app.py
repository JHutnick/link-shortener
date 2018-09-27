from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# brings you to default home page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("home.html")


# retrieves the url, stores it, gets the base 62 value
@app.route('/urlenter', methods=['GET', 'POST'])
def home():
    global characters
    global Base
    global originalURL

    # the characters in base62
    characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # variable holding length of 62
    Base = len(characters)

    # open,execute and close database connection
    conn = sqlite3.connect('urlHolder.db')
    c = conn.cursor()
    originalURL = request.form['longurl']
    # Insert the url into database
    c.execute("INSERT INTO urlInfo (longurl) values (?)", (originalURL,))
    conn.commit()
    url = str(originalURL)
    # select the id where the url name matches
    c.execute("SELECT id FROM urlInfo WHERE longurl=?", (url,))
    # retrieves that db row
    k = c.fetchone()

    for value in k:
        temp = value

    tempvalue = ''
    # retrive the base 62
    while temp != 0:
        tempvalue = (characters[temp % Base]) + tempvalue
        temp = int(temp / Base)
    # set the new link value
    newlink = tempvalue
    # hold to return the new link value
    newurl = 'http://localhost:5000/' + str(newlink)

    return render_template("short.html", newUrl=newurl)


# converts the base 62 back to get the original url link to redirect the user
@app.route('/<newlink>')
def convert(newlink):
    holder = 0
    default = 1

    for value in reversed(newlink):
        holder += default * characters.index(value)
        default *= Base
    assign = holder
    # open and execute database connection
    conn = sqlite3.connect('urlHolder.db')
    c = conn.cursor()
    c.execute("SELECT * FROM urlInfo WHERE id=?", (assign,))

    # grab all and assign index 1, the original url to the redirect
    for data in c.fetchall():
        normalurl = data[1]
        return redirect(normalurl)


if __name__ == "__main__":
    app.run(debug=True)
