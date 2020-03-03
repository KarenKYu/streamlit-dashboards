import streamlit as st
import sqlite3
conn = sqlite3.connect('./special_moes.db')
cursor = conn.cursor()

def customers(bartender_name):
    moes_customers = """select DISTINCT(customers.name) from customers join orders on orders.customer_id = customers.id join bartenders on bartenders.id = orders.bartender_id where bartenders.name = ?"""
    cursor.execute(moes_customers,(bartender_name,))
    results = cursor.fetchall()
    return [result[0] for result in results]

def bartenders():
    all_bartenders = 'SELECT name FROM bartenders'
    cursor.execute(all_bartenders)
    results = cursor.fetchall()
    return [result[0] for result in results]
bartender_name = st.selectbox("Bartender", bartenders())

customer_names = ' '.join(customers(bartender_name))
st.write(customer_names)