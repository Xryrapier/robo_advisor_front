import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import requests
import time



features = {
    'HHSEX': {'female': 0, 'male': 1},
    'AGE': {'min': 17, 'max': 95},
    'EDCL': {'no high school diploma': 1, 'high school diploma': 2, 'some college': 3, 'college degree': 4},
    'MARRIED': {'yes': 1, 'no': 0},
    'KIDS': {'min': 0},
    'FAMSTRUCT_1': {'not_married_with_children': 1, 'else': 0},
    'FAMSTRUCT_2': {'not_married_no_children_under_55': 1, 'else': 0},
    'FAMSTRUCT_3': {'not_married_no_children_head_55': 1, 'else': 0},
    'FAMSTRUCT_4': {'married_with_children': 1, 'else': 0},
    'FAMSTRUCT_5': {'married_no_children': 1, 'else': 0},
    'OCCAT1': {'work_for_someone_else': 1, 'self_employed_or_partnership': 2, 'retired_or_disabled_and_student_homemaker_misc_not_working_and_age_65_or_older': 3, 'other_groups_not_working_under_65_and_out_of_the_labor_force': 4},
    'INCOME': {},
    'WSAVED': {'spending_exceeded_income': 1, 'spending_equaled_income': 2, 'spending_less_than-income': 3},
    'YESFINRISK': {'yes': 1, 'no': 0},
    'NETWORTH': {}
}






# Define the layout
st.title('Robo Advisor Dashboard')
st.markdown('### Enter Investor and Investment Characteristics')
st.markdown(
    """
    <style>
    .appview-container h1, .appview-container span, .appview-container label, .appview-container p, .appview-container {
      color: white !important;
    }

    .appview-container {
      background-image: url('https://4kwallpapers.com/images/wallpapers/purple-light-geometric-glowing-lines-minimalist-5k-5120x2880-6724.jpg');
      background-size: cover;
      background-repeat: no-repeat;
    }

    .row-widget.stButton {
      display: flex;
      justify-content: center;
      margin-top: 20px;
    }

    .row-widget.stButton > button {
        background-color: #a10000;
        color: white;
    }
    
    .row-widget.stRadio > div {
        flex-direction:row;

    span[data-baseweb=tag] {
        background-color: #02852b !important;
    }
    
     [theme]
    base="light"
    primaryColor="#a10000"
    
    </style>
    """,
    unsafe_allow_html=True
)

left, right = st.columns(2)

with left:
    age = st.slider('Age', min_value=features['AGE']['min'], max_value=features['AGE']['max'])
    gender = st.radio("Gender", ["Male", "Female"])
    marital_status = st.radio("Marital status", ["Married" , "Not married"])
    kids = st.slider('Number of children', min_value=0, max_value=9)
    risk_willingness = st.checkbox("Are you willing to take risk?")

with right:
    education_levels = {
        'No high school diploma': 1,
        'High school diploma': 2,
        'College in progress': 3,
        'College degree or higher': 4
    }
    education = st.selectbox("Education", [""] + list(education_levels.keys()), index=0)

    occupation_levels = {
        'Employee': 1,
        'Self-employed or partnership': 2,
        'Retired or disabled and +65': 3,
        'Student, homemaker, or not working -65': 4,
    }
    occupation = st.selectbox("Occupation", [""] + list(occupation_levels.keys()), index=0)

    savings_dict = {
        'Have debts': 1,
        'No saving, no debt': 2,
        'Have savings': 3,
    }
    savings = st.selectbox("Savings", [""] + list(savings_dict.keys()), index=0)

    net_worth = st.text_input('Networth')
    income = st.text_input('Monthly income')

    amount=st.text_input('Investment amount')
    n_days=st.text_input('Investment period')

    gender_dict = {
        'Male': 1,
        'Female': 2
    }
    marital_status_dict = {
        'Married': 0,
        'Not married': 1
    }

    if marital_status == "Not married":
        if kids !=0 :
            FAMSTRUCT=1
        else :
            if age <55:
                FAMSTRUCT=2
            else:
                FAMSTRUCT=3
    else:
        if kids!=0 :
            FAMSTRUCT=4
        else:
            FAMSTRUCT=5




submit_button = st.button('Find my best portfolio and risk ')

if submit_button:
    x_pred_data=dict(
    HHSEX= gender_dict.get(gender, 0),
    AGE=age,
    EDCL=education_levels.get(education, 0),
    MARRIED=marital_status_dict.get(marital_status, 0),
    KIDS=kids,

    FAMSTRUCT=FAMSTRUCT,
    OCCAT1=occupation_levels.get(occupation, 0),
    INCOME=float(income),
    WSAVED=savings_dict.get(savings, 0),
    YESFINRISK=int(risk_willingness),
    NETWORTH=float(net_worth))

    robo_advisor_api_url = 'https://eficientfrontierfinal-wjqgur6ida-ew.a.run.app/predict'
    response = requests.get(robo_advisor_api_url, params=x_pred_data)
    prediction = response.json()

    res=pd.DataFrame(prediction["res"])

    sigma =np.round(prediction["sigma"][0]*100,2)
    st.text_input('Risk tolerance (Scale of 100)', value=sigma, key='risk_tolerance_input')

    st.markdown('#### Asset Allocation and Portfolio Performance')
    st.multiselect('Best assets for the portfolio', options=res["Ticker"], default=res["Ticker"])

    res['Number of actions'] = res['Number of actions'].apply(lambda x: int(x))
    res.drop(columns = ['Weight'], inplace = True)


    fig, ax = plt.subplots(figsize=(3, 2))
    bars = ax.bar(res['Ticker'], res['Number of actions'], color="#02852b")
    ax.set_xlabel('Ticker', fontsize=5)
    ax.set_ylabel('Number of Stocks', fontsize=5)
    ax.tick_params(axis='both', which='major', labelsize=5)

    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=5)
    new_max_y = res['Number of actions'].max() + 20
    ax.set_ylim(0, new_max_y)

    st.pyplot(fig)
