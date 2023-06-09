import streamlit
import urllib.error
import pandas
import requests
import snowflake.connector

streamlit.title('My parents healthy new diner')
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

# Rest of your code...
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?', key='fruit_info_input')
    if not fruit_choice:
        streamlit.error('Please enter a fruit to get info')
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except urllib.error.URLError as e:
    streamlit.error('An error occurred')

streamlit.write('The user entered', fruit_choice)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("fruit load list contains:")
streamlit.dataframe(my_data_rows)

fruit_choice = streamlit.text_input('What fruit would you like to add?', key='add_fruit_input')
streamlit.write('Thanks for adding', fruit_choice)

my_cur.execute("insert into fruit_load_list values (:fruit)", {"fruit": fruit_choice})

# Add additional fruits to the list
fruits_to_add = ['jackfruit', 'papaya', 'guava', 'kiwi']
for fruit in fruits_to_add:
    my_cur.execute("insert into fruit_load_list values (?)", (fruit,))

streamlit.header("The fruit load list contains:")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

if streamlit.button('Get Fruit List', key='get_fruit_list_button'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values (?)", (new_fruit,))
        return "Thanks for adding " + new_fruit
    
add_my_fruit = streamlit.text_input('What fruit would you like to add?', key='add_fruit_input')
if streamlit.button('Add a Fruit to the List', key='add_fruit_button'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)
