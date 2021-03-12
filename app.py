# Use 'ctrl' + '~' to activate the powershell at the bottom of the screen. 

# First thing that we need to do with a flask app is import flask
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Then we need to set up our application
# __name__ refresences the file that we are working in. 
app = Flask(__name__)

# Now we will start to configure our Data base. 
# We start off with the below command with 
# //// - Absolute path. /// - Relative path. then the name of the DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# Initilize the DB
db = SQLAlchemy(app) 
# Then to set up the database do the following. 
# Start an python shell
# Run the command - from app import db
# Then - db.create_all()
# You should see a db file appear. 

# This is the class model of our DB to follow. Pretty simillar to Django. Buiild a class
# Then specifiy what data type if going to be housed in each column.
class Todo(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return '<Task %r>' % self.id


# Then we need to create an index route
# Routes are set up using the app rough decerator. 
# argument is the URL string of the route. 
@app.route('/', methods=['POST', 'GET']) 
# Then we will write a function based view. 
def index():
    if request.method == "POST":
        # This is the logic for what to do when someone submits a form
        # First we will create a variable that will house the data that is in
        # 'content' form. the argument of form is the id of the form we want  
        task_content = request.form['content']
        
        # Next we turn the fill our Todo object with the content that is in the form
        # i.e. we are instantianting the class that we used for our DB with the 
        # content that the user input
        new_task = Todo(content=task_content)

        # Then we need to push the class instance to our DB. 
        try: 
            # Adds the class element to the DB. 
            db.session.add(new_task)
            # Commits the db changes to memory. 
            db.session.commit()
            # Then we want to redirect to the home page. 
            return redirect('/')
        except: 
            return "There was an issue adding your task"
        
    else:
        # In the case that the page isn't handleing a POST request. This is what will happen. 
        # we will fill a variable with all of your DB content. 
        tasks = Todo.query.order_by(Todo.date_created).all()
        # Then we need to pass that variable to our template. 
        return render_template('index.html', tasks=tasks)

# Now we need to add a route for the delete item
# first you need to tell flask what the URL will look like. 
# Included the unique Todo instance id
@app.route('/delete/<int:id>')
# Then we need to write a function to delete the db entry
def delete(id):
    # First create a variable for the task that we want to delete. 
    # we do this by doing a db querey on the id that was passed to the function. 
    # The function get_or_404 will either get the class instnace we need. OR return a 404
    task_to_delete = Todo.query.get_or_404(id)

    try: 
        # Then we will try to delte the line from the DB
        # to do this we will use the command 
        db.session.delete(task_to_delete)

        # then commit the db change. 
        db.session.commit()

        # Then we want to redirect back to our homne page. 
        return redirect('/')

    except: 
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # first we need to figure out which task needs to be updated. 
    # we do that by quering our db
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        # We need to update the DB with the content of the form. 
        # Becuase we already know which task we are working with from the query 
        # above all we need to do is update the attribute. 
        task.content = request.form['content']

        
        try: 
            # Then we rewrite the update into the DB
            db.session.commit()
            return redirect('/')
        except: 
            return "There was an issue updating this task"
        
        
    else:     
        return render_template('update.html', task=task)

# Then we set up the expression that calls the program. 
if __name__ == "__main__":
    app.run(debug=True) # This allows errors to pop on the webpage so we can see them. 


