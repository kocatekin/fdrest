import os
import sqlite3

DB_PATH = "sensor_data.db"

def init_db():
   conn = sqlite3.connect(DB_PATH)
   c = conn.cursor()
   c.execute("""
             CREATE TABLE IF NOT EXISTS sensor_data(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             time TEXT NOT NULL,
             rotation_speed REAL,
             temperature REAL,
             level REAL,
             kurtosis_axial REAL,
             kurtosis_vertical REAL,
             kurtosis_horizontal REAL,
             peak_axial REAL,
             peak_vertical REAL,
             peak_horizontal REAL,
             vibration_acc_axial REAL,
             vibration_acc_vertical REAL,
             vibration_acc_horizontal REAL,
             vibration_vel_axial REAL,
             vibration_vel_vertical REAL,
             vibration_vel_horizontal REAL,
             band_0_8k REAL,
             band_8_16k REAL,
             band_16_24k REAL,
             band_24_32k REAL,
             band_32_40k REAL,
             band_40_48k REAL,
             band_48_56k REAL,
             band_56_64k REAL,
             band_64_72k REAL,
             band_72_80k REAL,
             band_0_200 REAL,
             band_200_400 REAL,
             band_400_600 REAL,
             band_600_800 REAL,
             band_800_1000 REAL,
             band_1_1_2k REAL,
             band_1_2_1_4k REAL,
             band_1_4_1_6k REAL,
             band_1_6_1_8k REAL,
             band_1_8_2k REAL,
             fault0 REAL,
             fault1 REAL,
             fault2 REAL,
             fault3 REAL,
             fault4 REAL,
             fault5 REAL,
             fault6 REAL,
             fault7 REAL
             );""")
   conn.commit()
   conn.close()

init_db()