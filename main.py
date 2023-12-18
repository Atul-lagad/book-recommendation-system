import streamlit as st
import pandas as pd
import random
import numpy as np
#
#
# #Define navbar options
# options = ["Home", "Content_Based", "Recommended", "Contact"]
#
# # Define functions for each button click
# def on_click_home():
#     return st.write("Welcome to Book Recommandation System")
#     # ... add specific content for Home page ...
#
# def on_click_content_based():
#     st.write("This is the About page")
#     # ... add specific content for About page ...
#
# def on_click_recommended():
#     st.write("This is the Projects page")
#     # ... add specific content for Projects page ...
#
# def on_click_contact():
#     st.write("This is the Contact page")
#     # ... add specific content for Contact page ...
#
# # Create the navbar
# with st.sidebar:
#     st.sidebar.markdown("<h1 style='text-align: center; color: #111111;'>Menu</h1>", unsafe_allow_html=True)
#     st.sidebar.markdown("---")
#     for option in options:
#         # Use buttons with click functions
#         st.sidebar.button(option, key=option, on_click=eval(f"on_click_{option.lower()}"))
#



st.header("Book Recommendation System")
tab1, tab2 = st.tabs(["Trending Books", "Recommendation"])

with tab1:
    books = pd.read_csv("books.csv.gzip", compression="gzip",low_memory=False)
    # books = pd.read_csv('books.csv', low_memory=False)
    # users = pd.read_csv('users.csv')
    # ratings = pd.read_csv('ratings.csv')
    # # Popularity-based recommendation logic
    # rating_with_name = pd.merge(ratings, books, on='ISBN', how='inner')
    # num_rating_df = rating_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
    # num_rating_df.rename(columns={'Book-Rating': 'num_rating_on_book'}, inplace=True)
    # avg_rating_df = rating_with_name.groupby('Book-Title')['Book-Rating'].mean().reset_index()
    # avg_rating_df.rename(columns={'Book-Rating': 'avg_rating'}, inplace=True)
    # popular_df = pd.merge(num_rating_df, avg_rating_df, on='Book-Title', how='inner')
    # popular_df = popular_df[popular_df['num_rating_on_book'] >= 250].sort_values(by='avg_rating', ascending=False)
    # a = pd.merge(popular_df, books, on='Book-Title', how='inner').drop_duplicates('Book-Title')
    # popular_df_final = a[['Book-Title', 'Book-Author', 'Image-URL-M', 'num_rating_on_book', 'avg_rating', 'Year-Of-Publication']]
    popular_df_final=pd.read_csv('popular.csv')
    # Selecting random 5 from them
    random_sample = popular_df_final.sample(n=10, random_state=random.randint(1, 100))

    # Assuming you have the following lists
    a = list(random_sample['Book-Title'])
    b = list(random_sample['Image-URL-M'])
    c = list(random_sample['Book-Author'])
    #d = list(random_sample['num_rating_on_book'])
    # per row 5 books
    num_columns_per_row = 5
    for i in range(0, len(a), num_columns_per_row):
        current_row_items = a[i:i + num_columns_per_row]
        current_row_images = b[i:i + num_columns_per_row]
        current_row_authors = c[i:i + num_columns_per_row]
        #current_row_ratings=d[i:i + num_columns_per_row]
        # Create a row with up to num_columns_per_row items
        columns = st.columns(len(current_row_items), gap="large")
        for j in range(len(current_row_items)):
            with columns[j]:
                st.image(current_row_images[j])
                st.caption(f'<span style="color:black">{current_row_items[j]}</span>', unsafe_allow_html=True)
                #st.caption("Ratings: " + str(current_row_ratings[j]))
                st.caption(" Author: " + current_row_authors[j])
        st.markdown("---")
    # For refresh
    def generate_random_sample():
        return popular_df_final.sample(n=10, random_state= random.randint(1, 100))

    if st.button("Generate Random Sample"):
        st.session_state.random_sample = generate_random_sample()
    else:
        st.write('')

with tab2:
    name = st.text_input('Book title', '')

    if name:  # Check if the input name is not empty
        # rating_with_name = pd.merge(ratings, books, on='ISBN', how='inner')
        # b = rating_with_name.groupby('User-ID').count()['Book-Rating'] > 100
        # exp_users = b[b].index
        # filtered_user = rating_with_name[rating_with_name['User-ID'].isin(exp_users)]
        # a = filtered_user.groupby('Book-Title').count()['Book-Rating'] > 100
        # filterd_book = a[a].index
        # final_rating = filtered_user[filtered_user['Book-Title'].isin(filterd_book)]
        final_rating=pd.read_csv("final.csv")
        pt = final_rating.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
        pt.fillna(0, inplace=True)
        # pt=pd.read_csv('pt.csv')

        # Calculate cosine similarity
        from sklearn.metrics.pairwise import cosine_similarity
        similarity_score = cosine_similarity(pt)

        # Function to recommend books
        def recommend(book_name):
            if book_name in pt.index:
                index = np.where(pt.index == book_name)[0][0]
                similar_item = list(enumerate(similarity_score[index]))
                similar_item = sorted(similar_item, key=lambda x: x[1], reverse=True)
                similar_item = similar_item[0:6]
                listt = [pt.index[i[0]] for i in similar_item]
                recommendations=listt

                # Get recommendations
                # First book data
                recommended_books_data_first = books[books['Book-Title'] == recommendations[0]].head(1)
                #st.table(recommended_books_data_first)
                aaa = list(recommended_books_data_first['Book-Title'])
                bbb = list(recommended_books_data_first['Image-URL-M'])
                ccc = list(recommended_books_data_first['Book-Author'])
                # Display details of the first book separately
                st.subheader("Your Book")
                col1, col2= st.columns([1, 3])
                with col1:
                    st.image(bbb[0])
                with col2:
                    st.table(recommended_books_data_first[['Book-Title','Book-Author','Year-Of-Publication']])

                # other books
                st.subheader("Recommended for You")
                recommendations = recommendations[1:6]
                # Filter books DataFrame based on recommendations
                recommended_books_data = books[books['Book-Title'].isin(recommendations)]
                recommended_books_data.drop_duplicates(['Book-Title'], inplace=True)

                # Display recommended books data
                # st.write("Recommended Books:")
                # st.write(recommended_books_data)

                # Assuming you have the following lists
                aa = list(recommended_books_data['Book-Title'])
                bb = list(recommended_books_data['Image-URL-M'])
                cc = list(recommended_books_data['Book-Author'])
                # per row 5 books
                num_columns_per_row = 5
                for i in range(0, len(aa), num_columns_per_row):
                    current_row_items = aa[i:i + num_columns_per_row]
                    current_row_images = bb[i:i + num_columns_per_row]
                    current_row_authors = cc[i:i + num_columns_per_row]

                    # Create a row with up to num_columns_per_row items
                    columns = st.columns(len(current_row_items), gap="large")
                    for j in range(len(current_row_items)):
                        with columns[j]:
                            st.image(current_row_images[j])
                            st.caption(f'<span style="color:black">{current_row_items[j]}</span>',
                                       unsafe_allow_html=True)
                            st.caption(" Author: " + current_row_authors[j])
                    st.markdown("---")

            else:
                st.subheader(f"The book with name '{book_name}' is not found , Are you searching")
                search = pt[pt.index.str.contains(book_name)]
                # if book is not in pt dataset , means we cannot recommand for it , but show similar matches of it
                recommendations = list(search.index)[:5]
                recommended_books_data = books[books['Book-Title'].isin(recommendations)]
                recommended_books_data.drop_duplicates(['Book-Title'], inplace=True)
                aa = list(recommended_books_data['Book-Title'])
                bb = list(recommended_books_data['Image-URL-M'])
                cc = list(recommended_books_data['Book-Author'])
                # per row 5 books
                num_columns_per_row = 5
                for i in range(0, len(aa), num_columns_per_row):
                    current_row_items = aa[i:i + num_columns_per_row]
                    current_row_images = bb[i:i + num_columns_per_row]
                    current_row_authors = cc[i:i + num_columns_per_row]

                    # Create a row with up to num_columns_per_row items
                    columns = st.columns(len(current_row_items), gap="large")
                    for j in range(len(current_row_items)):
                        with columns[j]:
                            st.image(current_row_images[j])
                            st.caption(f'<span style="color:black">{current_row_items[j]}</span>',
                                       unsafe_allow_html=True)
                            st.caption(" Author: " + current_row_authors[j])
                    st.markdown("---")
        recommend(name)




