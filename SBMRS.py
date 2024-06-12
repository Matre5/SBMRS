import numpy as np
import pickle
import pandas as pd
from Sym_Diseases import Disease_dict, symptoms_dict


#Loading Databases
symptoms = pd.read_csv('data/symtoms_df.csv')
precautions = pd.read_csv('data/precautions_df.csv')
lifestyle = pd.read_csv('data/workout_df.csv')
description = pd.read_csv('data/description.csv')
medication = pd.read_csv('data/medications.csv')

#Loading our svc trained model
svc = pickle.load(open("model/svc.pkl", "rb"))


def details(PD):
    Description = description[description['Disease'] == PD]['Description']
    Description = " ".join([w for w in Description])
    
    Precaution = precautions[precautions['Disease'] == PD][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    Precaution = [pre  for pre in Precaution.values]
    
    Medication = medication[medication['Disease'] == PD]['Medication']
    Medication = [med for med in Medication.values]
    
    Lifestyle = lifestyle[lifestyle['disease'] == PD]['workout']
    
    return Description, Precaution, Medication, Lifestyle


def predict_sym(patient_Symptoms):
    input_vector = np.zeros(len(symptoms_dict))

    for item in patient_Symptoms:
        input_vector[symptoms_dict[item]] = 1
    return Disease_dict[svc.predict([input_vector])[0]]
