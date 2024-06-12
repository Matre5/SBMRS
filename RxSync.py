import numpy as np
import pickle
import streamlit as st
from SBMRS import description, precautions, medication, lifestyle, symptoms_dict, Disease_dict
# from email_utilities import send_email
import logging
import os
import smtplib as sm
from email.message import EmailMessage
from googletrans import Translator, LANGUAGES


#Loading our trained model
svc = pickle.load(open("model/svc.pkl", "rb"))

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG

email_sender = 'aigmatre5@gmail.com'
email_password = 'gfpvxyrynrdksehk'

def details(PD):
    
    import importlib
    SBMRS = importlib.import_module("SBMRS")
    
    description = SBMRS.description
    precautions = SBMRS.precautions
    medication = SBMRS.medication
    lifestyle = SBMRS.lifestyle
        
    
    Description = description[description['Disease'] == PD]['Description']
    Description = " ".join([w for w in Description])
    
    Precaution = precautions[precautions['Disease'] == PD][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    Precaution = [pre  for pre in Precaution.values]
    
    Medication = medication[medication['Disease'] == PD]['Medication']
    Medication = [med for med in Medication.values]
    
    Lifestyle = lifestyle[lifestyle['disease'] == PD]['workout']
    
    return Description, Precaution, Medication, Lifestyle


def predict_sym(patient_Symptoms):
    # Dynamically import SBMRS module here
    import importlib
    SBMRS = importlib.import_module("SBMRS")
    
    symptoms_dict = SBMRS.symptoms_dict
    Disease_dict = SBMRS.Disease_dict
    
    
    input_vector = np.zeros(len(symptoms_dict))

    for item in patient_Symptoms:
        input_vector[symptoms_dict[item]] = 1
    return Disease_dict[svc.predict([input_vector])[0]]

page_contents = {
    
    "instruction": "Please select a disease and click 'Generate recommendation' to view the description.",
    "generate_button": "Generate recommendation",
    "result_header": "Prediction Details:",
    "description_label": "Description:",
    "precautions_label": "Precautions:",
    "medication_label": "Medication:",
    "lifestyle_label": "Lifestyle:",
    "send_email_button": "Send result to email",
    "error_message": "Please fill in all required fields.",
    "generate_error_message": "Failed to generate a recommendation. Please try again.",
    "email_sent_message": "Email sent successfully!",
    "name_prompt": "Please enter your name",
    "email_prompt": "Preferred email for your result",
    "symptoms_prompt": "Select symptoms, as many as experienced"
}


def main():
    
    
    st.title("RxSync⚕️")
    st.subheader("***Syncing symptoms with the perfect prescription match...***")
    logging.debug("Starting main function")
    
    options = ["English", "Others"]
    
    Response = st.selectbox("Preffered page language: ", options)
    
    if Response == "English": 
        #getting input from users
        name = st.text_input("Please enter your name")
        logging.debug(f"Name entered: {name}")
        
        email = st.text_input('Preferred email for your result')
        logging.debug(f"Email entered: {email}")
            
        selected_symptoms = st.multiselect('Select symptoms, as many as experienced', list(symptoms_dict.keys()))
        logging.debug(f"Selected symptoms: {selected_symptoms}")
        
        predicted_dis = ''
     
        #creating the submit button for recommendation
        if st.button("Generate recommendation", key="gen rec"):
            if not name or not email or not selected_symptoms:
                st.error("Please fill in all required fields.")
            else:
                predicted_dis = predict_sym(selected_symptoms)
            
                if predicted_dis:
                    # Displaying prediction details
                    Description, Precaution, Medication, Lifestyle = details(predicted_dis)
                    
                
                    st.markdown("<h1>Prediction Details:</h1>", unsafe_allow_html=True)
                    
                    # Displaying Description
                    st.write("**Description:**")
                    st.write(Description)
                    
                    # Displaying Precautions
                    st.write("**Precautions:**")
                    for idx, pre in enumerate(Precaution, start=1):
                        st.write(f"Precaution : {pre}")
                    
                    # Displaying Medication
                    st.write("**Medication:**")
                    for med in Medication:
                        st.write(med)
                    
                    # Displaying Lifestyle
                    st.write("**Lifestyle:**")
                    l = 1
                    for life in Lifestyle:
                        st.write(life)
                        l += 1
            
            
            # Button to send email
            
            # send_email = st.button("Send result to email")
                    subject = "RxSync⚕️"
                    email_body = f"""
                    Dear {name}
                    This is your result from your Symptom based Medicine Recommendation System
                    
                    Your symptoms: {selected_symptoms}
                    
                    The Predicted disease: {predicted_dis}
                    
                    Description of the disease: {Description}
                    
                    Dos and Don't : {Precaution}
                    
                    Medications: {', '.join(Medication)}
                    
                    Lifestyle : {', '.join(Lifestyle)}
                    """
                    if st.button("Send result to email", key="sender"):
                        try:
                            connection = sm.SMTP('smtp.gmail.com', 587)
                            connection.starttls()
                            connection.login(email_sender, email_password)
                            message = "Subject:{}\n\n{}".format(subject, email_body)
                            connection.sendmail(email_sender, email, message)
                            connection.quit()
                            st.success("Email sent successfully")
                        except Exception as e:
                                a = os.system("ping www.google.com")
                                if a == 1:
                                    st.error("Please check your internet connection")
                                else:
                                    st.error("Wrong Email or Password")
                else:
                    st.error("Failed to generate a recommendation. Please try again.")
                    

    
    elif Response == "Others":
        # st.button("Translate page")
        
        languages = get_languages()
        target_language = st.selectbox("Select the language:", languages)
        # Update page with translated contents
        
        title = "RxSync⚕️"
        sub_t = "Syncing symptoms with the perfect prescription match..."
        st.title(translate_text(title, target_language))
        st.subheader(translate_text(sub_t,target_language))
        st.write(translate_text(page_contents["instruction"], target_language))
        name = st.text_input(translate_text(page_contents["name_prompt"], target_language))
        logging.debug(f"Name entered: {name}")
        
        email = st.text_input(translate_text(page_contents["email_prompt"], target_language))
        logging.debug(f"Email entered: {email}")
            
        selected_symptoms = st.multiselect(translate_text(page_contents["symptoms_prompt"], target_language), list(symptoms_dict.keys()))
        logging.debug(f"Selected symptoms: {selected_symptoms}")
        
       
        predicted_dis = ''
        if st.button(translate_text(page_contents["generate_button"], target_language)):
            if not name or not email or not selected_symptoms:
                st.error(translate_text(page_contents["error_message"], target_language))
            else:
                predicted_dis = predict_sym(selected_symptoms)
                if predicted_dis:
                    # Displaying prediction details
                    Description, Precaution, Medication, Lifestyle = details(predicted_dis)
                    Pred = translate_text(page_contents["result_header"], target_language)
                    st.title(Pred)
                    
                    st.write(translate_text(page_contents["description_label"], target_language))
                    st.write(translate_text(Description, target_language))
                    
                    st.write(translate_text(page_contents["precautions_label"], target_language))
                    for idx, pre in enumerate(Precaution, start=1):
                        pre_list = pre.tolist()  # Convert NumPy array to list
                        translated_precaution = [translate_text(item, target_language) for item in pre_list]
                        st.write(f"Precaution : {', '.join(translated_precaution)}")
                    st.write(translate_text(page_contents["medication_label"], target_language))
                    for med in Medication:
                        st.write(translate_text(med, target_language))
                        
                    st.write(translate_text(page_contents["lifestyle_label"], target_language))
                    for life in Lifestyle:
                        st.write(translate_text(life, target_language))

                    # Button to send email
                    if st.button(translate_text(page_contents["send_email_button"], target_language), key="sender"):
                        if predicted_dis:
                            # email_sender(name, email, selected_symptoms, predicted_dis, Description, Precaution, Medication, Lifestyle)
                            st.success(translate_text(page_contents["email_sent_message"], target_language))
                        try:
                            connection = sm.SMTP('smtp.gmail.com', 587)
                            connection.starttls()
                            connection.login(email_sender, email_password)
                            message = "Subject:{}\n\n{}".format(subject, email_body)
                            connection.sendmail(email_sender, email, message)
                            connection.quit()
                            st.success("Email sent successfully")
                        except Exception as e:
                                a = os.system("ping www.google.com")
                                if a == 1:
                                    st.error("Please check your internet connection")
                                else:
                                    st.error("Wrong Email or Password")
                else:
                    st.error(translate_text(page_contents["generate_error_message"], target_language))            
    
    return name, email, selected_symptoms, predicted_dis

def get_languages():
    language = [LANGUAGES[lang] for lang in LANGUAGES]
    return language

def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text


if __name__ == '__main__':
    main()