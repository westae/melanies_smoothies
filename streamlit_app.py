# use 4-spaces instead of a Tab, for when we try this in Streamlit OG

# Import python packages
import streamlit as st
import requests  # Moved this up to the top (Lesson 62)
#from snowflake.snowpark.context import get_active_session -- removed when moving out of Snowflake
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

import streamlit as st

smoothiefroot_response = requests.get('https://my.smoothiefroot.com/api/fruit/watermelon')  
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

name_on_order = st.text_input("Name on your Smoothie:")
st.write("The name on your Smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True) 

# My attempt to make this work:
ingredient_list = st.multiselect(
    "Choose up to 5 ingredients"
    , my_dataframe
    , max_selections=5
    )

# st.write("You selected:", options)
if ingredient_list: # which means when the list is null, do everything below this line that is indented.
    ingredients_string = ''
    #st.write(ingredient_list)
    #st.text(ingredient_list)

    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)
    #st.stop() # halts execution for troubleshooting.  Stop here before we write to db
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert: # which means when the list is null, do everything below this line that is indented.
        session.sql(my_insert_stmt).collect()    
    
#    if ingredients_string:
#        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!  ' + name_on_order, icon="✅")
    
