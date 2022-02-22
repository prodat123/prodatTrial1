import random
import mysql.connector
from Person import Person
from News import News
from flask import Flask, redirect, url_for, render_template, request

import string
# import cv2
# from pyzbar.pyzbar import decode
import datetime

import os
from werkzeug.utils import secure_filename
import uuid as uuid

camOn = False

studentIndex = 0

personNameSelect = ""
points = 0
newPeople = []
people = []

CurrentAccount = open("CurrentAccount.txt", "r")

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="password123",
    database="News",
)

news = """CREATE TABLE News (
    ID VARCHAR(250),
    Publisher VARCHAR(250),
    PublishedDate VARCHAR(250),
    NewsLink VARCHAR(250),
    CoverImage VARCHAR(250),
    Heading VARCHAR(250),
    Content VARCHAR(250),
    Likes INTEGER(255),
    Channel VARCHAR(250))
    """


c = mydb.cursor()


#c.execute(news)

def addNews(id, publisher, date, link, image, heading, content, channel):
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="password123",
        database="News",
    )
    c = mydb.cursor()
    with mydb:
        insertNews = """INSERT INTO News (ID, Publisher, PublishedDate, NewsLink, CoverImage, Heading, Content, Likes, Channel) VALUES (%s, %s, %s, %s, %s, %s, %s, 0, %s)"""
        record = (id, publisher, date, link, image, heading, content, channel)
        c.execute(insertNews, record)
        mydb.commit()
        print("Record inserted successfully into News Table")


# people = """CREATE TABLE people1 (
#                     ID VARCHAR(255),
#                     Name VARCHAR(255),
#                     CreditPoints VARCHAR(255),
#                     DetentionCounter VARCHAR(255),
#                     Role VARCHAR(255),
#                     Username VARCHAR(255),
#                     Password VARCHAR(255),
#                     Image VARCHAR(255),
#                     Channel VARCHAR(255)
#                     )"""
#
# c.execute(people)

def insert_person(ID, Name, CreditPoints, DetentionCounter, Role, Username, Password, Image, Channel):
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="password123",
        database="People",
    )

    c = mydb.cursor()

    with mydb:
        insertPerson = """INSERT INTO people1 (ID, Name, CreditPoints, DetentionCounter, Role, Username, Password, Image, Channel) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        record = (ID, Name, CreditPoints, DetentionCounter, Role, Username, Password, Image, Channel)
        c.execute(insertPerson, record)
        mydb.commit()


def get_person_user(username, password):
    get_person_user.Username = ""
    get_person_user.success = False
    get_person_user.passwordError = False
    get_person_user.usernameError = False
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="password123",
        database="People",
    )
    c = mydb.cursor()

    with mydb:

        query = "SELECT Password, COUNT(*) FROM people1 WHERE Username = %s GROUP BY Username"

        c.execute(query, (username,))
        results = c.fetchall()
        print(results)
        row_count = c.rowcount
        print("number of affected rows: {}".format(row_count))
        if row_count == 0:
            print("This username does not exist")
            get_person_user.success = False
            get_person_user.usernameError = True
        else:

            if password == results[0][0]:
                print("Successful login")
                get_person_user.success = True
                account = "SELECT * FROM people1 WHERE Password = %s"
                c.execute(account, (password,))
                get_person_user.SignedInAccount = c.fetchall()
                print(get_person_user.SignedInAccount)
                get_person_user.Username = get_person_user.SignedInAccount[0][5]
                CurrentAccount = open("CurrentAccount.txt", "w")
                CurrentAccount.write("%s\r\n" % get_person_user.Username)
                CurrentAccount.close()
            else:
                get_person_user.success = False
                get_person_user.passwordError = True
                print("This is the wrong password")


def get_account_detail(username):
    get_account_detail.Account = []
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="password123",
        database="People",
    )
    c = mydb.cursor()
    with mydb:
        query = "SELECT * FROM people1 WHERE Username = %s"
        c.execute(query, (username,))

        get_account_detail.Account = c.fetchall()
        print(get_account_detail.Account)


student1 = Person('151560', 'Maxwell', 0, 0, 'student', 'maxwell', '267387', '', '')
student2 = Person('151706', 'Miley', 0, 0, 'student', 'miley', '090409', '', '')
teacher1 = Person('11520133', 'Benny', 0, 0, 'teacher', 'benny', '101010', '', '')


# insert_person("People", student1.ID, student1.Name, student1.CreditPoints, student1.DetentionCounter, student1.Role, student1.Username, student1.Password, student1.Image)
# insert_person(student2.ID, student2.Name, student2.CreditPoints, student2.DetentionCounter, student2.Role, student2.Username, student2.Password, student2.Image, student2.Channel)



print(people)

used_codes = []
#


app = Flask(__name__)


@app.route("/MakeNews", methods=['GET', 'POST'])
def MakeNews():
    if request.method == 'GET':
        return render_template("MakeNewNews.html")
    if request.method == 'POST':
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="password123",
            database="News",
        )
        c = mydb.cursor()
        x = datetime.datetime.now()
        DatePublished = x.strftime("%x")
        # Image = request.form.getlist('Image')
        Content = request.form.get('Content')
        Heading = request.form.get('Heading')
        account = open("CurrentAccount.txt", "r")
        Publisher = account.read()
        S = 6
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="password123",
            database="People",
        )
        c = mydb.cursor()
        ChannelQuery = "SELECT Channel FROM people1 WHERE Username = %s"
        PublisherString = Publisher.replace('\n', '')
        c.execute(ChannelQuery, (PublisherString, ))
        Channel = c.fetchall()
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="password123",
            database="News",
        )
        c = mydb.cursor()
        ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
        query = "SELECT ID, COUNT(*) FROM News WHERE ID = %s GROUP BY ID"

        c.execute(query, (ID,))
        results = c.fetchall()
        print(results)
        row_count = c.rowcount
        if row_count == 0:
            newNews = News(ID, Publisher, DatePublished, "", "", Heading, Content, Channel[0][0])
            addNews(newNews.id, newNews.publisher, newNews.publishedDate, newNews.newsLink, newNews.coverImage, newNews.heading, newNews.content, newNews.channel)
            likesList = """CREATE TABLE Likes""" + str(ID) + """ (
                            Liked VARCHAR(255))"""

            c.execute(likesList)
            print(ID)

            return redirect(url_for("NewsPage"))


DatePublished = ""
Content = ""
Link = ""

id = []


@app.route("/Home")
@app.route("/")
def HomePage():
    loginSuccess = ""
    channelName = ""
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="password123",
        database="People",
    )
    c = mydb.cursor()
    with open("CurrentAccount.txt", "r") as file:
        username = file.read().replace('\n', '')
        print(username)
        checkChannel = "SELECT Channel, COUNT(*) FROM people1 WHERE Username = %s GROUP BY Channel"
        c.execute(checkChannel, (username, ))
        channel = c.fetchall()
        print(channel)
        row_count = c.rowcount
        if username != " ":
            loginSuccess = "True"
            signedOut = "False"

            if row_count == 0:
                channelName = " "
                joinedChannel = False
            else:
                channelName = channel[0][0]
                HomePage.channel = channel[0][0]
                joinedChannel = True

        else:
            print("logged out")
            signedOut = "True"

    return render_template("HomePage.html", username=username[0].capitalize(), loginSuccess=loginSuccess,
                           signedOut=signedOut, roomName=channelName, joinedChannel=joinedChannel)


@app.route("/NewsPage/", methods=['POST', 'GET'])
def NewsPage():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="password123",
        database="People",
    )
    c = mydb.cursor()
    f = open("CurrentAccount.txt", "r")
    username = f.read().replace('\n', '')

    usernameChannel = "SELECT Channel FROM people1 WHERE Username = %s"
    c.execute(usernameChannel, (username, ))
    channel = c.fetchall()
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="password123",
        database="News",
    )
    c = mydb.cursor()
    getNewsQuery = "SELECT * FROM News WHERE Channel = %s"
    c.execute(getNewsQuery, (channel[0][0], ))
    news = c.fetchall()
    print(news)
    c.execute("SELECT ID FROM News WHERE Channel = %s", (channel[0][0], ))
    ID = c.fetchall()
    c.execute("SELECT PublishedDate FROM News WHERE Channel = %s", (channel[0][0], ))
    NewsDates = c.fetchall()
    c.execute("SELECT Publisher FROM News WHERE Channel = %s", (channel[0][0], ))
    Publisher = c.fetchall()
    c.execute("SELECT NewsLink FROM News WHERE Channel = %s", (channel[0][0], ))
    NewsLinks = c.fetchall()
    c.execute("SELECT CoverImage FROM News WHERE Channel = %s", (channel[0][0], ))
    CoverImages = c.fetchall()
    c.execute("SELECT Heading FROM News WHERE Channel = %s", (channel[0][0],))
    Heading = c.fetchall()
    c.execute("SELECT Content FROM News WHERE Channel = %s", (channel[0][0], ))
    Content = c.fetchall()
    c.execute("SELECT Likes FROM News WHERE Channel = %s", (channel[0][0], ))
    Likes = c.fetchall()

    if request.method == 'GET':

        return render_template("NewsPage.html", news=len(news), id=ID, publisher=Publisher, newsDate=NewsDates, newsLink=NewsLinks,
                               newsImage=CoverImages, heading = Heading, content=Content, likes=Likes)
    if request.method == 'POST':

        for i in range(len(news)):

            currentAccount = open("CurrentAccount.txt", "r")

            currentLoggedInAcc = currentAccount.read()

            user = str(currentLoggedInAcc)

            likeButton = "like" + str(i)
            if request.form['NewsButton'] == likeButton:
                CheckPerson = "SELECT Liked, COUNT(*) FROM Likes" +news[i][0] + " WHERE Liked = %s GROUP BY Liked"
                print(news[i][0])
                c.execute(CheckPerson, (user,))
                results = c.fetchall()
                row_count = c.rowcount
                print(row_count)
                if row_count == 0:
                    AddLike = "INSERT INTO Likes" + news[i][0] + " (Liked) VALUES (%s)"
                    c.execute(AddLike, (user,))
                    likesNum = "SELECT count(*) FROM Likes"+news[i][0]
                    c.execute(likesNum)
                    likes = c.fetchall()
                    updateLikes = likes[0][0]
                    UpdateLikes = "UPDATE News SET Likes = %s WHERE ID = %s"

                    update = (updateLikes, news[i][0])

                    c.execute(UpdateLikes, update)
                    mydb.commit()
                else:

                    deleteUsername = "DELETE FROM Likes"+news[i][0]+" WHERE Liked = %s"
                    c.execute(deleteUsername, (user,))
                    mydb.commit()
                    likesNum = "SELECT count(*) FROM Likes" + news[i][0]
                    c.execute(likesNum)
                    likes = c.fetchall()
                    updateLikes = likes[0][0]
                    UpdateLikes = "UPDATE News SET Likes = %s WHERE ID = %s"
                    update = (updateLikes, news[i][0])

                    c.execute(UpdateLikes, update)
                    mydb.commit()

                print("success")

                c.execute("SELECT Likes FROM News")
                Likes = c.fetchall()

                return render_template("NewsPage.html", news=len(news), id=ID, publisher=Publisher, newsDate=NewsDates, newsLink=NewsLinks,
                                       newsImage=CoverImages, heading=Heading, content=Content, likes=Likes)

            if request.form['NewsButton'] == str(i):
                print("registered")
                newsID = request.form.getlist('NewsButton')
                print(newsID)
                print("Second stage working")
                sql_select_query = "SELECT * FROM News WHERE ID = %s"
                c.execute(sql_select_query, (ID[i][0],))

                print("success")
                newsInfo = c.fetchall()
                print(newsInfo[0])
                NewsPage.newsInfo = newsInfo
                return redirect(url_for("Page"))
                # return render_template("NewsPage.html", news=len(news), id=ID, newsDate=NewsDates, newsLink=NewsLinks,
                #                    newsImage=CoverImages, content=Content, likes=Likes)


@app.route("/Page/", methods=['POST', 'GET'])
def Page():
    newsInfo = NewsPage.newsInfo

    return render_template("News.html", news=newsInfo, newsLength=len(newsInfo))


app.config["IMAGE_UPLOADS"] = 'C:/Users/maxwe/PycharmProjects/Project1/static/ProfileImage'


@app.route("/SignUpPage", methods=['GET', 'POST'])
def SignUpPage():
    if request.method == 'GET':
        return render_template("SignUpPage.html")
    if request.method == 'POST':
        id = request.form.getlist('ID')
        name = request.form.getlist('name')
        username = request.form.getlist('uname')
        password = request.form.getlist('psw')
        occupation = request.form.getlist('occupation')
        # profileImage = request.files['ProfileImage']
        # profileImage.save(os.path.join(app.config["IMAGE_UPLOADS"], profileImage.filename))
        # print("Image saved")
        # print(profileImage)
        insert_person(id[0], name[0], 0, 0, occupation[0], username[0], password[0], "", "")
        return render_template("HomePage.html")


@app.route("/SignInPage", methods=['POST'])
def SignInPage():
    if request.method == 'POST':
        username = request.form.getlist('Username')
        password = request.form.getlist('Password')
        get_person_user(username[0], password[0])
        if get_person_user.success:

            readAccount = open("CurrentAccount.txt", "r")

            username = readAccount.read()
            print(username)
            return redirect(url_for('HomePage'))
            #return render_template("HomePage.html", loginSuccess="True", username=username[0].capitalize())

        else:
            return render_template("HomePage.html", loginSuccess="False", usernameError=get_person_user.usernameError,
                                   psdError=get_person_user.passwordError)



@app.route("/Home", methods=['POST'])
def signOut():
    if request.method == 'POST':
        SignOut = open("CurrentAccount.txt", "w")
        SignOut.write(" ")
        SignOut.close()
        print("clicked")

        return redirect(url_for('HomePage'))


mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="password123",
    database="Servers",
)
c = mydb.cursor()
channels = """CREATE TABLE servers(
                    ChannelID VARCHAR(255)
                    )"""
#c.execute(channels)


@app.route("/MakeChannel", methods=['GET', 'POST'])
def MakeChannel():
    if request.method == 'GET':
        return redirect(url_for('HomePage'))
    if request.method == 'POST':
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="password123",
            database="People",
        )
        c = mydb.cursor()
        S = 6
        ChannelName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
        with open("CurrentAccount.txt", "r") as f:
            accountRead = f.read().replace('\n', '')
            CheckUserOccupation = "SELECT Role FROM people1 WHERE Username = %s"
            c.execute(CheckUserOccupation, (accountRead, ))
            f.close()
            userOccupation = c.fetchall()
            print(userOccupation[0][0])
            if userOccupation[0][0] == "teacher":
                mydb = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    passwd="password123",
                    database="Servers",
                )

                c = mydb.cursor()

                channelInsert = "INSERT INTO servers (ChannelID) VALUES (%s)"

                c.execute(channelInsert, (ChannelName,))

                mydb.commit()
                print(ChannelName)
                MakeChannel.CorrectChannel = ChannelName
                mydb = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    passwd="password123",
                    database="People",
                )

                peopleCursor = mydb.cursor()
                sql = "UPDATE people1 SET Channel = %s WHERE Username = %s"
                update = (ChannelName, accountRead)
                peopleCursor.execute(sql, update)
                mydb.commit()
                return redirect(url_for('HomePage'))

               # return render_template("HomePage.html", CreateChannel="True", RoomName=correctRoomName)

            else:
                return redirect(url_for('MakeChannel'))
                #return render_template("HomePage.html", CreateChannel="False")





@app.route("/JoinChannel", methods=['GET', 'POST'])
def JoinChannel():
    if request.method == 'POST':
        ChannelName = request.form.getlist('Channel')
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="password123",
            database="Servers",
        )
        c = mydb.cursor()
        query = "SELECT ChannelID, COUNT(*) FROM servers WHERE ChannelID = %s GROUP BY ChannelID"

        c.execute(query, (ChannelName[0],))
        results = c.fetchall()
        print(results)
        row_count = c.rowcount

        if row_count == 0:
            print("This channel does not exist")
            ChannelExists = False
        else:
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                passwd="password123",
                database="People",
            )
            c = mydb.cursor()
            sql = "UPDATE people1 SET Channel = %s WHERE Username = %s"

            readAccount = open("CurrentAccount.txt", "r")

            username = readAccount.read()
            accountRead = username.replace('\n', '')
            val = (ChannelName[0], accountRead)
            c.execute(sql, val)
            mydb.commit()
            ChannelExists = True
            return redirect(url_for('HomePage'))

    return render_template("HomePage.html", channelExists=ChannelExists)

@app.route("/People List")
def PeopleList():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="password123",
        database="People",
    )
    c = mydb.cursor()
    query = "SELECT Username FROM people1 WHERE Channel = %s"
    c.execute(query, (HomePage.channel, ))
    usernames = c.fetchall()
    print(usernames)
    return render_template("PeopleList.html", usernames=usernames, length=len(usernames))



@app.route("/AccountPage")
def AccountPage():
    AccountRead = open("CurrentAccount.txt", "r")
    AccountUsername = AccountRead.read().replace("\n", "")
    AccountRead.close()
    print(AccountUsername)
    get_account_detail(AccountUsername)
    print(get_account_detail.Account)

    return render_template("AccountPage.html", account=get_account_detail.Account[0],
                           length=len(get_account_detail.Account[0]))

@app.route("/Search")

def Search():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="password123",
        database="People",
    )
    c = mydb.cursor()
    query = "SELECT Username FROM people1"
    c.execute(query)
    peopleResult = c.fetchall()
    return render_template("Search.html", people=peopleResult)


if __name__ == "__main__":
    app.run()
