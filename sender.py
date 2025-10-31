import requests as req
import csv
import time


API_URL = "http://localhost:5000/send"
CSV_FILE = "data.csv"
SLEEP_TIME = 3


EXCLUDE_COLS = ["fault0", "fault1", "fault2", "fault3", "fault4", "fault5", "fault6", "fault7"]

def try_float(value):
   try:
      return float(value)
   except ValueError:
      #print("there was something wrong")
      return value


def read_csv(filename):
   with open(filename, newline="", encoding="utf-8") as f:
      reader = csv.reader(f)
      headers = next(reader)
      for row in reader:
         filtered_row = row[0:-8]
         filtered_headers = headers[0:-8]
         converted_row = [try_float(val) for val in filtered_row]
         yield dict(zip(filtered_headers, converted_row))
         

def send_request(data):
   try:
      res = req.post(API_URL, json=data)
      print(f"sent: {list(data.keys())[:5]}... -> status: {res.status_code}")
   except Exception as e:
      print(f"error: {e}")

def main():
   for row in read_csv(CSV_FILE):
      send_request(row)
      time.sleep(SLEEP_TIME)

if __name__ == "__main__":
   main()

