# this script follows a tutorial at
# http://www.discoversdk.com/blog/getting-started-with-flask?utm_medium=blog&utm_campaign=aaron&utm_source=quora
# on creating a basic web app with flask

# importing libraries
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

# here we are creating an instance of the flask class and
# pass the name of the current module to its constructor
app = Flask(__name__)

# here we are configuring a resource (our sql database)
#### SIDEQUEST ALERT ####
# I didn't know what a URI was so looked it up, but the answer
# I got made me think this should be labeled a url and not uri
# I mean the database is a resource and it is implied that you are using http to access it right?
# here is what i found:
#
# The terms “URI” and “URL” are often used interchangeably, but they are not exactly the same.
# A URI is an identifier of a specific resource. Like a page, or book, or a document.
# A URL is special type of identifier that also tells you how to access it, such as
# HTTPs, FTP, etc.—like https://www.google.com.
# If the protocol (https, ftp, etc.) is either present or implied for a domain,
# you should call it a URL—even though it’s also a URI.
# see what I mean? Anyways...
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://test.db'


# this function will define our home page, but we need a way to know this is our home page
# before we write our home page function, we are going to wrap this function with the
# decorator fuction @app.route(). The string inside the parens shows the path of the page
# since we are doing our home page for our site, the string is simply "/"
@app.route("/")
# next we have a straight up python function that returns a super cheesy string
def home():
    return render_template("index.html")

# add debugging that will show up on our page if something goes wrong
if __name__ == "__main__":
    app.run(debug=True)
