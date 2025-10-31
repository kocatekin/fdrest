from flask import Flask, jsonify, render_template, request, render_template_string, send_from_directory, make_response
from flask_socketio import SocketIO, emit
from mlmodel import guess
import pandas as pd
import sqlite3



from flask_cors import CORS

app = Flask(__name__, static_folder="static")
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

received_data = []
DB_PATH = "sensor_data.db"


@app.route('/')
def index():
   return send_from_directory(app.static_folder, "f2.html")

@app.route('/send', methods=['POST'])
def send():
   data = request.get_json()
   print(f"received: {data}")
   print("time", data.get("Time"))  
   
   #fault detection
   rec_data = [data]
   df = pd.DataFrame(rec_data)

   #drop time column
   if "Time" in df.columns:
      df = df.drop(columns=["Time"])

   result = guess(df)
   fault_values = result.to_dict(orient="records")[0]
   full_record = {**data, **fault_values}
   print(full_record)


   #save to database
   conn = sqlite3.connect(DB_PATH)
   c = conn.cursor()
   c.execute("""
            INSERT INTO sensor_data(
             time, rotation_speed, temperature, level, kurtosis_axial, kurtosis_vertical, kurtosis_horizontal, peak_axial, peak_vertical, peak_horizontal, vibration_acc_axial, vibration_acc_vertical, vibration_acc_horizontal,vibration_vel_axial, vibration_vel_vertical, vibration_vel_horizontal, band_0_8k, band_8_16k, band_16_24k, band_24_32k, band_32_40k, band_40_48k, band_48_56k, band_56_64k, band_64_72k, band_72_80k, band_0_200, band_200_400, band_400_600, band_600_800, band_800_1000, band_1_1_2k, band_1_2_1_4k, band_1_4_1_6k, band_1_6_1_8k, band_1_8_2k, fault0, fault1, fault2, fault3, fault4, fault5, fault6, fault7) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
             (full_record["Time"], full_record["Rotation Speed"], full_record["Temperature"], full_record["Level"], full_record["KURTOSIS_Axial"], full_record['KURTOSIS_Vertical'], full_record['KURTOSIS_Horizontal'], full_record['PEAK_Axial'], full_record['PEAK_Vertical'], full_record['PEAK_Horizontal'], full_record['VIBRATION_ACC_Axial'], full_record['VIBRATION_ACC_Vertical'], full_record['VIBRATION_ACC_Horizontal'], full_record['VIBRATION_VEL_Axial'], full_record['VIBRATION_VEL_Vertical'], full_record['VIBRATION_VEL_Horizontal'], full_record['0-8 kHz'], full_record['8-16 kHz'], full_record['16-24 kHz'], full_record['24-32 kHz'], full_record['32-40 kHz'], full_record['40-48 kHz'], full_record['48-56 kHz'], full_record['56-64 kHz'], full_record['64-72 kHz'], full_record['72-80 kHz'], full_record['0-200 Hz'], full_record['200-400 Hz'], full_record['400-600 Hz'], full_record['600-800 Hz'], full_record['800-1000 Hz'], full_record['1-1.2 kHz'], full_record['1.2-1.4 kHz'], full_record['1.4-1.6 kHz'], full_record['1.6-1.8 kHz'], full_record['1.8-2 kHz'], full_record['fault0'], full_record['fault1'], full_record['fault2'], full_record['fault3'], full_record['fault4'], full_record['fault5'], full_record['fault6'], full_record['fault7']))
   conn.commit()
   conn.close()

   
   socketio.emit('update_table', result.to_dict(orient="records"))
   return jsonify(result.to_dict(orient="records"))

   
@app.route('/history')
def history():
   metric = request.args.get("metric")
   limit = request.args.get("limit")
   print(metric, limit)

   # connect to db and call it, return {timestamps: [], values: []}
   conn = sqlite3.connect(DB_PATH)
   c = conn.cursor()
   c.execute(f"select time, {metric} from sensor_data order by id desc limit ?", (limit,))
   rows = c.fetchall()
   conn.close()
   rows.reverse()
   timestamps = [r[0] for r in rows]
   values = [r[1] for r in rows]
   print(timestamps, values)
   return jsonify({"timestamps": timestamps, "values": values})
   
@app.route('/dashboard')
def dashboard():
   return render_template("index.html")

@app.route('/report')
def report():
   return send_from_directory(app.static_folder, "report.html")


@app.route('/generate_csv')
def generate_csv():
   start_date = request.args.get("start")
   end_date = request.args.get("end")
   threshold_str = request.args.get("threshold", "").strip()

   conn = sqlite3.connect(DB_PATH)
   df = pd.read_sql_query(
      "select * from sensor_data where time between ? and ? order by time asc",
      conn,
      params=(start_date, end_date)
   )
   conn.close()

   if df.empty:
      return jsonify({"message": "No data found for given range"}), 404
   
   #compute max_fault
   df["max_fault"] = df[["fault0", "fault1", "fault2", "fault3", "fault4", "fault5", "fault6", "fault7"]].max(axis=1)

   if threshold_str:
      try:
         threshold = float(threshold_str)
         df = df[df["max_fault"] >= threshold]
         if df.empty:
            return jsonify({"message": "No data exceeded threshold"}), 404
      except ValueError:
         return jsonify({"message": "Invalid threshold value"}), 400
      
   csv_data = df.to_csv(index=False)

   filename = f"fault_report_{start_date}_to_{end_date}.csv"
   response = make_response(csv_data)
   response.headers["Content-Disposition"] = f"attachment; filename={filename}"
   response.headers["Content-Type"] = "text/csv"
   return response


   




if __name__ == "__main__":
   socketio.run(app, host="0.0.0.0", port=5000, debug=True)