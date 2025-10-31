# FD-REST: Fault Detection REST API and Interactive Dashboard

**FD-REST** is a reproducible research software for **machine fault detection** and **real-time visualization**.  
It demonstrates the complete pipeline — from **sensor data acquisition** to **neural-network-based fault prediction**, **database storage**, **web-based dashboards**, and **report generation** — all encapsulated in a **Docker environment** for long-term reproducibility.

---

## Overview

FD-REST combines:

- **A REST API (Flask + Flask-SocketIO)** for prediction and data handling  
- **A trained Deep Neural Network (Keras)** for fault estimation  
- **An SQLite database** for historical storage  
- **A simulation script (`sender.py`)** that mimics live sensor streams  
- **Tailwind- and Chart.js-based dashboards** for monitoring and reporting  
- **A Docker container** that reproduces the full environment automatically  

It is suitable for:

- **Researchers** who want to reproduce fault detection pipelines  
- **Educators** demonstrating machine learning integration in industrial monitoring  
- **Engineers** exploring lightweight, local dashboards for predictive maintenance

---

## 🗂️ Project Structure

| File / Folder | Description |
|----------------|-------------|
| `create_db.py` | Initializes the SQLite database (`sensor_data.db`) with all sensor and fault fields. Automatically creates the schema if not present. |
| `mlmodel.py` | Loads the pre-trained `dnn_model.keras` model, normalizes inputs with `feature_scaler.pkl`, and reverses output scaling using `target_scaler.pkl`. |
| `restapi.py` | Main Flask backend. Exposes endpoints for data ingestion, history retrieval, CSV export, and serves the live dashboard. Integrates Socket.IO for real-time updates. |
| `sender.py` | Simulates sensor readings by reading `data.csv` line by line and sending them as JSON to the `/send` endpoint. Acts as a virtual sensor node. |
| `data.csv` | Example dataset representing machine telemetry and vibration bands. Each row corresponds to one time step. |
| `f2.html` | Full-featured fault detection dashboard with TailwindCSS UI, live charts, and fault category insights. |
| `report.html` | Allows generating downloadable CSV reports filtered by date and fault threshold. |
| `frontend.html`, `index.html` | Minimal alternative UIs showing raw prediction tables for debugging or demonstration. |
| `Dockerfile` | Defines a reproducible environment (Python 3.10 + TensorFlow + Flask) for long-term execution. |
| `sensor_data.db` | SQLite database file (auto-generated). |
| `target_scaler.pkl`, `feature_scaler.pkl` | Scaler files used for normalization and denormalization of model inputs/outputs. |

---

## Architecture


1. **Simulation (`sender.py`)** mimics sensor data being streamed every few seconds.  
2. **REST API (`restapi.py`)** receives this data, applies the ML model, stores it in SQLite, and emits predictions to all connected dashboards.  
3. **Dashboard (`f2.html`)** displays live fault probabilities, categories, and charts using WebSockets and `/history` endpoint.  
4. **Report Page (`report.html`)** allows exporting filtered historical results as CSV.  

---

## Getting Started

### 1. Prerequisites

- Docker Desktop (Windows/macOS) or Docker Engine (Linux)  
- Optional: Python ≥ 3.10 with `pip` if you prefer local execution  
- Port 5000 free on your system  

### 2. Clone the Repository

```bash
git clone https://github.com/<yourusername>/fdrest.git
cd fdrest
```

### 3. Build the Docker Image

`docker build -t fdrest .`

### 4. Run the container

`docker run -p 5000:5000 fdrest`

**Result:**

* API and dashboard are available at: http://localhost:5000
* The database (sensor_data.db) will be created automatically inside the container.

## Simulating Real Life Data

The system expects sensor data in JSON format — but since no real sensors are connected, `sender.py` serves as a virtual sensor.

1. Open a second terminal.
2. Run inside your local machine or attach to the container shell:
`python sender.py`
3. The script will:
* Read each row from `data.csv`
* Convert values into a dictionary
* Send it as a JSON POST to `http://localhost:5000/send`
* Wait a few seconds between each transmission, controlled by `SLEEP_TIME = 3`

Each successful POST will print the following into the console:
`sent: ['Time', 'Rotation Speed', 'Temperature', ...] -> status: 200`

## Machine Learning Workflow

Backend loads:

* `dnn_model.keras` -> Trained neural network
* `feature_scaler.pkl` -> StandardScaler for input normalization
* `target_scaler.pkl` → Scaler to revert model output

When new data arrives:

1. Input features are scaled using feature_scaler.pkl
2. The model predicts fault intensities (fault0–fault7)
3. Outputs are inverse-transformed and inserted into the database
4. The dashboard receives a live JSON update via Socket.IO

## Web Interface

Web interface is accessed via: `http://localhost:5000` which will refer to `f2.html`.

Features:
* Live Fault Probability
* Fault Category & Root Cause information
* Dynamic metric grid to see all values for every fault type
* Temperature and Kurtosis charts (refreshes every 5 seconds)
* Responsive layout

## Report Generator

Accessed via a button or directly from: `http://localhost:5000/report`.

**Usage:**
1. Choose a start and end date
2. Optionally enter a threshold (if you want to see only fault values above a certain level)
3. Filtered report downloads automatically in csv format

## REST API Endpoints

| Endpoint        | Method | Parameters                               | Description                                                   |
| --------------- | ------ | ---------------------------------------- | ------------------------------------------------------------- |
| `/send`         | `POST` | JSON body of sensor readings             | Inserts a record, predicts faults, emits WebSocket update.    |
| `/history`      | `GET`  | `metric`, `limit`                        | Returns last *N* samples for a given metric (used in charts). |
| `/generate_csv` | `GET`  | `start`, `end`, `threshold` *(optional)* | Exports historical data as CSV for reporting.                 |
| `/report`       | `GET`  | –                                        | Displays the CSV report generator interface.                  |
| `/dashboard`    | `GET`  | –                                        | Alternate minimal dashboard (`index.html`).                   |
| `/`             | `GET`  | –                                        | Main Tailwind dashboard (`f2.html`).                          |


## Example workflow summary

1. Run container: `docker run -p 5000:5000 fdrest`
2. Simulate sensor feed: `python sender.py`
3. Observe dashboard: `http://localhost:5000`
4. Generate CSV report: `http://localhost:5000/report`

## Tech stack

| Layer            | Tools                                    |
| ---------------- | ---------------------------------------- |
| Backend          | Flask, Flask-SocketIO, Flask-CORS        |
| ML / Inference   | TensorFlow (Keras), Scikit-learn, Joblib |
| Database         | SQLite3                                  |
| Frontend         | HTML5, TailwindCSS, Chart.js, Socket.IO  |
| Containerization | Docker (Python 3.10 base image)          |


## License

Distributed under the MIT License.
You are free to use, modify, and cite this project with attribution.