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
st.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = st.text_input('What fruit would you like information about?')
    if not fruit_choice:
        st.error("please select a fruit to get information.")
    else:
        frutlyvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
        fruityvice_normalized = pd.json_normalize(frutlyvice_response.json())
        st.dataframe(fruityvice_normalized)
except URLError as e:
    st.error()
#st.write('The user entered ', fruit_choice)

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

# write your own comment -what does the next line do? 
#fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
#st.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
st.header("The fruit load list contains:")
st.dataframe(my_data_row)

add_my_fruit = st.text_input('What fruit would you like to add?','jackfruit')
st.write('Thanks for adding ', add_my_fruit)
my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('add_my_fruit+')")