
import pickle
from unicodedata import name
from flask import Flask, render_template , request,redirect

#A bit of change
#ML Code 


filename = 'finalreco.pkl'
with open(filename, 'rb') as f:
    similarity,df,movie_db = pickle.load(f)

def recommend(movie):
    for i in range(1000):
      if movie_db[i][0].lower()==movie.lower():
        k=i

    ls = []
    index = k
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in range(1,10):
      ind=distances[i][0]
      ls.append(movie_db[ind][0])

    return ls

## End of ML Code



app = Flask(__name__)

@app.route('/')
def index() :
    return render_template("index.html")

@app.route('/res', methods=["POST"])
def result() :
    name = request.form.get("name")
    ls = recommend(name)
    return render_template("result.html",name = ls)


