import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Book Recommender", layout="wide")

# load the files
try:
    popular = pickle.load(open('popular.pkl', 'rb'))
    pt = pickle.load(open('pt.pkl', 'rb'))
    books = pickle.load(open('books.pkl', 'rb'))
    scores = pickle.load(open('similarity_scores.pkl', 'rb'))
except FileNotFoundError:
    st.error("Missing .pkl files! Make sure they are in the same folder.")

st.title('📚 Book Recommender System')

# sidebar search
st.sidebar.header("Find a Book")
booklist = pt.index.values
selectbook = st.sidebar.selectbox("Pick a book you like", booklist)

if st.sidebar.button('Recommend'):
    try:
        # find the book index
        idx = np.where(pt.index == selectbook)[0][0]
        items = sorted(list(enumerate(scores[idx])), key=lambda x: x[1], reverse=True)[1:6]

        st.subheader(f"Because you liked: {selectbook}")
        cols = st.columns(5)
        for i, col in enumerate(cols):
            # get book info
            df = books[books['Book-Title'] == pt.index[items[i][0]]].drop_duplicates('Book-Title')
            with col:
                st.image(df['Image-URL-M'].values[0])
                st.text(df['Book-Title'].values[0])
    except Exception as e:
        st.error("Something went wrong with the recommendation logic.")

st.divider()

# trending section (always visible)
st.header("Top Trending Books")
top10 = popular.head(10)

c1 = st.columns(5)
for i, col in enumerate(c1):
    with col:
        st.image(top10['Image-URL-M'].values[i])
        st.caption(f"**{top10['Book-Title'].values[i]}**")

c2 = st.columns(5)
for i, col in enumerate(c2):
    with col:
        st.image(top10['Image-URL-M'].values[i+5])
        st.caption(f"**{top10['Book-Title'].values[i+5]}**")