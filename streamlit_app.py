import streamlit as st
import pandas as pd

st.title("breakfast favaourites")
st.text("🥣omega 3 & blueberry oatmeal") 
st.text("🥗kale. spinach & rocket smothie")
st.text("🐔har-boiled free-range eggs")
st.text("🥑🍞 avocado toast")

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
st.dataframe(my_fruit_list)