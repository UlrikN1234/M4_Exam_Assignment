# Import necessary libraries
import pandas as pd

def load_data():
    # Read Excel file
    file_path = 'C:\\Users\\Bruger\\OneDrive\\Skrivebord\\Data_butikker.xlsx'
    df_raw = pd.read_excel(file_path)

    # View the first 5 rows of the data
    print(df_raw.head())

    # Convert 'Dato' column to datetime format (assuming it's in 'dd-mm-yyyy' format)
    df_raw['Dato'] = pd.to_datetime(df_raw['Dato'], format='%d-%m-%Y')

    # Convert 'Tidspunkt' to string format 'HH:MM:SS'
    df_raw['Tidspunkt'] = df_raw['Tidspunkt'].astype(str)

    # Combine 'Dato' and 'Tidspunkt' columns to create a single 'Datetime' column
    df_raw['Dato'] = pd.to_datetime(df_raw['Dato'].astype(str) + ' ' + df_raw['Tidspunkt'], format='%Y-%m-%d %H:%M:%S')

    # Group the data by Hændelses-ID and aggregate the necessary columns
    df_raw = df_raw.groupby('Hændelses-ID').first().reset_index()

    # Replace missing values in 'Antal Tyve' with 1
    df_raw['Antal tyve'] = df_raw['Antal tyve'].fillna(1)

    # Make a column drop list
    columns_to_drop = [
        'Tidspunkt','Kategori-ID', 'Kategori', 'Vare', 'Antal', 'Stykpris', 'Samlet pris for alle varer', 
        'Samlet erstatningskrav for varer', 'Erstatningskrav udover varen', 'Samlet erstatningskrav', 
        'Varesikringsalarm aktiveret?', 'Politikreds', 
        'Forurettede ønsker, at erstatningskravet medtages i straffesagen', 
        'Forurettede ønsker at frafalde erstatningskravet og ønsker beløbet lagt oven i bøden', 
        'Ombytning af prismærker', 'Uddybelse af tricktyveri', 'Uddybelse af truende adfærd', 
        'Uddybelse af tidligere forhold', 
        'Blev gerningspersonen antruffet/tilbageholdt efter sidste betalingsmulighed eller uden for butikken?', 
        'Der er brugbar videoovervågning, hvor man kan se tyven og/eller tyveriet'
    ]

    # Drop columns from the drop list
    df = df_raw.drop(columns=columns_to_drop)


    # View the first 5 rows of the data 
    print(df.head())

    return df