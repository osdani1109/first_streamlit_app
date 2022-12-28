import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

#st.stop()
st.title("breakfast favaourites")
st.text("🥣omega 3 & blueberry oatmeal") 
st.text("🥗kale. spinach & rocket smothie")
st.text("🐔har-boiled free-range eggs")
st.text("🥑🍞 avocado toast")

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
st.dataframe(fruits_to_show)
def get_frutyvice_data(this_fruit_choice):
    frutlyvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    fruityvice_normalized = pd.json_normalize(frutlyvice_response.json())
    return fruityvice_normalized

st.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = st.text_input('What fruit would you like information about?')
    if not fruit_choice:
        st.error("please select a fruit to get information.")
    else:
        back_from_function = get_frutyvice_data(fruit_choice)
        st.dataframe(back_from_function)
except URLError as e:
    st.error()

st.header("the fruit load list contains:")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
        my_data_row = my_cur.fetchall()
        return my_data_row

if st.button('get fruit load list'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_row = get_fruit_load_list()
    st.dataframe(my_data_row)
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('"+new_fruit+"')")
        return "Thanks for adding "+new_fruit


add_my_fruit = st.text_input('What fruit would you like to add?')
if st.button("Add a fruit to the list"):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    st.write(back_from_function)
