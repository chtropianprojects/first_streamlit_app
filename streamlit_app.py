import streamlit 
import snowflake.connector
import pandas
import requests
from urllib.error import URLError

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


def get_fruity_data(fruit_choice):
  fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


def get_fruit_load_list():
  with my_cnx.cursor() as  my_cur:
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()
 

def insert_fruits(fruit):
   with my_cnx.cursor() as  my_cur:
    my_cur.execute(f"insert into PC_RIVERY_DB.PUBLIC.fruit_load_list values('{fruit}')")
    return f"Thanks for adding the fruit {fruit}"

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado","Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page.

streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit for informaitons")
  else:
   
    back_from_function=get_fruity_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()


streamlit.header("List of products")

if streamlit.button('get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

    
streamlit.header("Add a product in the list")  
third_choice = streamlit.text_input('What fruit would you like information about? (connection with sql)','banana')

if streamlit.button('Add a product'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    text_v = insert_fruits(third_choice)
    my_cnx.close()
    streamlit.write(text_v)


