# this script follows a tutorial at
# http://www.discoversdk.com/blog/getting-started-with-flask?utm_medium=blog&utm_campaign=aaron&utm_source=quora
# on creating a basic web app with flask

# importing libraries
import flask

# here we are creating an instance of the flask class and
# pass the name of the current module to its constructor
app = flask.Flask(__name__)


# next we have a straight up python function that returns a super cheesy string
def home():
    return "Welcome to my home page that I made available with the help of flask."