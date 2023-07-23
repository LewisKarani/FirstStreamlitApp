import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)


@st.cache_data
def load_data():
    file_path = r'C:\Users\HP\Data Science\Pandas/all_data_cleaned.csv'
    data = pd.read_csv(file_path)
    data.groupby('Month').sum()
    data.groupby(['City']).sum()
    data.groupby(['Hour'])
    
    return data
data = load_data()

st.title("End to end analysis project")
st.write("This app analyzes the all_sales data and visualizations.")

with st.sidebar:
    selected = option_menu(
        menu_title = "Options Menu",
        options = ["Home", "Best Sales Month", "Best Sales City", "Best Time For Sales", "Products that sold together", "Most Sold Product"]
    )

if selected == "Home":
    st.title("General Info")
    if st.checkbox("Show Raw Data"):
       st.subheader("Raw Data")
       st.write(data)
if selected == "Best Sales Month":
    st.title("Representation for the month that had the most sales.")
    Best_sales_month, Graphical_rep_for_month_sales = st.columns(2)
    with Best_sales_month:
       best_month_for_sales = data.groupby('Month').sum()
       st.write(best_month_for_sales)
    with Graphical_rep_for_month_sales:
        months = range(1,13)
        fig1 = px.bar(x=best_month_for_sales.index, y=best_month_for_sales['Sales'],
                  labels={'x': 'Month number', 'y': 'Sales in USD'},
                  title='Monthly Sales Analysis')
        st.plotly_chart(fig1)

if selected == "Best Sales City":
    st.title("Best Seller city Representation")
    Col1, Col2 = st.columns(2)
    with Col1:
        best_seller = data.groupby(['City']).sum()
        st.write(best_seller)
    with Col2:
        cities = data.groupby(['City'])
        keys = [city for city, df in cities]
        fig2 = px.bar(x=keys, y=data.groupby(['City']).sum()['Sales'],
                      labels={'x': 'Month Number', 'y': 'Sales in USD ($)'},
                      title= 'Best seller City'
                      )
        st.plotly_chart(fig2)

if selected == "Best Time For Sales":
    st.title("Representation for how many sales were done along the time stamp")
    keys = [pair for pair, df in data.groupby(['Hour'])]
    plt.plot(keys, data.groupby(['Hour']).count()['Count'])
    plt.xticks(keys)
    plt.xlabel("Time Stamp")
    plt.ylabel("Sales per unit time")
    plt.title("Total sales per unit time")
    plt.grid()
    plt.show()
    st.pyplot()

if selected == "Products that sold together":
    df=data[data['Order ID'].duplicated(keep=False)]
    df['Grouped']=df.groupby('Order ID')['Product'].transform(lambda x:','.join(x))
    df=df[['Order ID','Grouped']].drop_duplicates()
    
    from itertools import combinations
    from collections import Counter

    count =Counter()

    for row in df['Grouped']:
       row_list =row.split(',')
       count.update(Counter(combinations(row_list, 2)))
    
    sold_together = count.most_common(10)
    st.table(sold_together)

if selected == "Most Sold Product":
    st.subheader("Bar plot for the most sold product data")
    
    product_group = data.groupby('Product')
    quantity_ordered = product_group.sum()['Quantity Ordered']
    keys = [pair for pair, df in product_group]
    plt.bar(keys, quantity_ordered)
    plt.xticks(keys, rotation='vertical', size=8)
    plt.xlabel("Product")
    plt.ylabel("Total Sales")
    plt.show()
    st.pyplot()

    st.subheader("Combined bar and line graph for the most sold product data")
    prices = data.groupby('Product').mean()['Price Each']

    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax1.bar(keys, quantity_ordered, color='g')
    ax2.plot(keys, prices, color='b')

    ax1.set_xlabel('Product Name')
    ax1.set_ylabel('Quantity Ordered', color='g')
    ax2.set_ylabel('Price ($)', color='b')
    ax1.set_xticklabels(keys, rotation='vertical', size=8)

    fig.show()
    st.pyplot()

    
