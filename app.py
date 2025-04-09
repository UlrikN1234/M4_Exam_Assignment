# Frontend made in streamlit which allows users to input their specifics to be able predict if a theft is happening in their area today.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from EDA import load_data  
from duckduckgo_search import DDGS

# Load the data
df = load_data()

# Streamlit app title
st.title("Shoplifting Incident Dashboard")

st.markdown("""
            Welcome to the Shoplifting Incident Dashboard. As efforts to reduce retail crime continue to evolve, understanding the factors behind theft incidents is crucial. This interactive dashboard leverages data analytics to provide insights into theft patterns, store types, time-of-day trends, and regional disparities. By analyzing these trends, we aim to offer actionable strategies for reducing losses and enhancing security measures in retail environments.
""")

with st.expander("📊 **Objective**"):
    st.markdown("""
At the core of this dashboard is the mission to visually analyze shoplifting data, enabling stakeholders to gain insights into key trends such as:
- Which regions and store types are most affected by shoplifting incidents?
- What times of day see the highest frequency of thefts?
- What patterns emerge in the demographics of offenders involved in retail theft?
- Based on observed trends, what strategies can be implemented to reduce theft and improve store security?

This dashboard aims to uncover underlying patterns, providing actionable insights to reduce losses and optimize store operations.
""")
    
visualization_option = st.selectbox(
    "Select Visualization 🎨", 
    ["Number of Thefts per Month",
     "Number of Thefts per Weekday", 
     "Number of Thefts per Time of Day", 
     "Number of Thefts per Store",
     "Number of Thefts per Organization",
     "Number of Thefts Reported to the Police",
     "Distribution of Perpetrators' Gender",
     "Distribution of Total Theft Amount", 
     "Distribution of Number of Thieves per Incident", 
     "Distribution of Trick Theft"
     ]
)


if visualization_option == "Number of Thefts per Month":
    st.header("Number of Thefts per Month")
    st.markdown("""This visualization shows the number of thefts that occurred each month. 
    It's useful for identifying seasonal trends and spotting increases or decreases over time.""")

    fig, ax = plt.subplots(figsize=(12, 6))
    df.groupby(df['Dato'].dt.to_period("M")).size().plot(kind='line', ax=ax)
    ax.set_xlim([pd.Timestamp('2020-01-01').to_period('M'), pd.Timestamp('2025-12-31').to_period('M')])
    ax.set_title('Number of Thefts per Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Thefts')
    ax.grid(True)
    st.pyplot(fig)

    if st.button("Please explain the monthly trend of thefts"):
        with st.expander("AI Explanation"):
            monthly_df = df.groupby(df['Dato'].dt.to_period("M")).size()
            st.markdown(DDGS().chat(
                "You are a very intelligent Data Analyst: Please explain the monthly trend of thefts based on this: " + str(monthly_df.describe()), 
                model="gpt-4o-mini"))

# --- Theft frequency per weekday ---
elif visualization_option == "Number of Thefts per Weekday":
    st.header("Thefts per Weekday")
    st.markdown("This chart shows how theft incidents are distributed across the days of the week.")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='Ugedag', data=df, order=df['Ugedag'].value_counts().index, ax=ax)
    ax.set_title('Number of Thefts per Weekday')
    ax.set_xlabel('Weekday')
    ax.set_ylabel('Number of Thefts')
    st.pyplot(fig)

    if st.button("Please explain the weekday distribution of thefts"):
        with st.expander("AI Explanation"):
            weekday_counts = df['Ugedag'].value_counts()
            st.markdown(DDGS().chat(
                "You are a very intelligent Data Analyst: Please explain the distribution of thefts across weekdays: " + str(weekday_counts.describe()), 
                model="gpt-4o-mini"))
            
# --- Theft frequency per hour of day ---
elif visualization_option == "Number of Thefts per Time of Day":
    st.header("Thefts by Hour of Day")
    st.markdown("This chart shows the number of thefts by hour, helping identify peak times for incidents.")

    df['Hour of Day'] = df['Dato'].dt.hour
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='Hour of Day', data=df, hue='Hour of Day', palette='viridis', legend=False, ax=ax)
    ax.set_title('Number of Thefts per Time of Day')
    ax.set_xlabel('Time of Day (Hour)')
    ax.set_ylabel('Number of Thefts')
    ax.set_xticks(range(0, 24))
    st.pyplot(fig)

    if st.button("Please explain the hourly distribution of thefts"):
        with st.expander("AI Explanation"):
            hour_counts = df['Hour of Day'].value_counts()
            st.markdown(DDGS().chat(
                "You are a very intelligent Data Analyst: Please analyze this hourly theft distribution: " + str(hour_counts.describe()), 
                model="gpt-4o-mini"))

# --- Thefts per store ---
elif visualization_option == "Number of Thefts per Store":
    st.header("Thefts per Store")
    st.markdown("This chart visualizes the number of thefts reported by each store location.")

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.countplot(y='Butik', data=df, order=df['Butik'].value_counts().index, ax=ax)
    ax.set_title('Number of Thefts per Store')
    ax.set_xlabel('Number of Thefts')
    ax.set_ylabel('Store')
    st.pyplot(fig)

    if st.button("Please explain thefts per store"):
        with st.expander("AI Explanation"):
            store_counts = df['Butik'].value_counts()
            st.markdown(DDGS().chat(
                "You are a very intelligent Data Analyst: Analyze the store-level theft distribution: " + str(store_counts.describe()), 
                model="gpt-4o-mini"))

# --- Thefts per organization ---
elif visualization_option == "Number of Thefts per Organization":
    st.header("Thefts per Organization")
    st.markdown("This chart shows the number of thefts reported by each organization.")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(y='Organisation', data=df, order=df['Organisation'].value_counts().index, ax=ax)
    ax.set_title('Number of Thefts per Organization')
    ax.set_xlabel('Number of Thefts')
    ax.set_ylabel('Organization')
    st.pyplot(fig)

    if st.button("Please explain the organization theft chart"):
        with st.expander("AI Explanation"):
            org_counts = df['Organisation'].value_counts()
            st.markdown(DDGS().chat(
                "You are a very intelligent Data Analyst: Interpret the thefts by organization: " + str(org_counts.describe()), 
                model="gpt-4o-mini"))

# --- Reported to police ---
elif visualization_option == "Number of Thefts Reported to the Police":
    st.header("Reported to Police")
    st.markdown("This chart shows whether thefts were reported to the police. It helps understand how frequently incidents are escalated to law enforcement.")

    fig6, ax6 = plt.subplots(figsize=(10, 6))
    sns.countplot(x='Anmeldt til Politiet', data=df, ax=ax6)
    ax6.set_title('Number of Thefts Reported to the Police')
    ax6.set_xlabel('Reported to Police')
    ax6.set_ylabel('Number of Incidents')
    st.pyplot(fig6)

    if st.button("Please explain the reporting behavior"):
        with st.expander("AI Explanation"):
            report_counts = df['Anmeldt til Politiet'].value_counts()
            st.markdown(DDGS().chat(
                "You are a very intelligent Data Analyst: Analyze the reporting behavior to the police: " + str(report_counts.describe()), 
                model="gpt-4o-mini"))

# --- Perpetrator gender ---
elif visualization_option == "Distribution of Perpetrators' Gender":
    st.header("Perpetrator Gender")
    st.markdown("This chart shows the distribution of genders among the identified perpetrators.")

    fig7, ax7 = plt.subplots(figsize=(10, 6))
    sns.countplot(x='Gerningsperson 1 køn', data=df, ax=ax7)
    ax7.set_title("Distribution of Perpetrators' Gender")
    ax7.set_xlabel('Gender')
    ax7.set_ylabel('Number of Perpetrators')
    st.pyplot(fig7)

    if st.button("Please explain the gender distribution"):
        with st.expander("AI Explanation"):
            gender_counts = df['Gerningsperson 1 køn'].value_counts()
            st.markdown(DDGS().chat(
                "You are a very intelligent Data Analyst: Analyze the gender distribution of perpetrators: " + str(gender_counts.describe()), 
                model="gpt-4o-mini"))

# --- Total theft amount distribution ---
elif visualization_option == "Distribution of Total Theft Amount":
    st.header("Total Theft Amount Distribution")
    st.markdown("This histogram shows the distribution of the total price/value involved in each theft. It helps identify how large or small most incidents are.")

    fig8, ax8 = plt.subplots(figsize=(10, 6))
    sns.histplot(df['Samlet pris'], bins=20, kde=True, ax=ax8)
    ax8.set_title('Distribution of Total Theft Amount')
    ax8.set_xlabel('Total Price')
    ax8.set_ylabel('Frequency')
    st.pyplot(fig8)

    if st.button("Please explain the price distribution"):
        with st.expander("AI Explanation"):
            price_stats = df['Samlet pris'].describe()
            st.markdown(DDGS().chat(
                "You are a very intelligent Data Analyst: Analyze the distribution of theft amounts: " + str(price_stats), 
                model="gpt-4o-mini"))
            
# --- Number of thieves per incident ---
elif visualization_option == "Distribution of Number of Thieves per Incident":
    st.header("Number of Thieves per Incident")
    st.markdown("This chart shows how many thieves were typically involved in each incident.")

    fig9, ax9 = plt.subplots(figsize=(10, 6))
    sns.histplot(df['Antal tyve'], bins=10, kde=False, ax=ax9)
    ax9.set_title('Distribution of Number of Thieves per Incident')
    ax9.set_xlabel('Number of Thieves')
    ax9.set_ylabel('Frequency')
    st.pyplot(fig9)

    if st.button("Please explain the number of thieves per incident"):
        with st.expander("AI Explanation"):
            thief_stats = df['Antal tyve'].describe()
            st.markdown(DDGS().chat(
                "You are a very intelligent Data Analyst: Analyze the distribution of the number of thieves per incident: " + str(thief_stats), 
                model="gpt-4o-mini"))

# --- Trick thefts ---
elif visualization_option == "Distribution of Trick Thef":
    st.header("Trick Theft Distribution")
    st.markdown("This chart shows the number of thefts classified as 'trick thefts' versus others.")

    fig10, ax10 = plt.subplots(figsize=(10, 6))
    sns.countplot(x='Tricktyveri', data=df, ax=ax10)
    ax10.set_title('Distribution of Trick Theft')
    ax10.set_xlabel('Trick Theft')
    ax10.set_ylabel('Number of Incidents')
    st.pyplot(fig10)

    if st.button("Please explain trick theft data"):
        with st.expander("AI Explanation"):
            trick_counts = df['Tricktyveri'].value_counts()
            st.markdown(DDGS().chat(
                "You are a very intelligent Data Analyst: Analyze the distribution of trick thefts: " + str(trick_counts.describe()), 
                model="gpt-4o-mini"))

# Instructions
st.markdown("""
Choose the day of the week and the postal code of your store
""")

# Create a dropdown for the day of the week ("Ugedag")
day_of_week = st.selectbox(
    "Select the day of the week",
    df['Ugedag'].unique()
)

# Create a dropdown for the postal code ("Postnummer")
postal_code = st.selectbox(
    "Select your store's postal code",
    df['Postnummer'].unique()
)

# Display the selected values
st.write(f"You selected {day_of_week} for the day of the week and {postal_code} for the postal code. Press the button below to see if an incident happens in your area today")

# Button to run the model
st.button("Run Shoplifting Predictor")