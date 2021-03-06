import pickle
import os
import numpy as np
import lime
from lime import lime_tabular
# scaler = pickle.load(
#     open(
#         '/home/mufaddal/Mufaddal/Git/Backend/SepsisBackend/APIEndPoint/TrainedModel/scaler.sav',
#         'rb'))
# model = pickle.load(
#     open(
#         '/home/mufaddal/Mufaddal/Git/Backend/SepsisBackend/APIEndPoint/TrainedModel/model.sav',
#         'rb'))

cols = [
    'hr', 'o2sat', 'temp', 'sbp', 'map', 'dbp', 'resp', 'etco2', 'baseexcess',
    'hco3', 'fio2', 'ph', 'paco2', 'sao2', 'ast', 'bun', 'alkalinephos',
    'calcium', 'chloride', 'creatinine', 'bilirubin_direct', 'glucose',
    'lactate', 'magnesium', 'phosphate', 'potassium', 'bilirubin_total',
    'troponini', 'hct', 'hgb', 'ptt', 'wbc', 'fibrinogen', 'platelets', 'age',
    'gender', 'hospadmtime', 'iculos'
]

COLS = [
    'HR', 'O2Sat', 'Temp', 'SBP', 'MAP', 'DBP', 'Resp', 'EtCO2', 'BaseExcess',
    'HCO3', 'FiO2', 'pH', 'PaCO2', 'SaO2', 'AST', 'BUN', 'Alkalinephos',
    'Calcium', 'Chloride', 'Creatinine', 'Bilirubin_direct', 'Glucose',
    'Lactate', 'Magnesium', 'Phosphate', 'Potassium', 'Bilirubin_total',
    'TroponinI', 'Hct', 'Hgb', 'PTT', 'WBC', 'Fibrinogen', 'Platelets', 'Age',
    'Gender', 'HospAdmTime', 'ICULOS'
]

scaler = pickle.load(open('APIEndPoint/TrainedModel/scaler.sav', 'rb'))
model = pickle.load(open('APIEndPoint/TrainedModel/model_lgbm.sav', 'rb'))
# print(os.listdir(os.getcwd()))
explainer = pickle.load(open('APIEndPoint/TrainedModel/explainer.pkl', 'rb'))


def prob(data):
    return np.array(list(zip(1 - model.predict(data), model.predict(data))))


def processData(inp):

    data = []
    for k in cols:
        data.append(inp[k])

    X = scaler.transform([data])
    y = model.predict_proba(X)[:, 1]
    features = {
        # "ICULOS": 0.15565901989176315,
        # "Temp": 0.04888667943307586,
        # "Bilirubin_direct": 0.02674016073371643,
        # "Hct": -0.023410676554303914,
        # "Calcium": -0.021169457728308104,
        # "WBC": 0.01955435898121803,
        # "BUN": -0.015787464366801403,
        # "HR": 0.015564168886349804,
        # "MAP": -0.012930284073671474,
        # "EtCO2": -0.012584893804325184
    }

    inpar = np.array(data)
    exp = explainer.explain_instance(inpar, predict_fn=prob, num_features=10)

    f = exp.as_map()
    for i in f[1]:
        ind = i[0]
        val = i[1]
        features[COLS[ind]] = val
    return (y[0], features)