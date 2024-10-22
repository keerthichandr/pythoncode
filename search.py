import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Load the books DataFrame
books_df = pd.read_csv("goodreads_data.csv")

# Function to preprocess the text
def preprocess_text(text):
    return str(text).lower()

# Preprocess descriptions
books_df['processed_Description'] = books_df['Description'].apply(preprocess_text)

# Vectorize the descriptions
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(books_df['processed_Description'])

# Fit the NearestNeighbors model
n_neighbors = 6  # Number of neighbors to return, including the input book
model = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')
model.fit(tfidf_matrix)

# Recommendation function based on description similarity
def recommend_books(description):
    processed_description = preprocess_text(description)
    description_vector = vectorizer.transform([processed_description])
    distances, indices = model.kneighbors(description_vector)
    indices = indices[0][1:]  # Exclude the input book from the recommendations
    return books_df.iloc[indices][['Book', 'Author']].to_dict(orient='records')