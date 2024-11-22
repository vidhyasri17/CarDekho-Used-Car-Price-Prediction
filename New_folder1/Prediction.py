import streamlit as st
from streamlit_extras.let_it_rain import rain
from streamlit_extras.colored_header import colored_header
import pandas as pd
import pickle

def app():
    colored_header(
        label='Welcome to Data :red[Prediction] page 👋🏼',
        color_name='red-70',
        description='CarDekho Used Cars Price Prediction'
    )

    @st.cache_data
    def load_data():
        df = pd.read_csv('Cleaned_Car_Dheko.csv')
        df1 = pd.read_csv('Preprocessed_Car_Dheko.csv')
        return df, df1
    
    df, df1 = load_data()

    # Drop unnecessary columns
    cols_to_drop = ['Manufactured_By', 'No_of_Seats', 'No_of_Owners', 'Fuel_Type', 'Registration_Year', 'Car_Age']
    df.drop(cols_to_drop, axis=1, inplace=True)
    df1.drop(cols_to_drop, axis=1, inplace=True)

    # Encode categorical variables
    encoding_dicts = {}
    for col in df.select_dtypes(include='object').columns:
        unique_values = df[col].sort_values().unique()
        encoding_dict = dict(zip(unique_values, range(len(unique_values))))
        encoding_dicts[col] = encoding_dict

    # Define function to apply inverse transformation
    def inv_trans(x):
        return 1 / x if x != 0 else 0

    # Streamlit form
    with st.form(key='form', clear_on_submit=False):
        car_model = st.selectbox(
            "**Select a Car Model**",
            options=df['Car_Model'].unique()
        )
        
        model_year = st.selectbox(
            "**Select a Car Produced Year**",
            options=df['Car_Produced_Year'].unique()
        )
        
        transmission = st.radio(
            "**Select a Transmission Type**",
            options=df['Transmission_Type'].unique(),
            horizontal=True
        )

        location = st.selectbox(
            "**Select a Location**",
            options=df['Location'].unique()
        )

        km_driven = st.number_input(
            f"**Enter Kilometers Driven (Min: {df['Kilometers_Driven'].min()}, Max: {df['Kilometers_Driven'].max()})**",
            min_value=float(df['Kilometers_Driven'].min()), 
            max_value=float(df['Kilometers_Driven'].max())
        )

        engine_cc = st.number_input(
            f"**Enter Engine CC (Min: {df['Engine_CC'].min()}, Max: {df['Engine_CC'].max()})**",
            min_value=float(df['Engine_CC'].min()), 
            max_value=float(df['Engine_CC'].max())
        )

        mileage = st.number_input(
            f"**Enter Mileage (Min: {df['Mileage(kmpl)'].min()}, Max: {df['Mileage(kmpl)'].max()})**",
            min_value=float(df['Mileage(kmpl)'].min()), 
            max_value=float(df['Mileage(kmpl)'].max())
        )

        button = st.form_submit_button('**Predict**', use_container_width=True)

        if button:
            try:
                # Prepare input data for prediction
                features = [
                    inv_trans(km_driven), 
                    encoding_dicts['Transmission_Type'][transmission],
                    encoding_dicts['Car_Model'][car_model],
                    model_year,
                    engine_cc,
                    mileage,
                    encoding_dicts['Location'][location]
                ]

                # Load model and predict
                with open('GradientBoost_model.pkl', 'rb') as file:
                    model = pickle.load(file)

                result = model.predict([features])
                st.markdown(f"## :green[*Predicted Car Price is {result[0]:,.2f}*]")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    app()
