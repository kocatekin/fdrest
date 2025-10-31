import pandas as pd
import joblib
from tensorflow.keras.models import load_model

def guess(mydata):
   
   model = load_model("dnn_model.keras", compile=False) 
   feature_scaler = joblib.load("feature_scaler.pkl")
   target_scaler = joblib.load("target_scaler.pkl")

   #scaled features
   X_scaled = feature_scaler.transform(mydata)

   #predict
   y_pred_normalized = model.predict(X_scaled)
   y_pred = target_scaler.inverse_transform(y_pred_normalized)

   #show results
   fault_columns = ["fault0", "fault1", "fault2", "fault3", "fault4", "fault5", "fault6", "fault7"]
   prediction_df = pd.DataFrame(y_pred, columns=fault_columns)
   #row_dict = prediction_df.iloc[0].to_dict()
   return prediction_df
   