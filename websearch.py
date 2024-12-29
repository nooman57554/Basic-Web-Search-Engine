from flask import Flask, request, render_template
from web_crawler import engine, Page
from sqlalchemy.orm import sessionmaker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__, template_folder="./static", static_folder="./static")


@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/websearch", methods=['GET', 'POST'])
def websearch():
    query = request.form.get("query")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    if query:
        # Fetch pages containing the query terms
        pages = session.query(Page).filter(
            (Page.title.like(f"%{query}%")) | 
            (Page.content.like(f"%{query}%"))
        ).all()

        if not pages:
            return render_template("results.html", query=query, results=None)
        
        # Prepare text data for vectorization
        documents = [query] + [page.content for page in pages]
        tfidf_vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
        print(tfidf_matrix)

        # Compute cosine similarity
        query_vector = tfidf_matrix[0]
        page_vectors = tfidf_matrix[1:]
  
        similarities = cosine_similarity(query_vector, page_vectors).flatten()
     
        # Combine cosine similarity and PageRank for ranking
        results = []
        for page, similarity in zip(pages, similarities):
            score = similarity + page.pagerank  # Weighted score
            results.append((page, score))

        # Sort results by the combined score (descending)
        results = sorted(results, key=lambda x: x[1], reverse=True)

        return render_template("results.html", query=query, results=results)
    
    return render_template("homepage.html")


if __name__ == "__main__":
    app.run(debug=True)
