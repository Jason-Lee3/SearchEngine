from flask import *
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, RadioField, SubmitField)
from wtforms.validators import InputRequired, Length, DataRequired
from index import fileDirectory, buildIndex, booleanSearch, displayTop10Postings, returnTop10Postings, porterStemming, tfidf, mergeIndex, buildIndexOfIndex, indexOfIndex, makeDocFile, retrieveDocId, openCache
from porterStemming import PorterStemmer
import time

# using flask for our web interface
app = Flask(__name__)
app.secret_key = "123"

# form (the user writes a query in our search bar)
class BasicForm(FlaskForm):
    ids = StringField("ID",validators=[DataRequired()], render_kw={"placeholder": "What are you looking for?"})
    submit = SubmitField("Search")

@app.route("/", methods=["GET", "POST"])
def index():
    form = BasicForm()
    return render_template("index.html", form = form)

# ids will be our query. ex. if you search "Cristina lopes" in the search bar, ids will equal a string of "Cristina Lopes"
@app.route("/search", methods=["GET", "POST"])
def search():
    form = BasicForm()
    csrf_token = request.form['csrf_token']
    ids = request.form['ids']
    print(ids)
    st = time.time()
    # if we decide to use porter stemming
    """p = PorterStemmer()
    print("Previous", ids)
    ids = porterStemming(ids, p)
    print("After", ids)"""
    query = ids.lower().split(" ")
    # print(query)
    # displayTop5Postings(booleanSearch(invertedIndex, query), doc_id)
    listOfUrls = returnTop10Postings(booleanSearch(query))
    et = time.time()
    exe_time = (et-st)*1000
    print(f"execution time: {exe_time} ms") 
    return render_template("search.html", csrf_token=csrf_token, ids=ids, len = len(listOfUrls), listOfUrls= listOfUrls, form=form)

if __name__ == "__main__":
    #fileDirectory()
    #tfidf()
    #mergeIndex()
    buildIndexOfIndex() # have this uncommented when you're running
    #makeDocFile()
    retrieveDocId() # have this uncommmted
    openCache() # have this uncomted
    app.run()