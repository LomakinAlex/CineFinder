import csv

from flask import Flask, render_template, request, redirect, jsonify
from collections import Counter

csv.field_size_limit(112 * 1048576) # 112 MB

app = Flask(__name__)

@app.route('/')
def index(): return render_template("index.html")

@app.route('/about')
def about(): return render_template("about.html")

@app.route('/api')
def api(): return render_template('api.html')

@app.route('/find', methods=["GET"])
def findget(): return redirect('/')

def load_word_to_films():
    word_to_films = {}
    with open('find.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            word_to_films[row['Word']] = row['Movie Titles'].split(', ')
    return word_to_films

def load_films_data():
    films_data = {}
    with open('data.csv', mode='r', newline='', encoding='utf-8') as filmscsv:
        reader = csv.DictReader(filmscsv)
        for row in reader:
            films_data[row["Title"].strip()] = list(row.items())
    return films_data

word_to_films = load_word_to_films()
films_data = load_films_data()

@app.route('/find', methods=["POST"])
def find():
    if request.method == "POST":
        info = request.form.to_dict()
        plot = info["toFind"].replace("\n","")
        words = plot.lower().split()
        plen = len(words)
        
        films = []
        for word in words:
            if word in word_to_films:
                films.extend(word_to_films[word])
        
        film_counter = Counter(films)
        common_films = [film for film, count in film_counter.items() if count <= plen and film in films_data]
        lengoff = len(common_films)
        common_films = common_films[:50]
        print(common_films)
        
        dumpdata = [films_data[film] for film in common_films]
        return render_template("find.html", data=dumpdata, w=info, leng=lengoff)

@app.route('/api/ask/')
def ask():
    plot = request.args.get('plot')
    amount = request.args.get('amount')
    
    if plot is None and amount is None: 
        return jsonify({"error": "Ask Error: The 'plot' and 'amount' argument was not found."})
    if plot is None: return jsonify({"error": "Ask Error: The 'plot' argument was not found."})
    if amount is None: return jsonify({"error": "Ask Error: The 'amount' argument was not found."})
    if not isinstance(plot, str): return jsonify({"error": "Ask Error: 'plot' must be string"})
    try: amount = int(amount)
    except: return jsonify({"error": "Ask Error: 'amount' should be integer"})
    if amount < 1: return jsonify({"error": "Ask Error: 'amount' must be at least 1"})

    words = plot.lower().split()
    plen = len(words)
    
    films = []
    for word in words:
        if word in word_to_films:
            films.extend(word_to_films[word])
    
    film_counter = Counter(films)
    d = [film for film, count in film_counter.items() if count <= plen and film in films_data]
    
    return jsonify(d[:amount])

@app.errorhandler(404)
def page_not_found(e): return render_template('error.html',error=e), 404

if __name__ == "__main__": app.run(debug=True)