from flask import Flask, render_template, request
import pickle
import numpy as np

# Load models and data
with open('popular.pkl', 'rb') as file:
    df_popular = pickle.load(file)

with open('pt.pkl', 'rb') as file:
    pt = pickle.load(file)

with open('books.pkl', 'rb') as file:
    books = pickle.load(file)

with open('similarity.pkl', 'rb') as file:
    similarity_scores = pickle.load(file)

app = Flask(__name__)

# Home Page
@app.route('/')
def index():
    images = [url.replace('http://', 'https://') for url in df_popular['Image-URL-M'].values]
    return render_template('index.html',
                           book_name=list(df_popular['Book-Title'].values),
                           author=list(df_popular['Book-Author'].values),
                           image=images,
                           votes=list(df_popular['num-ratings'].values),
                           rating=list(df_popular['avg-rating'].values)
                           )

# Recommend UI Page
@app.route('/recommend')
def recommend_UI():
    return render_template('recommend.html')

# Recommend Logic
@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda a: a[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        df_temp = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')
        title = df_temp['Book-Title'].values[0]
        author = df_temp['Book-Author'].values[0]
        image_url = df_temp['Image-URL-M'].values[0].replace('http://', 'https://')
        data.append([title, author, image_url])

    print(data)
    return render_template('recommend.html', data=data)

# Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
