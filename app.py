# ========================================   /  Required Libraries   /   =================================== #
import streamlit as st
import pickle
import pandas as pd
import requests

# ========================================   /   Dash board   /   =================================== #
# Configuring Streamlit GUI 

st.set_page_config(page_title="Movie Recommender System", page_icon="https://www.shutterstock.com/image-vector/film-clapper-3d-cartoon-icon-600nw-2239181291.jpg",
                   layout="wide", initial_sidebar_state="collapsed", menu_items=None)

# Title

st.title(":cyan[Movie Recommender System 🎞️] ")
st.write(" ")
st.write(" ")

# Sidebar

with st.sidebar:
   
   st.image("movie-icon-15142.png",use_column_width=True)
   
   st.markdown("#### Domain : :grey[Media]")
   st.markdown("#### Skills take away from this Project : :grey[Python scripting , Streamlit, API integration, NLP]")
   st.markdown("#### Overall view : :grey[Building a movie recommender system with a simple UI using streamlit , that suggests movies to users based on their past behavior and preferences.]")
   st.markdown("#### Developed by : :grey[VIDHYALAKSHMI K K]")

# ========================================   /   Movie recommendation zone   /   =================================== #

with open('movies.pkl','rb') as f:
    movies=pickle.load(f)

movies_list=movies['title'].values
selected_movie_name = st.selectbox(options=movies_list,label='*Select a movie*')

with open('consine_similarity.pkl','rb') as f:
    cosine_sim=pickle.load(f)

# Function to fetch the movie posters

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8f622a5b86847048458dea9df1249c67&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path is None:
        print(f"Warning: No poster found for movie ID {movie_id}")
        full_path = "https://example.com/default_poster.jpg"  # Fallback image
    else:
        full_path = "https://image.tmdb.org/t/p/w500" + poster_path
    return full_path

# Function to fetch the selected movie details

def fetch_movie_details(movie_id):
    details={}
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8f622a5b86847048458dea9df1249c67&language=en-US"
    data = requests.get(url).json()
    details['title']=data.get('title')
    details['overview']=data.get('overview')
    details['release_date']=data.get('release_date')
    details['run_time']=str(data.get('runtime'))+' min(s)'
    details['status']=data.get('status')
    details['ratings']=round(data.get('vote_average'),1)
    details['genre']=[i['name'] for i in data['genres']]
    return details

# Function to fetch the recommendations

def recommend(movie_title):
    recommended_movie_names = []
    recommended_movie_posters = []
    movie_index=movies[movies['title'] == movie_title].index[0]
    similarity_scores = pd.DataFrame(cosine_sim[movie_index],columns=["similarity"])
    movie_indices = similarity_scores.sort_values("similarity", ascending=False)[1:11].index
    
    for i in movie_indices:
        movie_id=movies.iloc[i].id
        recommended_movie_names.append(movies['title'].iloc[i])
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names,recommended_movie_posters

# Displays the selected movie details

if st.button('Recommend'):
    st.write(" ")
    st.write(" ")
    col1, col2 ,col3= st.columns([1.5,0.1,5.5])
    with col1:
        selected_movie_index=movies[movies['title'] == selected_movie_name].index[0]
        selected_movie_id=movies.iloc[selected_movie_index].id
        poster=fetch_poster(selected_movie_id)
        st.image(poster)
    with col3:
        details=fetch_movie_details(selected_movie_id)
        title=details['title']
        st.write(f"**TITLE** : :grey[{title}]")
        overview=details['overview']
        st.write(f"**OVERVIEW** : :grey[{overview}]")
        genre=details['genre']
        genres=""
        for i in genre:
            genres+=i+" , "
        st.write(f"**GENRE** : :grey[{genres[:-2]}]")
        ratings=details['ratings']
        st.write(f"**RATINGS** : :grey[{ratings}]")
        release_date=details['release_date']
        st.write(f"**RELEASE DATE** : :grey[{release_date}]")
        run_time=details['run_time']
        st.write(f"**RUN TIME** : :grey[{run_time}]")
        status=details['status']
        st.write(f"**STATUS** : :grey[{status}]")
    
    st.write(" ")
    st.write(" ")
    st.markdown('<h2> Recommended Movies for you </h2>',unsafe_allow_html=True)
    st.write(" ")
    st.write(" ")
    st.write(" ")

# Displays the recommendations

    name,poster=recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(name[0])
        st.image(poster[0])
    with col2:
        st.write(name[1])
        st.image(poster[1])

    with col3:
        st.write(name[2])
        st.image(poster[2])
    with col4:
        st.write(name[3])
        st.image(poster[3])
    with col5:
        st.write(name[4])
        st.image(poster[4])

    st.write("")
    st.write("")
    st.write("")
    st.write("")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(name[5])
        st.image(poster[5])
    with col2:
        st.write(name[6])
        st.image(poster[6])

    with col3:
        st.write(name[7])
        st.image(poster[7])
    with col4:
        st.write(name[8])
        st.image(poster[8])
    with col5:
        st.write(name[9])
        st.image(poster[9])

# ========================================   /   Completed  /   =================================== #