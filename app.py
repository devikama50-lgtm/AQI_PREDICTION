import streamlit as st
import requests


st.set_page_config(page_title="AQI Checker",page_icon="🌍")

API_URL = "http://127.0.0.1:8000"

st.title("🌍 AQI Checker")

st.subheader("Location-Based AQI Prediction with Historical Environmental Data")

# ui customization
st.markdown("""
<style>

/* Background */
.stApp {
background-color: #DFF3FA;
}

/* ALL headings */
h1, h2, h3, h4 {

color: #123B4A !important;
}

/* Title */
.stTitle {
    color: #123B4A !important;
}

/* Normal text */
p {
    color: #123B4A !important;
}

/* Selectbox label */
label {
    color: #123B4A !important;
}

/* Selectbox */
div[data-baseweb="select"] {
    background-color: white !important;
    border-radius: 8px;
}

div[data-baseweb="select"] span {
    color: #123B4A !important;
}

/* Button */
.stButton > button {
    width: 100%;
    height: 45px;
    border-radius: 8px;
    background-color: #8CCFE3 !important;
    color: #123B4A !important;
    font-size: 16px;
    font-weight: 600;
    border: none;
}

/* Metric boxes */
div[data-testid="stMetric"] {
    background-color: white !important;
    padding: 15px !important;
    border-radius: 10px !important;
    border: 1px solid #B8DCE7 !important;
}

/* Feature names */
div[data-testid="stMetricLabel"] {
    color: #123B4A !important;
}

div[data-testid="stMetricLabel"] p {
    color: #123B4A !important;
    font-weight: 600 !important;
}

/* Feature values */
div[data-testid="stMetricValue"] {
    color: #123B4A !important;
}

div[data-testid="stMetricValue"] div {
    color: #123B4A !important;
}

/* Warning and error text */
div[data-testid="stAlert"] {
    color: #123B4A !important;
}

</style>
""", unsafe_allow_html=True)


# Gets locations from FastAPI
try:
    response = requests.get(f"{API_URL}/locations")

    locations = response.json()["locations"]

except:
    st.error("FastAPI server is not running.")
    st.stop()



selected_city = st.selectbox("📍 Select Location",["Choose location"] + locations)



if st.button("🔍 Check AQI"):

    if selected_city == "Choose location":

        st.warning("Please choose a location.")

    else:

        response = requests.get(
            f"{API_URL}/predict/{selected_city}"
        )

        if response.status_code == 200:

            result = response.json()


            

            st.header("AQI Prediction")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Predicted AQI",
                    result["predicted_aqi"]
                )

            with col2:
                st.metric(
                    "Category",
                    result["category"]
                )

            st.header("Average Environmental Conditions")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "PM2.5",
                    f'{result["pm25"]} µg/m³'
                )

                st.metric(
                    "PM10",
                    f'{result["pm10"]} µg/m³'
                )

                st.metric(
                    "NO₂",
                    f'{result["no2"]} µg/m³'
                )


            with col2:

                st.metric(
                    "SO₂",
                    f'{result["so2"]} µg/m³'
                )

                st.metric(
                    "O₃",
                    f'{result["o3"]} µg/m³'
                )

                st.metric(
                    "CO",
                    f'{result["co"]} mg/m³'
                )


            with col3:

                st.metric(
                    "Temperature",
                    f'{result["temperature"]} °C'
                )

                st.metric(
                    "Humidity",
                    f'{result["humidity"]} %'
                )

                st.metric(
                    "Wind Speed",
                    f'{result["wind_speed"]} m/s'
                )


        else:

            st.error(
                response.json()["detail"]
            )