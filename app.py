
### Importing libraries
import requests
import pandas as pd
import streamlit as st

## Definning API and connections
RICK_AND_MORTY_API = 'https://rickandmortyapi.com/api/character/'

def get_data():
    try:
        response = requests.get(RICK_AND_MORTY_API)
        response.raise_for_status()
        data = response.json().get('results', [])
        df = pd.DataFrame(data)
        
### Data Cleaning

        df['origin'] = df['origin'].apply(lambda x: x['name'] if isinstance(x, dict) else 'unknown')
        df['location'] = df['location'].apply(lambda x: x['name'] if isinstance(x, dict) else 'unknown')
        df['type'] = df['type'].replace('', pd.NA)
        return df
    except requests.exceptions.RequestException as e:
        st.error(f'Error at getting data: {e}')
        return pd.DataFrame()

# Load data
df_ = get_data()


### Definning the dashboard
def main():
    st.title('Dashboard Rick and Morty')

    if not df_.empty:
        # Sidebar filters
        status_filter = st.sidebar.multiselect('Filter by Status', df_['status'].unique(), df_['status'].unique())
        gender_filter = st.sidebar.multiselect('Filter by Gender', df_['gender'].unique(), df_['gender'].unique())
        species_filter = st.sidebar.multiselect('Filter by Species', df_['species'].unique(), df_['species'].unique())

        # Apply filters correctly
        filtered_df = df_[
            (df_['status'].isin(status_filter)) &
            (df_['gender'].isin(gender_filter)) &
            (df_['species'].isin(species_filter))
        ]

        # Display filtered data
        st.write("Character Data")
        st.dataframe(filtered_df[['id', 'name', 'status', 'species', 'gender', 'origin', 'location']])
    else:
        st.write("No data available.")

if __name__ == '__main__':
    main()