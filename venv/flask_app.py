# this script follows a tutorial at
# http://www.discoversdk.com/blog/getting-started-with-flask?utm_medium=blog&utm_campaign=aaron&utm_source=quora
# on creating a basic web app with flask

# importing libraries
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# here we are creating an instance of the flask class and
# pass the name of the current module to its constructor
app = Flask(__name__)

# here we are configuring a resource (our sql database)
# we are telling our app where to locate our database
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# next we will initialize our database
db = SQLAlchemy(app)

# next we are going to create our database model
# we have three columns in this table,
# one for id,
# one for the content of the to-do task,
# and one that records the date the task was created
# the model is stored as a class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # next we create a function that returns a string (the task id) every
    # time something is entered in the table
    def __repr__(self):
        return '<Task %r>' % self.id



# this function will define our home page, but we need a way to know this is our home page
# before we write our home page function, we are going to wrap this function with the
# decorator fuction @app.route(). The string inside the parens shows the path of the page
# since we are doing our home page for our site, the string is simply "/"
@app.route("/", methods=['POST', 'GET'])
# next we have a straight up python function that returns a super cheesy string
def index():
    # if the request is a content post we want to assign the content to a
    # variable then pass that to a new task
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        # then we try to add our new task to the list of things we want our db to do.
        # then we commit the tasks we wanted added
        # then we redirect to our page
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There were issues adding your task"
    else:
        # or else just stay on the page after looking up all the tasks by date
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)



# here we are creating a new route for deleting entries
# the wrapper function creates a route that goes to home directory,
# then the delete subdirectory,
# then to a subdirectory that accepts and int argument
# that int argument in the id field of our sql table
# the id is our primary key for the table and serves as a unique
# identifier for the entry we want to delete
@app.route('/delete/<int:id>')
# now we will create our function that actually deletes the variable
def delete(id):
    # this line creates a variable task_to_delete, that is the result of
    # querying the database for the id,
    # if it does not find the id, it results in a 404 error
    task_to_delete = Todo.query.get_or_404(id)
    # now we pass our variable to a try statement where we we will
    # actually delete it from the database,
    # then commit our changes to the database,
    # and finally redirect back to the homepage
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
            return "There was an issue deleting the task, try again later."

# we are creating another page/route that updates a particular
# task (allows the user to edit the string)
# the route wrapper function is pretty much the
# same as the last one, except it also needs the get and post methods
# like our index page so that the edited task will be posted
@app.route('/update/<int:id>', methods=['GET', 'POST'])
# the function itself queries the database for the entry matching the id and assigns that to a variable
# The content value of the variable is then updated to what was in the request form
# then it tries to commit the change to the database
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == "POST":
        task_to_update.content = request.form["content"]

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating your task, please try again later."
    else:
        return render_template("update.html", task=task_to_update)

# add debugging that will show up on our page if something goes wrong
if __name__ == "__main__":
    app.run(debug=True)
