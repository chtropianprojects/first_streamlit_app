import streamlit 
import snowflake.connector
import pandas
import requests
import urllib.error as URLError

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')









my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado","Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page.

streamlit.dataframe(fruits_to_show)

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
streamlit.header("Fruityvice Fruit Advice!")
#streamlit.text(fruityvice_response.json())
# create a table from json file
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# print the table 
streamlit.dataframe(fruityvice_normalized)



streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_rows = my_cur.fetchall()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()

my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()

streamlit.header("List of products")
third_choice = streamlit.text_input('What fruit would you like information about? (connection with sql)','banana')
my_cur.execute(f"select * from pc_rivery_db.public.fruit_load_list where Fruit_name='{third_choice}'")
my_data_rows = my_cur.fetchall()
streamlit.dataframe(my_data_rows)
streamlit.write('thanks for adding',third_choice)
my_cur.execute(f"insert into PC_RIVERY_DB.PUBLIC.fruit_load_list values('fromstreamlight')")

