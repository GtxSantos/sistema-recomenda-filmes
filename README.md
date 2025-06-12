# 🎬 Sistema de Recomendação de Filmes Híbrido

![Prévia da Aplicação](Captura de Tela (168).png)

Um sistema de recomendação de filmes completo e interativo, desenvolvido em Python, que utiliza uma abordagem híbrida para fornecer sugestões personalizadas. A aplicação foi construída com Streamlit e integra dois modelos distintos de Machine Learning.

---

## 🚀 Sobre o Projeto

Este projeto foi desenvolvido como um estudo prático e profundo sobre sistemas de recomendação. O objetivo era construir uma aplicação funcional que não apenas recomendasse filmes, mas também explorasse e comparasse duas das mais importantes técnicas da área:

* **Filtragem por Conteúdo (Content-Based Filtering):** Recomenda filmes com base em suas características intrínsecas (gênero, enredo, elenco, diretor, etc.). Ideal para encontrar itens similares a um que o usuário já conhece e gosta.
* **Filtragem Colaborativa (Collaborative Filtering):** Recomenda filmes com base no comportamento e nas avaliações de uma comunidade de usuários. É excelente para descobrir novos filmes que fogem do óbvio, mas que se alinham ao perfil de gosto do usuário.

A combinação dessas duas técnicas em uma única aplicação web interativa demonstra um fluxo de trabalho completo de um projeto de Data Science.

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído com as seguintes tecnologias e bibliotecas:

* **Linguagem:** Python
* **Análise de Dados:** Pandas, NumPy
* **Machine Learning:** Scikit-learn, Scikit-surprise (para SVD)
* **Interface Web:** Streamlit
* **Coleta de Dados:** API do The Movie Database (TMDB)
* **Versionamento:** Git & GitHub

---

## 🏁 Como Rodar o Projeto Localmente

Siga os passos abaixo para executar o projeto em sua máquina.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/GtsSantos/sistema-recomendacao-filmes.git](https://github.com/GtsSantos/sistema-recomendacao-filmes.git)
    cd sistema-recomendacao-filmes
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para Windows
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```

3.  **Instale as dependências:**
    O arquivo `requirements.txt` contém todas as bibliotecas necessárias.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Baixe os datasets externos:**
    Para a Filtragem Colaborativa, é necessário baixar o dataset "MovieLens Small".
    - Acesse [https://grouplens.org/datasets/movielens/latest/](https://grouplens.org/datasets/movielens/latest/)
    - Baixe `ml-latest-small.zip`, descompacte e coloque os arquivos `ratings.csv` e `movies.csv` na raiz da pasta do projeto.

5.  **Execute a aplicação Streamlit:**
    ```bash
    streamlit run app_final.py
    ```

A aplicação será aberta no seu navegador!

---

## ✨ Agradecimentos

* Dados dos filmes fornecidos pela **[API do TMDB](https://www.themoviedb.org/)**.
* Dataset de avaliações fornecido pelo **[MovieLens](https://grouplens.org/datasets/movielens/)**.
* Projeto desenvolvido em colaboração guiada com a **IA Gemini do Google**.
