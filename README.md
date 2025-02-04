# Sensor-Fault-Detection

### Problem Statement
The Air Pressure System (APS) is a critical component of a heavy-duty vehicle that uses compressed air to force a piston to provide pressure to the brake pads, slowing the vehicle down. The benefits of using an APS instead of a hydraulic system are the easy availability and long-term sustainability of natural air.

This is a Binary Classification problem, in which the affirmative class indicates that the failure was caused by a certain component of the APS, while the negative class
indicates that the failure was caused by something else.

### Solution Proposed 
In this project, the system in focus is the Air Pressure system (APS) which generates pressurized air that are utilized in various functions in a truck, such as braking and gear changes. The datasets positive class corresponds to component failures for a specific component of the APS system. The negative class corresponds to trucks with failures for components not related to the APS system.

The problem is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions.
## Tech Stack Used
1. Python 
2. FastAPI 
3. Machine learning algorithms
4. MongoDB

## How to run?
Before we run the project, make sure that you are having MongoDB in your local system, with Compass since we are using MongoDB for data storage.

## Project Archietecture
![image](https://github.com/user-attachments/assets/a0861177-57ea-44d5-a4ee-8c1c3966060d)

### Step 1: Clone the repository
```bash
git clone https://github.com/Akhil244/minisensor.git
```

### Step 2- Create a conda environment after opening the repository

```bash
conda create -n sensor python=3.12.4 -y
```

```bash
conda activate sensor
```

### Step 3 - Install the requirements
```bash
pip install -r requirements.txt
```

### Step 4 - Export the environment variable
```bash

export MONGODB_URL="mongodb+srv://<username>:<password>@cluster0.9dl24.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

```

### Step 5 - Run the application server
```bash
python main.py
```
