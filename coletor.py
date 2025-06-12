import requests
import pandas as pd
import time

# --------------- CONFIGURAÇÃO ---------------
API_KEY = '54ef234da6f9f785518fa955639f7b38' # Substitua pela sua chave da API do TMDB
BASE_URL = 'https://api.themoviedb.org/3'
LANGUAGE = 'pt-BR'
# --------------- FIM DA CONFIGURAÇÃO ---------------

def get_movie_details(movie_id, api_key):
    """Busca detalhes extras de um filme: créditos (elenco, diretor) e palavras-chave."""
    details = {'director': '', 'cast': [], 'keywords': []}

    # Busca por créditos (elenco e equipe)
    try:
        credits_url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={api_key}&language={LANGUAGE}"
        response = requests.get(credits_url)
        response.raise_for_status()
        credits_data = response.json()

        # Encontra o diretor na equipe
        for member in credits_data.get('crew', []):
            if member.get('job') == 'Director':
                details['director'] = member.get('name')
                break
        
        # Pega os 3 atores principais
        details['cast'] = [actor.get('name') for actor in credits_data.get('cast', [])[:3]]

    except requests.exceptions.RequestException as e:
        print(f"  - Erro ao buscar créditos para o filme ID {movie_id}: {e}")

    # Busca por palavras-chave
    try:
        keywords_url = f"{BASE_URL}/movie/{movie_id}/keywords?api_key={api_key}"
        response = requests.get(keywords_url)
        response.raise_for_status()
        keywords_data = response.json()
        details['keywords'] = [keyword.get('name') for keyword in keywords_data.get('keywords', [])]

    except requests.exceptions.RequestException as e:
        print(f"  - Erro ao buscar palavras-chave para o filme ID {movie_id}: {e}")

    return details


def fetch_movies_from_tmdb(api_key, num_pages_to_fetch=2): # Reduzimos para 2 páginas para ser mais rápido
    """Busca filmes populares e enriquece com detalhes extras."""
    all_movies_data = []
    print(f"Buscando {num_pages_to_fetch} página(s) de filmes populares...")

    # Primeiro, busca a lista de filmes populares
    popular_movies_raw = []
    for page_num in range(1, num_pages_to_fetch + 1):
        endpoint = f"{BASE_URL}/movie/popular"
        params = {'api_key': api_key, 'language': LANGUAGE, 'page': page_num}
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get('results'):
                popular_movies_raw.extend(data['results'])
                print(f"Página {page_num} de filmes populares buscada.")
            else:
                break
            time.sleep(0.5)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar lista de filmes populares: {e}")
            return []

    # Busca o mapeamento de gêneros
    genre_map = {}
    try:
        genre_url = f"{BASE_URL}/genre/movie/list?api_key={api_key}&language={LANGUAGE}"
        response_genre = requests.get(genre_url)
        response_genre.raise_for_status()
        genres_data = response_genre.json()
        genre_map = {genre['id']: genre['name'] for genre in genres_data['genres']}
        print("Mapeamento de gêneros obtido com sucesso.")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar mapeamento de gêneros: {e}")

    # Agora, processa cada filme para adicionar detalhes
    print(f"\nEnriquecendo dados de {len(popular_movies_raw)} filmes...")
    for i, movie in enumerate(popular_movies_raw):
        print(f"Processando filme {i+1}/{len(popular_movies_raw)}: {movie.get('title')}")
        
        # Busca os detalhes extras (diretor, elenco, keywords)
        extra_details = get_movie_details(movie.get('id'), api_key)
        
        # Mapeia os nomes dos gêneros
        genre_names = [genre_map.get(genre_id, "Desconhecido") for genre_id in movie.get('genre_ids', [])]
        
        all_movies_data.append({
            'id_tmdb': movie.get('id'),
            'title': movie.get('title'),
            'overview': movie.get('overview'),
            'genres': ", ".join(genre_names),
            'director': extra_details['director'],
            'cast': ", ".join(extra_details['cast']),
            'keywords': ", ".join(extra_details['keywords']),
            'release_date': movie.get('release_date'),
            'popularity': movie.get('popularity'),
            'vote_average': movie.get('vote_average'),
            'vote_count': movie.get('vote_count'),
            'poster_path': movie.get('poster_path')
        })
        time.sleep(0.5) # Delay para não sobrecarregar a API

    print("\nProcessamento concluído.")
    return all_movies_data


# --- Execução Principal ---
if __name__ == "__main__":
    if API_KEY == 'SUA_CHAVE_API_AQUI' or not API_KEY:
        print("ERRO: Por favor, substitua 'SUA_CHAVE_API_AQUI' pela sua chave da API do TMDB no topo do script.")
    else:
        # Lembre-se de colocar sua chave aqui!
        movies_enriched = fetch_movies_from_tmdb(API_KEY, num_pages_to_fetch=2) # 2 páginas = ~40 filmes

        if movies_enriched:
            df_movies = pd.DataFrame(movies_enriched)
            print("\n--- Amostra dos Dados Enriquecidos ---")
            # Mostra algumas das novas colunas
            print(df_movies[['title', 'director', 'cast', 'keywords']].head())
            
            df_movies.to_csv('movies_data_tmdb.csv', index=False, encoding='utf-8')
            print("\nNovo arquivo 'movies_data_tmdb.csv' com dados enriquecidos foi salvo com sucesso!")
        else:
            print("Nenhum filme foi buscado. Verifique sua chave de API e conexão.")