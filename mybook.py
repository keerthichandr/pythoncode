import pandas as pd



def get_mybook(user_id): 
    # Load the CSV file into a DataFrame (adjust the file path as needed)
    csv_file_path = 'mybook.csv'
    books_df = pd.read_csv(csv_file_path)
    print(user_id)
    if not user_id:
        return None  # If no user_id is provided, return None

    # Filter the DataFrame based on the user ID
    user_books = books_df[books_df['userid'] == user_id]

    # Check if any books were found for the user
    if user_books.empty:
        return []  # Return an empty list if no books found

    # Prepare the response format
    recommendations = user_books[['author', 'booktitle','datetime']].rename(columns={'author': 'Author', 'booktitle': 'Book','datetime':'DateTime'}).to_dict(orient='records')

    # Return the recommendations in the desired format
    return recommendations