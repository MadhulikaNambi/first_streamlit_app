import  streamlit
import urllib.error
from urllib.error import URLError
streamlit.title('My parents healthy new diner')
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include  
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected] 

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

import requests
from urllib.error import URLError

# Rest of your code...
# write your own comment -what does the next line do? 
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
#streamlit.dataframe(fruityvice_normalized)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized                                    
streamlit.header("Fruityvice Fruit Advice!")
                                                                  
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please enter a fruit to get info')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)  
    streamlit.dataframe(back_from_function)
except URLError as e:
     streamlit.error()  
       
        
streamlit.text(fruityvice_response)
streamlit.write('The user entered ', fruit_choice)

import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("fruit load list contains:")
streamlit.dataframe(my_data_rows)

fruit_choice = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', fruit_choice)

my_cur.execute("insert into fruit_load_list values('from streamlit')");



                                  
                                       
streamlit. header ("The fruit load list contains:")
#Snowflake-related functions 
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load list")
        return my_cur.fetchall ()
# Add a button to load the fruit
if streamlit. button( 'Get Fruit Load List'):
    my_cnx = snowflake. connector.connect (**streamlit.secrets ["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe (my_data_rows)                                                                                                              
                                                             
                                                              
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('from streamlit')")
        return "Thanks for adding " + new_fruit
                        
                        
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets ["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text (back_from_function)