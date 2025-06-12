import pandas as pd
from surprise import Reader, Dataset, SVD
from surprise.model_selection import train_test_split

print("Iniciando o sistema de recomendação colaborativa...")

# --- 1. Carregar os Dados ---
try:
    # Carregamos os arquivos que baixamos do MovieLens
    ratings_df = pd.read_csv('ratings.csv')
    movies_df = pd.read_csv('movies.csv')
except FileNotFoundError:
    print("Erro: Arquivos 'ratings.csv' ou 'movies.csv' não encontrados.")
    print("Certifique-se de que você baixou o dataset MovieLens e colocou os arquivos na pasta do projeto.")
    exit()

print("Datasets carregados com sucesso.")

# --- 2. Preparar os Dados para a Biblioteca Surprise ---

# O 'Reader' é usado para parsear o arquivo de ratings.
# O 'rating_scale' diz que as notas vão de 1 a 5.
reader = Reader(rating_scale=(1, 5))

# 'load_from_df' carrega o DataFrame do pandas no formato que a biblioteca entende.
# Precisamos das colunas na ordem: user, item, rating.
data = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader)

print("Dados preparados para o treinamento.")

# --- 3. Treinar o Modelo de Recomendação ---

# Vamos usar um dos algoritmos mais famosos, o SVD (Singular Value Decomposition).
# É uma técnica matemática avançada de "fatoração de matrizes" que encontra
# padrões e preferências "escondidos" nos dados de avaliação dos usuários.
print("Treinando o modelo SVD... (Isso pode levar um momento)")
algo = SVD()

# Dividimos os dados em treino e teste (uma boa prática)
trainset, testset = train_test_split(data, test_size=0.25)

# Treinamos o algoritmo com o conjunto de treino.
algo.fit(trainset)

print("Modelo treinado com sucesso!")

# --- 4. Gerar Recomendações para um Usuário ---

def get_collaborative_recommendations(user_id, n=10):
    """
    Gera recomendações para um usuário específico.
    """
    # Primeiro, pegamos a lista de todos os IDs de filmes
    all_movie_ids = ratings_df['movieId'].unique()
    
    # Depois, removemos os filmes que o usuário JÁ avaliou
    movies_rated_by_user = ratings_df[ratings_df['userId'] == user_id]['movieId'].unique()
    movies_to_predict = [movie_id for movie_id in all_movie_ids if movie_id not in movies_rated_by_user]
    
    # Agora, usamos nosso modelo treinado para prever a nota que o usuário daria
    # para cada filme que ele ainda não viu.
    predictions = [algo.predict(user_id, movie_id) for movie_id in movies_to_predict]
    
    # Ordenamos as previsões pela nota estimada (da maior para a menor)
    predictions.sort(key=lambda x: x.est, reverse=True)
    
    # Pegamos os 'n' melhores filmes recomendados
    top_n_predictions = predictions[:n]
    
    # Buscamos os IDs desses filmes
    top_n_movie_ids = [pred.iid for pred in top_n_predictions]
    
    # Buscamos os títulos desses filmes no nosso dataframe de filmes
    recommended_movies = movies_df[movies_df['movieId'].isin(top_n_movie_ids)]
    
    return recommended_movies[['title', 'genres']]

# --- 5. Teste Final ---
if __name__ == "__main__":
    # Vamos gerar recomendações para o usuário de exemplo com ID = 1
    USER_ID_TO_RECOMMEND = 1
    
    print(f"\n--- Gerando 10 recomendações para o Usuário #{USER_ID_TO_RECOMMEND} ---")
    
    recommendations = get_collaborative_recommendations(USER_ID_TO_RECOMMEND, n=10)
    
    print(recommendations)