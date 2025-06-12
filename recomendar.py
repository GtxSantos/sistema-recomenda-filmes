import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- CARREGAR OS DADOS ---
try:
    df_movies = pd.read_csv('movies_data_tmdb.csv')
except FileNotFoundError:
    print("Erro: Arquivo 'movies_data_tmdb.csv' não encontrado.")
    print("Certifique-se de que o arquivo está na mesma pasta que o script 'recomendar.py'.")
    exit()

# --- LÓGICA DE RECOMENDAÇÃO MELHORADA ---

# Tratar valores ausentes (NaN) nas colunas, substituindo por uma string vazia.
df_movies['overview'] = df_movies['overview'].fillna('')
df_movies['genres'] = df_movies['genres'].fillna('')

# --- A GRANDE MELHORIA ESTÁ AQUI! ---
# Vamos criar uma "sopa de conteúdo" combinando gêneros e sinopse.
# Repetimos os gêneros para dar mais peso a eles na análise de similaridade.
df_movies['content_soup'] = df_movies['genres'] + ' ' + df_movies['genres'] + ' ' + df_movies['overview']


# Criar um vetorizador TF-IDF.
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Aplicar o vetorizador na nossa nova "sopa de conteúdo".
tfidf_matrix = tfidf_vectorizer.fit_transform(df_movies['content_soup'])

# Calcular a matriz de similaridade de cossenos (esta parte não muda).
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Criar a Série de índices (esta parte não muda).
indices = pd.Series(df_movies.index, index=df_movies['title']).drop_duplicates()


def get_recommendations(title, cosine_sim_matrix=cosine_sim, num_recommendations=5):
    """
    Função que recebe o título de um filme e retorna uma lista de filmes recomendados.
    """
    if title not in indices:
        return f"Filme '{title}' não encontrado em nosso banco de dados."

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations+1]
    movie_indices = [i[0] for i in sim_scores]
    return df_movies['title'].iloc[movie_indices].tolist()


# --- TESTANDO A NOVA FUNÇÃO ---
if __name__ == "__main__":
    # Vamos testar com 'Viúva Negra' de novo para ver a diferença!
    filme_exemplo = "Viúva Negra" 
    
    recomendacoes = get_recommendations(filme_exemplo)

    print(f"--- Recomendações (VERSÃO MELHORADA) para quem gostou de '{filme_exemplo}' ---")
    if isinstance(recomendacoes, list):
        for i, movie in enumerate(recomendacoes):
            print(f"{i+1}. {movie}")
    else:
        print(recomendacoes)