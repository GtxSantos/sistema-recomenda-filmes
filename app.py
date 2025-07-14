import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Reader, Dataset, SVD
import os
from dotenv import load_dotenv

load_dotenv() # Carrega as variáveis do arquivo .env

# O app agora sabe como encontrar a chave, se precisar dela.
API_KEY = os.getenv('TMDB_API_KEY')
# --- CONFIGURAÇÃO DA PÁGINA (Deve ser o primeiro comando Streamlit) ---
st.set_page_config(layout="wide", page_title="Sistema de Recomendação Híbrido")

# --- MOTOR DE RECOMENDAÇÃO POR CONTEÚDO (Content-Based) ---
@st.cache_data
def load_content_data():
    try:
        df = pd.read_csv('movies_data_tmdb.csv')
        df['content_soup'] = (df['genres'].fillna('').astype(str).str.replace(' ', '').str.replace(',', ' ') + ' ' + 
                              df['keywords'].fillna('').astype(str).str.replace(' ', '').str.replace(',', ' ') * 3 + ' ' + 
                              df['cast'].fillna('').astype(str).str.replace(' ', '').str.replace(',', ' ') * 3 + ' ' + 
                              df['director'].fillna('').astype(str).str.replace(' ', '').str.replace(',', ' ') * 3 + ' ' + 
                              df['overview'].fillna(''))
        return df
    except FileNotFoundError:
        return None

@st.cache_data
def calculate_content_similarity(df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['content_soup'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()
    return cosine_sim, indices

# --- MOTOR DE RECOMENDAÇÃO COLABORATIVA (Collaborative Filtering) ---
@st.cache_resource # Usamos cache_resource para o modelo treinado
def train_collaborative_model():
    try:
        ratings_df = pd.read_csv('ratings.csv')
        movies_df = pd.read_csv('movies.csv')
    except FileNotFoundError:
        return None, None
    
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader)
    trainset = data.build_full_trainset()
    algo = SVD()
    algo.fit(trainset)
    return algo, movies_df

# --- Carregando todos os dados e modelos ---
content_df = load_content_data()
if content_df is not None:
    content_cosine_sim, content_indices = calculate_content_similarity(content_df)

collaborative_algo, collaborative_movies_df = train_collaborative_model()

# --- INTERFACE PRINCIPAL ---
st.title("🎬 Sistema de Recomendação de Filmes Híbrido")

if content_df is None or collaborative_algo is None:
    st.error("Erro ao carregar os arquivos de dados. Certifique-se de que 'movies_data_tmdb.csv', 'ratings.csv' e 'movies.csv' estão na pasta do projeto.")
else:
    # --- ABAS PARA CADA TIPO DE RECOMENDAÇÃO ---
    tab1, tab2 = st.tabs(["**1. Encontrar Filmes Parecidos (por Conteúdo)**", "**2. Recomendações Para Você (por Perfil)**"])

    # --- ABA 1: RECOMENDAÇÃO POR CONTEÚDO ---
    with tab1:
        st.header("Encontre filmes similares a um que você gosta")
        movie_list = content_df['title'].tolist()
        selected_movie = st.selectbox("Escolha um filme:", movie_list, key="content_select")
        
    if st.button("Recomendar Similares", key="content_button"):
        if selected_movie:
            # Pega o índice ou a série de índices
            idx_lookup = content_indices[selected_movie]

            # Verifica se o resultado é uma série (múltiplos filmes) ou um único número
            if isinstance(idx_lookup, pd.Series):
                # Se for uma série, pega o primeiro índice
                idx = idx_lookup.iloc[0]
            else:
                # Se for um único número, apenas o utiliza
                idx = idx_lookup

            sim_scores = list(enumerate(content_cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:6]
            movie_indices = [i[0] for i in sim_scores]
            recommendations = content_df.iloc[movie_indices]
            st.subheader(f"Recomendações parecidas com '{selected_movie}':")
            POSTER_BASE_URL = "https://image.tmdb.org/t/p/w342"
            cols = st.columns(5)
            for i, row in enumerate(recommendations.itertuples()):
                with cols[i]:
                    poster_path = row.poster_path
                    if pd.notna(poster_path):
                        st.image(POSTER_BASE_URL + poster_path, use_container_width=True)
                    st.caption(f"**{row.title}**")

    # --- ABA 2: RECOMENDAÇÃO COLABORATIVA ---
    with tab2:
        st.header("Descubra filmes baseados no seu perfil de usuário")
        user_id = st.number_input("Digite seu ID de Usuário (ex: 1 a 610):", min_value=1, max_value=610, value=1, step=1)
        
        if st.button("Obter Recomendações", key="collab_button"):
            all_movie_ids = collaborative_movies_df['movieId'].unique()
            user_ratings = pd.read_csv('ratings.csv')
            movies_rated_by_user = user_ratings[user_ratings['userId'] == user_id]['movieId'].unique()
            movies_to_predict = [movie_id for movie_id in all_movie_ids if movie_id not in movies_rated_by_user]
            
            predictions = [collaborative_algo.predict(user_id, movie_id) for movie_id in movies_to_predict]
            predictions.sort(key=lambda x: x.est, reverse=True)
            top_n_predictions = predictions[:10]
            top_n_movie_ids = [pred.iid for pred in top_n_predictions]
            
            recommended_movies = collaborative_movies_df[collaborative_movies_df['movieId'].isin(top_n_movie_ids)]

            st.subheader(f"Recomendações para o Usuário #{user_id}:")
            # Exibindo como uma lista simples
            for row in recommended_movies.itertuples():
                st.write(f"- **{row.title}** ({row.genres})")