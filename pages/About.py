import streamlit as st
st.subheader("BOOK RECOMMENDATION SYSTEM")
st.write("Problem Statement")
st.write('During the last few decades, with the rise of Youtube, Amazon'
         ', Netflix, and many other such web services, recommender systems have taken more and more place in our lives. '
         'From e-commerce (suggest to buyers articles that could interest them) to online advertisement '
         '(suggest to users the right contents, matching their preferences), recommender systems are today'
         ' unavoidable in our daily online journeys. In a very general way, recommender systems are algorithms'
         ' aimed at suggesting relevant items to users (items being movies'
         ' to watch, text to read, products to buy, or anything else depending on industries).')
recommender_types = [
    "1. Popularity Based (Formula Based)",
    "2. Content Based (Based on Attributes, Find Related)",
    "3. Collaborative Filtering Based (e.g., K-Nearest Neighbors, User Ratings)",
    "4. Hybrid (Mixture of All Above)"
]
for recommender_type in recommender_types:
    st.write(recommender_type)

