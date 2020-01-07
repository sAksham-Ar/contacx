from flask import Flask, render_template, flash, request, url_for, redirect, session
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField,TextField,IntegerField,RadioField
from wtforms.validators import DataRequired,Length,InputRequired,ValidationError
from MySQLdb import escape_string as thwart
import gc
from flask_wtf.recaptcha import RecaptchaField
import requests, json
app = Flask(__name__)
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Ld3bskUAAAAAELDiylDxZrvtyfyUkBY0o12BElY'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Ld3bskUAAAAAPA3ln7O3YCIX3ToghvcoCxFziA_'

app.config['SECRET_KEY'] = 'sakshu123'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sakshu123'
app.config['MYSQL_DB'] = 'contax'


mysql = MySQL(app)
class Search(FlaskForm):
    Value=StringField("Value",[InputRequired()])
    Category=RadioField("Category",choices=[('Name','Name'),('Number','Number'),('Hall','Hall'),('Department','Department'),('Year','Year')])

@app.route("/")
def hello():
     form=Search()
     return render_template("index.html",form=form)

@app.route("/search/",methods=["POST"])
def search1():
     try:
         form=Search()
         if form.validate_on_submit():
           Value=form.Value.data
           Category=form.Category.data
           con=mysql.connect
           c= con.cursor()
           x=c.execute("SELECT * FROM contacts WHERE %s = '%s'"%(Category,str(Value)))
           if int(x)>0:
                  con.commit()
                  return render_template("result.html",r=c.fetchall())
           else:
                  flash("not found")
                  return redirect(url_for('hello'))

         return render_template("index.html",form=form)

     except Exception as e:
        print(str(e))

def validate_number(form, field):
                  if len(field.data) != 10:
                     raise ValidationError('Number must be of 10 digits')

class RegistrationForm(FlaskForm):
    Name = TextField('Name',validators=[Length(min=4, max=20)])
    Number =TextField('Number',validators=[InputRequired(),validate_number])
    Hall = TextField('Hall',validators=[Length(min=4, max=50)])
    Department = TextField('Department',validators=[Length(min=4, max=50)])
    Year = TextField('Year',validators=[Length(min=4, max=20)])
    recaptcha = RecaptchaField()
@app.route('/register/', methods=["GET","POST"])
def register_page():
        try:
           form=RegistrationForm()

           if form.validate_on_submit():
             
             Name=form.Name.data
             Number=form.Number.data
             Hall=form.Hall.data
             Department=form.Department.data
             Year=form.Year.data
             con=mysql.connect
             c= con.cursor()
             
             x = c.execute("SELECT * FROM contacts WHERE Number = (%d)"%(int(Number)))
             

             if int(x) > 0:
                   

                    flash("That number is already added")
                    return render_template('register.html', form=form)

             else:
                    c.execute("INSERT INTO contacts (Name,Number,Hall,Department,Year) VALUES (%s, %s, %s, %s, %s)",(Name, int(Number),Hall, Department, Year))
                    con.commit()
                    flash("Thanks for adding the contact!")
                    c.close()
                    con.close()
                    gc.collect()

                    return redirect(url_for('register_page'))

           return render_template("register.html", form=form)


        except Exception as e:
           return(str(e))


if __name__ == "__main__":
    app.run()
