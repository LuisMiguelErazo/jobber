import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Load the data into a DataFrame
df = pd.read_csv('df.csv')

# Custom sorting function to sort alphabetically with numbers at the end
def custom_sort(values):
    alpha_part = sorted([v for v in values if not re.match(r'^\d', v)])
    numeric_part = sorted([v for v in values if re.match(r'^\d', v)])
    return alpha_part + numeric_part

# Ensure the category and title options are sorted using the custom sorting function
sorted_categories = custom_sort(df['category'].unique())
sorted_titles = custom_sort(df['title'].unique())

# Streamlit app
st.title('Job Salary Explorer')

# Create dropdowns
selected_category = st.selectbox('Select Category:', sorted_categories)
filtered_titles = custom_sort(df[df['category'] == selected_category]['title'].unique())
selected_title = st.selectbox('Select Title:', filtered_titles)

# Function to show salaries and plot
def show_salaries(category, title):
    filtered_df = df[(df['category'] == category) & (df['title'] == title)]
    
    if filtered_df.empty:
        st.write("No data found for the provided category and title.")
        return

    max_salary = filtered_df['max_annual_salary'].values[0]
    med_salary = filtered_df['med_annual_salary'].values[0]
    min_salary = filtered_df['min_annual_salary'].values[0]

    st.write(f"Salaries for {title} in the {category} category:")
    st.write(f"Max Annual Salary: {max_salary}")
    st.write(f"Median Annual Salary: {med_salary}")
    st.write(f"Min Annual Salary: {min_salary}")

    salaries = [min_salary, med_salary, max_salary]
    salary_labels = ['Min Annual Salary', 'Median Annual Salary', 'Max Annual Salary']

    norm_salaries = (salaries - np.min(salaries)) / (np.max(salaries) - np.min(salaries))
    scaled_norm_salaries = 0.3 + 0.7 * norm_salaries
    colors = plt.cm.Blues(scaled_norm_salaries)

    fig, ax = plt.subplots()
    bars = ax.bar(salary_labels, salaries, color=colors)
    ax.set_xlabel('Salary Type')
    ax.set_ylabel('Annual Salary')
    ax.set_title(f'Salary Ranges for {title} in {category}')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom')

    st.pyplot(fig)

# Button to trigger the salary display
if st.button('Show Salaries'):
    show_salaries(selected_category, selected_title)
