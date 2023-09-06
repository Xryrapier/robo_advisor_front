import streamlit as st
import pandas as pd
import numpy as np
import os
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

age = st.slider('Age', min_value=features['AGE']['min'], max_value=features['AGE']['max'])
gender = st.radio("Gender", ["Male", "Female"])
marital_status = st.radio("Marital status", ["Married" , "Not married"])
kids = st.slider('Number of children', min_value=0, max_value=9)

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

net_worth = st.text_input('Networth')
income = st.text_input('Monthly income')

savings_dict = {
    'Have debts': 1,
    'No saving, no debt': 2,
    'Have savings': 3,
}
savings = st.selectbox("Savings", [""] + list(savings_dict.keys()), index=0)

risk_willingness = st.checkbox("Are you willing to take risk?")

amount=st.text_input('Investment amount')
n_days=st.text_input('Investment period')
# Define dictionaries for gender and savings
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

# Calculate x_pred_data based on user inputs




submit_button = st.button('Find my best portfolio and risk ', key='submit-asset_alloc_button' )
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


    robo_advisor_api_url = 'https://eficientfrontier-wjqgur6ida-ew.a.run.app/predict'
    response = requests.get(robo_advisor_api_url, params=x_pred_data)
    prediction = response.json()

    fin_pd=pd.DataFrame(prediction["fin_pd"])
    sigma =np.round(prediction["sigma"][0]*100,2)
    st.text_input('Risk tolerance (Scale of 100)', value=sigma, key='risk_tolerance_input')


    st.markdown('#### Asset Allocation and Portfolio Performance')
    ticker_symbols = st.multiselect('Best assets for the portfolio', options=fin_pd["Ticker"] , default=fin_pd["Ticker"])
    st.bar_chart(fin_pd.set_index('Ticker')['Number of actions'] ,  width=300 ,height=270,color="#ff4b4b")
