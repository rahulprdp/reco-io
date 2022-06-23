
from email.policy import default
import pickle
from flask import Flask, render_template , request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import sqlalchemy

#ML Code 

filename = 'finalreco.pkl'
with open(filename, 'rb') as f:
    similarity,df,movie_db = pickle.load(f)

def recommend(movie):
    k=-1
    for i in range(1000):
      if movie_db[i][0].lower()==movie.lower():
        k=i
    ls = []
    ls.append("Incorrect Movie Name")
    if k==-1:
        return ls

    ls=[]

    
    index = k
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in range(1,10):
      ind=distances[i][0]
      ls.append(movie_db[ind][0])

    return ls

## End of ML Code


##Flask App -------------------------------------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///subs.db'

#Initialise DB
db=SQLAlchemy(app)

#Creating Models

class sub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    mail = db.Column(db.String(200), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)

    #Create fun to return string when we add stuff
    def __repr__(self):
        return '<name %r>' % self.id



@app.route('/')
def index() :
    return render_template("index.html")

@app.route('/res', methods=["POST"])
def result() :
    name = request.form.get("name")
    ls = recommend(name)
    if len(ls)==1:
        return render_template("index.html",name0 = ls[0])
    else:
        return render_template("result.html",name0 = ls[0],name1 = ls[1],name2 = ls[2],name3 = ls[3] ,name4 = ls[4])

@app.route('/about')
def about() :
    return render_template("about.html")



@app.route('/appends', methods=['POST','GET'])
def appends():
    fname = request.form.get("userName")
    fmail = request.form.get("userEmail")

    
    if request.method=="POST":
        if not fname or not fmail :
            errorStmt = "All Fields are required"
            return render_template("about.html",errorStmt=errorStmt, name=fname, mail=fmail)


        new_sub = sub(name=fname,mail=fmail)
        try:
            db.session.add(new_sub)
            db.session.commit()
            return redirect('/appends')
        except :
            return "<h1> There Was An Error </h1>"

    else :
        subs = sub.query.order_by(sub.dateCreated)
        n=""
        for s in subs:
            n=s.name
            
        return render_template("about.html",name="", mail="", sucMsg=n + " Was Scuccessfull Added ! ")


@app.route('/ctrl', methods=['POST','GET'])
def cntrl():
    subs = sub.query.order_by(sub.dateCreated)
    return render_template("ctrl.html",ss=subs)


