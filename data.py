import pandas as pd
import random
from datetime import datetime, timedelta

# --------------------------------------------------
# VEHICLE DEFINITIONS
# --------------------------------------------------

vehicle_types = [
    {
        "manufacturer": "Tesla",
        "model": "Model 3",
        "battery_capacity": 60,
        "max_speed": 225,
        "range": 500,
        "consumption": 0.14,
        "garage": "Garage A"
    },
    {
        "manufacturer": "Tata",
        "model": "Nexon EV",
        "battery_capacity": 40.5,
        "max_speed": 120,
        "range": 465,
        "consumption": 0.18,
        "garage": "Garage B"
    },
    {
        "manufacturer": "MG",
        "model": "ZS EV",
        "battery_capacity": 50.3,
        "max_speed": 175,
        "range": 461,
        "consumption": 0.17,
        "garage": "Garage C"
    },
    {
        "manufacturer": "Hyundai",
        "model": "Kona EV",
        "battery_capacity": 39.2,
        "max_speed": 167,
        "range": 452,
        "consumption": 0.16,
        "garage": "Garage D"
    }
]

# --------------------------------------------------
# CREATE 50 UNIQUE CARS
# --------------------------------------------------

cars = []

for i in range(50):

    spec = vehicle_types[i % 4]

    cars.append({
        "car_id": f"EV{str(i+1).zfill(4)}",
        "driver": f"Driver_{str(i+1).zfill(3)}",
        "manufacturer": spec["manufacturer"],
        "model": spec["model"],
        "battery_capacity": spec["battery_capacity"],
        "max_speed": spec["max_speed"],
        "range": spec["range"],
        "consumption": spec["consumption"],
        "garage": spec["garage"],
        "year_manufactured": random.randint(2019, 2025)
    })

# --------------------------------------------------
# GENERATE DATA
# --------------------------------------------------

rows = []

base_time = datetime(2025, 1, 1)

for car in cars:

    age_days = random.randint(100, 2500)

    avg_daily_km = random.randint(20, 120)

    base_km = age_days * avg_daily_km

    charging_cycles = base_km // 250

    battery_health = (
        100
        - (age_days / 365) * 1.5
        - charging_cycles * 0.01
        + random.uniform(-1.5, 1.5)
    )

    battery_health = round(
        max(70, min(100, battery_health)),
        2
    )

    for _ in range(200):

        timestamp = (
            base_time +
            timedelta(minutes=random.randint(0, 525600))
        )

        battery_percentage = round(
            random.uniform(5, 100),
            2
        )

        # Charging / Running

        if battery_percentage < 20:
            charging = 1
            running = 0
        else:
            charging = random.choice([0, 0, 0, 1])
            running = 1 - charging

        # Speed

        if running == 1:
            instantaneous_speed = random.randint(
                10,
                car["max_speed"]
            )
        else:
            instantaneous_speed = 0

        # Charging Cost

        if charging == 1:

            units = random.uniform(5, 50)

            charging_cost = round(
                units * random.uniform(8, 12),
                2
            )

        else:
            charging_cost = 0

        # Revenue

        if running == 1:

            if random.random() < 0.70:
                revenue = round(
                    random.uniform(100, 1000),
                    2
                )
            else:
                revenue = 0

        else:
            revenue = 0

        # KM Travelled

        km_travelled = (
            base_km +
            random.randint(0, 5000)
        )

        # Expected Distance

        expected_distance = round(
            car["range"]
            * (battery_percentage / 100)
            * (battery_health / 100),
            2
        )

        # Maintenance Cost

        maintenance_cost = round(
            (age_days * 0.5)
            + (km_travelled * 0.03),
            2
        )

        # Garage Status

        if charging == 1:
            garage_status = "Charging"
        else:
            garage_status = random.choice(
                ["Working", "Working", "Working", "Parked"]
            )

        rows.append([
            car["car_id"],
            car["manufacturer"],
            car["model"],
            car["driver"],
            car["battery_capacity"],
            battery_percentage,
            battery_health,
            expected_distance,
            car["max_speed"],
            instantaneous_speed,
            revenue,
            age_days,
            km_travelled,
            car["consumption"],
            car["year_manufactured"],
            maintenance_cost,
            charging,
            running,
            charging_cost,
            car["garage"],
            garage_status,
            timestamp.strftime("%d/%m/%Y %H:%M:%S")
        ])

# --------------------------------------------------
# DATAFRAME
# --------------------------------------------------

columns = [
    "Car_ID",
    "Manufacturer",
    "Car_Model",
    "Driver",
    "Battery_Capacity_kWh",
    "Battery_Percentage",
    "Battery_Health",
    "Expected_Distance_KM",
    "Max_Speed_KMH",
    "Instantaneous_Speed_KMH",
    "Revenue",
    "Age_Days",
    "KM_Travelled",
    "Energy_Consumption_Rate",
    "Year_Manufactured",
    "Maintenance_Cost",
    "Charging",
    "Running",
    "Charging_Cost",
    "Garage",
    "Garage_Status",
    "Timestamp"
]

df = pd.DataFrame(rows, columns=columns)

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    format="%d/%m/%Y %H:%M:%S"
)

df = df.sort_values("Timestamp")

df.to_csv(
    "EV_Fleet_10000_Rows.csv",
    index=False
)

print(df.head())
print("Rows:", len(df))
print("Saved as EV_Fleet_10000_Rows.csv")