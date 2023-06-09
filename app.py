import streamlit as st
import pickle
import numpy as np
import base64

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return
set_png_as_page_bg('true.png')


classifier_name=['XGBoost Classifier']
option = st.sidebar.selectbox('Model selected', classifier_name)
st.subheader(option)



#Importing model and label encoders
model=pickle.load(open("final_xg_model.pkl","rb"))
#model_1 = pickle.load(open("final_rf_model.pkl","rb"))
le_pik=pickle.load(open("label_encoding_for_gender.pkl","rb"))
le1_pik=pickle.load(open("label_encoding_for_geo.pkl","rb"))


def predict_churn(CreditScore, Geo, Gen, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary):
    input = np.array([[CreditScore, Geo, Gen, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary]]).astype(np.float64)
    if option == 'XGBoost Classifier':
        prediction = model.predict_proba(input)
        pred = '{0:.{1}f}'.format(prediction[0][0], 2)

    else:
        prediction = model.predict_proba(input)
        pred = '{0:.{1}f}'.format(prediction[0][0], 2)

    return float(pred)


def main():
    st.title("Prediction of churn customers")
    html_temp = """
    <div style="background-color:teal ;padding:10px">
    <h2 style="color:yellow;text-align:center;">Churn Classification</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)







    CreditScore = st.slider('Select credit score', 300, 900)

    Geography = st.selectbox('Enter geography', ['France', 'Germany', 'Spain'])
    Geo = int(le1_pik.transform([Geography]))

    Gender = st.selectbox('Enter the gender', ['Male', 'Female'])
    Gen = int(le_pik.transform([Gender]))

    Age = st.slider("Select Age(in years)", 10, 95)

    Tenure = st.selectbox("Select tenure(in years)", ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9','10', '11', '12', '13', '14', '15'])

    Balance = st.slider("Select balance", 0.00, 250000.00)

    NumOfProducts = st.selectbox('Select number of products', ['1', '2', '3', '4'])

    HasCrCard = st.selectbox("Has credit card or not.(yes-1,no-0)", ['0', '1'])

    IsActiveMember = st.selectbox("Is an active member or not.(yes-1,no-0)", ['0', '1'])

    EstimatedSalary = st.slider("Select the estimated salary", 0.00, 200000.00)

    churn_html = """  
              <div style="background-color:#F6EFEF;padding:10px >
               <h2 style="color:red;text-align:center;"> A churn customer</h2>
               </div>
            """
    no_churn_html = """  
              <div style="background-color:#F0F6EF;padding:10px >
               <h2 style="color:green ;text-align:center;"> not a churn customer</h2>
               </div>
            """

    if st.button('Predict'):
        output = predict_churn(CreditScore, Geo, Gen, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary)
        st.success('The probability of customer being churned is {}'.format(output))
        st.balloons()

        if output >= 0.5:
            st.markdown(churn_html, unsafe_allow_html= True)

        else:
            st.markdown(no_churn_html, unsafe_allow_html= True)

if __name__=='__main__':
    main()
