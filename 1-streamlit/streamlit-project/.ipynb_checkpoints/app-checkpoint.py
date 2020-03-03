import streamlit as st

# Text/Title 

# Header/Subheader

st.title("What makes a restaurant successful?")
st.header("Key Points")
st.subheader("First, have good food.")

st.text("Of all of the factors, quality of food displayed proved to be the most important factor.")


st.success("Restaurants with good food.")
st.info("Notice that price did not appear to play a role")
st.warning("But with excessive price can come angry customers.")

st.subheader("Top restaurants")
employees = ['moes', 'selmas', 'pats']
for employee in employees:
    st.markdown(f'* {employee}')

customers = ['bob', 'fred', 'sam']
for customer in customers:
    if customer.startswith('f'):
        st.write(customer)
        
        
names = ['fred', 'sam', 'sally']
text_input = ""
search_name = st.text_input("")
if st.button("Search"):
    search_name = search_name
if st.button("Clear"):
    search_name = ""
if search_name:
    names = [name for name in names if name.startswith(search_name)]
for name in names:
    st.markdown(f'* {name}')

    
status = st.radio("what is the status", ("active", "inactive"))
st.write("This is your status", status)
occupation = st.selectbox("Your occupation", ["Programmer", "Data Scientist", "Businessman"])
st.write("You selected this option", occupation)
locations = st.multiselect("Where do you work", ("London", "New York", "Accra"))
for location in locations:
    st.markdown(f'* {location}')