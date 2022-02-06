# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField, DateField, DateTimeField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange
from wtforms.fields import DateTimeLocalField
from datetime import date, datetime

import analysis
TRIG1=7
ECHO1=11
TRIG2=15
ECHO2=16
TRIG3=23
ECHO3=24
TRIG4=35
ECHO4=36
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'

# Flask-Bootstrap requires this line
Bootstrap(app)

# the name of the database; add path if necessary
db_name = 'stock_db.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and data type
class Barrel(db.Model):
    __tablename__ = 'barrels'
    id = db.Column(db.Integer, primary_key=True)
    itemCode = db.Column(db.String)
    currentLevel = db.Column(db.Float)
    remainStock = db.Column(db.Float)
    remainStockTrigger = db.Column(db.Float)
    dateExpiry = db.Column(db.String)
    dateCreated = db.Column(db.String)

    def __init__(self, itemCode, currentLevel, remainStock, remainStockTrigger, dateExpiry, dateCreated):
        self.itemCode = itemCode
        self.currentLevel = currentLevel
        self.remainStock = remainStock
        self.remainStockTrigger = remainStockTrigger
        self.dateExpiry = dateExpiry
        self.dateCreated = dateCreated

# small form
class DeleteForm(FlaskForm):
    id_field = HiddenField()
    purpose = HiddenField()
    submit = SubmitField('Delete This Item')
# +++++++++++++++++++++++
# forms with Flask-WTF

# form for add_record and edit_or_delete
# each field includes validation requirements and messages
class AddRecord(FlaskForm):
    # id used only by update/edit
    id_field = HiddenField()
    itemCode = StringField('Barrel name', [ InputRequired(),
        Length(min=3, max=25, message="Invalid barrel name length")
        ])
    currentLevel = HiddenField()
    remainStock = FloatField('Quantity in stock', [ InputRequired(),
        NumberRange(min=1.0, max=99, message="Invalid number")
        ])
    remainStockTrigger = FloatField('Remaining stock trigger', [ InputRequired(),
        NumberRange(min=1.0, max=99, message="Invalid number")
        ])
    dateExpiry = DateField('Expiry date', format='%Y-%m-%d' , validators=[InputRequired(),])

    # updated - date - handled in the route
    dateCreated = HiddenField()
    submit = SubmitField('Add/Update Record')

# +++++++++++++++++++++++
# get local date - does not account for time zone
# note: date was imported at top of script
def stringdate():
    today = date.today()
    date_list = str(today).split('-')
    # build string in format 01-01-2000
    date_string = date_list[1] + "-" + date_list[2] + "-" + date_list[0]
    return today

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def index():
    # get a list of unique values in the style column
    sensor1 = analysis.analyseMeasure(TRIG1,ECHO1) 
    sensor2 = analysis.analyseMeasure(TRIG2,ECHO2) 
    sensor3 = analysis.analyseMeasure(TRIG3,ECHO3) 
    sensor4 = analysis.analyseMeasure(TRIG4,ECHO4) 
    return render_template('index.html', sensor1=sensor1,sensor2=sensor2,sensor3=sensor3,sensor4=sensor4)

@app.route('/inventory')
def inventory():
    barrels = Barrel.query.order_by(Barrel.itemCode).all()
    return render_template('list.html', barrels=barrels)

# add a new item to the database
@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    form1 = AddRecord()
    if form1.validate_on_submit():
        itemCode = request.form['itemCode']
        currentLevel = 0
        remainStock = request.form['remainStock']
        remainStockTrigger = request.form['remainStockTrigger']
        dateExpiry = request.form['dateExpiry']
        # get today's date from function, above all the routes
        dateCreated = stringdate()
        # the data to be inserted into Item model - the table, items
        record = Barrel(itemCode, currentLevel, remainStock, remainStockTrigger, dateExpiry, dateCreated) 
        # Flask-SQLAlchemy magic adds record to database
        db.session.add(record)
        db.session.commit()
        # create a message to send to the template
        message = f"The data for barrel {itemCode} has been submitted."
        return render_template('add_record.html', message=message)
    else:
        # show validaton errors
        # see https://pythonprogramming.net/flash-flask-tutorial/
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('add_record.html', form1=form1)

# select a record to edit or delete
@app.route('/select_record/<letters>')
def select_record(letters):
    # alphabetical lists by item name, chunked by letters between _ and _
    # .between() evaluates first letter of a string
    a, b = list(letters)
    barrels = Barrel.query.filter(Barrel.itemCode.between(a, b)).order_by(Barrel.itemCode).all()
    return render_template('select_record.html', barrels=barrels)

# edit or delete - come here from form in /select_record
@app.route('/edit_or_delete', methods=['POST'])
def edit_or_delete():
    id = request.form['id']
    choice = request.form['choice']
    barrel = Barrel.query.filter(Barrel.id == id).first()
    # two forms in this template
    form1 = AddRecord()
    form2 = DeleteForm()
    return render_template('edit_or_delete.html', barrel=barrel, form1=form1, form2=form2, choice=choice)

# result of delete - this function deletes the record
@app.route('/delete_result', methods=['POST'])
def delete_result():
    id = request.form['id_field']
    purpose = request.form['purpose']
    barrel = Barrel.query.filter(Barrel.id == id).first()
    if purpose == 'delete':
        db.session.delete(barrel)
        db.session.commit()
        message = f"The barrel {barrel.itemCode} has been deleted from the database."
        return render_template('result.html', message=message)
    else:
        # this calls an error handler
        abort(405)

# result of edit - this function updates the record
@app.route('/edit_result', methods=['POST'])
def edit_result():
    id = request.form['id_field']
    # call up the record from the database
    barrel = Barrel.query.filter(Barrel.id == id).first()
    # update all values
    barrel.itemCode = request.form['itemCode']
    barrel.remainStock = request.form['remainStock']
    barrel.remainStockTrigger = request.form['remainStockTrigger']
    barrel.dateExpiry = request.form['dateExpiry']
    # get today's date from function, above all the routes
    barrel.dateCreated = stringdate()

    form1 = AddRecord()
    if form1.validate_on_submit():
        # update database record
        db.session.commit()
        # create a message to send to the template
        message = f"The data for barrel {barrel.itemCode} has been updated."
        return render_template('result.html', message=message)
    else:
        # show validaton errors
        barrel.id = id
        # see https://pythonprogramming.net/flash-flask-tutorial/
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('edit_or_delete.html', form1=form1, barrel=barrel, choice='edit')

# +++++++++++++++++++++++
# error routes
# https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/#registering-an-error-handler

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', pagetitle="404 Error - Page Not Found", pageheading="Page not found (Error 404)", error=e), 404

@app.errorhandler(405)
def form_not_posted(e):
    return render_template('error.html', pagetitle="405 Error - Form Not Submitted", pageheading="The form was not submitted (Error 405)", error=e), 405

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', pagetitle="500 Error - Internal Server Error", pageheading="Internal server error (500)", error=e), 500

# +++++++++++++++++++++++
    
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
	app.run(host="0.0.0.0", port = 5000, debug = False)
