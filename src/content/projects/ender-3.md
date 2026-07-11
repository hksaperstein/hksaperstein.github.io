---
title: "Ender-3 Pro"
description: "Optimizations and improvements made to my Ender-3 Pro with an ongoing drive to tinker further."
date: 2024-04-04
categories: [3D Printing]
featured_image: "/assets/images/projects/ender3-pro/sensor-monitoring.gif"
thingiverse_url: "https://www.thingiverse.com/hksaperstein/collections/43743826/things"
demo_url: "#"

models:
  - file: "/assets/models/iot-monitor/sensor-housing.gltf"
    description: "Weatherproof housing for outdoor sensor deployment"
  - file: "/assets/models/iot-monitor/test.gltf"
    description: "IoT sensor enclosure 3D model"

schematics:
  - file: "/assets/schematics/iot-monitor/main-board.svg"
    description: "ESP32 main control board with sensor interfaces"
  - file: "/assets/schematics/iot-monitor/power-management.svg"
    description: "Solar charging system with battery backup"
  - file: "/assets/schematics/iot-monitor/sensor-network.svg"
    description: "Wireless sensor network topology and communication"


components:
  - name: "Ender-3 Pro"
    quantity: 1
    description: "Creality Ender-3 Pro"
    link: "https://www.creality.com/products/ender-3-pro-3d-printer"
    
  - name: "Sprite Extruder Pro Kit"
    quantity: 1
    description: "Retrofit the Ender-3 Pro with a direct-drive filiment extruder" 
    link: "https://www.creality.com/products/sprite-extruder-pro-kit"
    
  - name: "Raspberry Pi 4 Model B, 2GB"
    quantity: 1
    description: "Used for Klipper and Moonraker with a Fluidd front-end"
    

gallery:
  - type: "image"
    file: "/assets/images/projects/ender3-pro/featured.jpg"
    description: "IoT Environmental monitoring station - Physical hardware setup"
  - type: "image"
    file: "/assets/images/projects/ender3-pro/sensor-monitoring.gif"
    description: "Real-time sensor data visualization - Animated demonstration of live monitoring dashboard"
---

## Project Overview
Diving into the world of 3D printing with an Ender-3 Pro purchased 2nd-hand. It has proven to be an excellent platform to practice mechanical design and rapid prototyping. The efforts of which have been used to make improvements to the printer itself.

## System Architecture

### Hardware Components
- **ESP32 Microcontroller**: Main processing unit with WiFi connectivity
- **Multi-Sensor Array**: Temperature, humidity, pressure, light, soil conditions, and weather
- **Solar Power System**: Self-sustaining power with battery backup
- **Weatherproof Enclosure**: IP65-rated protection for outdoor deployment

### Software Stack
- **Embedded Firmware**: C++ on ESP32 for sensor reading and data transmission
- **MQTT Protocol**: Lightweight messaging for IoT communication
- **Python Backend**: Data processing, storage, and analysis
- **Web Dashboard**: Real-time visualization and monitoring interface
- **Mobile App**: Remote monitoring and alert notifications

## Key Features

### Comprehensive Monitoring
- **Temperature & Humidity**: High-precision DHT22 sensor
- **Atmospheric Pressure**: BMP280 barometric sensor
- **Light Levels**: TSL2561 digital luminosity sensor
- **Soil Conditions**: Moisture and temperature monitoring
- **Weather Data**: Rain detection, wind speed and direction

### Energy Efficient Design
- **Solar Powered**: 6W solar panel with MPPT charging
- **Battery Backup**: 2000mAh LiPo for 72-hour operation without sun
- **Sleep Modes**: Ultra-low power consumption between readings
- **Power Monitoring**: Real-time battery voltage and charging status

### Wireless Connectivity
- **WiFi Communication**: IEEE 802.11 b/g/n connectivity
- **MQTT Protocol**: Efficient publish/subscribe messaging
- **Over-the-Air Updates**: Remote firmware updates
- **Fallback Storage**: Local data logging when offline

### Intelligent Alerting
- **Threshold Monitoring**: Customizable alert thresholds
- **Multi-Channel Notifications**: Email, SMS, and push notifications
- **Smart Filtering**: Reduces false alarms with trend analysis
- **Escalation Policies**: Different alert levels based on severity

## Technical Specifications

| Parameter | Specification |
|-----------|---------------|
| **Operating Voltage** | 3.3V (regulated from solar/battery) |
| **Power Consumption** | 45mA active, 10μA sleep |
| **Transmission Range** | WiFi: 100m (outdoor) |
| **Data Resolution** | Temperature: ±0.1°C, Humidity: ±2% |
| **Sampling Rate** | 30 seconds (configurable) |
| **Data Storage** | 1MB onboard flash + cloud storage |
| **Operating Temperature** | -40°C to +85°C |
| **Weather Rating** | IP65 (dust tight, water resistant) |

## Sensor Details

### Environmental Sensors
1. **DHT22**: ±0.5°C temperature, ±2-5% humidity accuracy
2. **BMP280**: ±1 hPa pressure accuracy, 0.17m altitude resolution
3. **TSL2561**: 0.1 to 40,000 lux light measurement range

### Agricultural Sensors
1. **Capacitive Soil Moisture**: Corrosion-resistant, 0-100% range
2. **DS18B20 Soil Temperature**: Waterproof, ±0.5°C accuracy
3. **Rain Sensor**: Digital rain/no-rain detection

### Weather Sensors
1. **Anemometer**: Hall effect, 0-70 m/s wind speed range
2. **Wind Vane**: 16-position wind direction measurement
3. **Weather Station Integration**: Compatible with standard protocols

## Data Processing Pipeline

### Real-Time Processing
1. **Sensor Fusion**: Combines multiple sensor readings for accuracy
2. **Quality Checks**: Validates data for sensor errors and outliers
3. **Calibration**: Automatic drift compensation and calibration
4. **Aggregation**: Computes moving averages and trends

### Advanced Analytics
- **Anomaly Detection**: Machine learning-based outlier detection
- **Predictive Modeling**: Weather and crop condition forecasting
- **Correlation Analysis**: Identifies relationships between variables
- **Statistical Reporting**: Automated daily/weekly/monthly reports

## Dashboard Features

### Real-Time Visualization
- **Live Gauges**: Current readings with color-coded status
- **Time Series Charts**: Historical data with zoom and pan
- **Weather Maps**: Geographic visualization of sensor network
- **Mobile Responsive**: Optimized for phones and tablets

### Data Export
- **CSV Downloads**: Raw data export for analysis
- **API Access**: RESTful API for third-party integration
- **Report Generation**: Automated PDF reports
- **Database Backup**: Scheduled data backups

## Installation & Deployment


<details class="assembly-details">
<summary>Installation & Deployment</summary>
<div class="assembly-content" markdown="1">

### Site Preparation
1. **Location Selection**: Clear view of sky for solar panel
2. **Mounting**: Secure pole or structure installation
3. **Network Setup**: WiFi coverage area verification
4. **Sensor Placement**: Optimal positioning for accurate readings

### Configuration
1. **WiFi Credentials**: Connect to local network infrastructure
2. **MQTT Broker**: Configure cloud or local message broker
3. **Alert Thresholds**: Set customized warning and critical levels
4. **Sampling Intervals**: Optimize for battery life vs. data resolution

</div>
</details>

# Environmental Data Analysis & Visualization

## Real-time Sensor Data Plots

### Multi-parameter Time Series Analysis
```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Generate sample environmental data (24 hours)
time_range = pd.date_range(start='2024-01-01', periods=288, freq='5min')
np.random.seed(42)

# Realistic environmental patterns
temperature = 18 + 8 * np.sin(2 * np.pi * np.arange(288) / 288) + np.random.normal(0, 0.5, 288)
humidity = 65 + 20 * np.sin(2 * np.pi * np.arange(288) / 288 + np.pi) + np.random.normal(0, 2, 288)
pressure = 1013 + 3 * np.sin(2 * np.pi * np.arange(288) / 288 + np.pi/4) + np.random.normal(0, 0.8, 288)
soil_moisture = 45 + 10 * np.sin(2 * np.pi * np.arange(288) / 288 + np.pi/2) + np.random.normal(0, 1.5, 288)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# Temperature
ax1.plot(time_range, temperature, 'r-', linewidth=1.5, alpha=0.8)
ax1.axhline(y=25, color='orange', linestyle='--', alpha=0.7, label='High Threshold')
ax1.axhline(y=15, color='blue', linestyle='--', alpha=0.7, label='Low Threshold')
ax1.set_ylabel('Temperature (°C)')
ax1.set_title('Temperature Monitoring')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Humidity
ax2.plot(time_range, humidity, 'b-', linewidth=1.5, alpha=0.8)
ax2.axhline(y=80, color='red', linestyle='--', alpha=0.7, label='High Alert')
ax2.axhline(y=40, color='orange', linestyle='--', alpha=0.7, label='Low Alert')
ax2.set_ylabel('Humidity (%)')
ax2.set_title('Relative Humidity')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Atmospheric Pressure
ax3.plot(time_range, pressure, 'g-', linewidth=1.5, alpha=0.8)
ax3.set_ylabel('Pressure (hPa)')
ax3.set_title('Atmospheric Pressure')
ax3.grid(True, alpha=0.3)

# Soil Moisture
ax4.plot(time_range, soil_moisture, 'brown', linewidth=1.5, alpha=0.8)
ax4.axhline(y=30, color='red', linestyle='--', alpha=0.7, label='Irrigation Needed')
ax4.axhline(y=60, color='blue', linestyle='--', alpha=0.7, label='Optimal Range')
ax4.set_ylabel('Soil Moisture (%)')
ax4.set_title('Soil Moisture Content')
ax4.set_xlabel('Time')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.xticks(rotation=45)
plt.show()
```

### Sensor Correlation Analysis
```python
# Correlation matrix and scatter plots
data = pd.DataFrame({
    'Temperature': temperature,
    'Humidity': humidity,
    'Pressure': pressure,
    'Soil_Moisture': soil_moisture
})

# Calculate correlation matrix
correlation_matrix = data.corr()

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

# Correlation heatmap
im = ax1.imshow(correlation_matrix, cmap='coolwarm', vmin=-1, vmax=1)
ax1.set_xticks(range(len(correlation_matrix.columns)))
ax1.set_yticks(range(len(correlation_matrix.columns)))
ax1.set_xticklabels(correlation_matrix.columns, rotation=45)
ax1.set_yticklabels(correlation_matrix.columns)
ax1.set_title('Sensor Data Correlation Matrix')

# Add correlation values to heatmap
for i in range(len(correlation_matrix.columns)):
    for j in range(len(correlation_matrix.columns)):
        ax1.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}', 
                ha='center', va='center', color='white' if abs(correlation_matrix.iloc[i, j]) > 0.5 else 'black')

plt.colorbar(im, ax=ax1)

# Temperature vs Humidity scatter
ax2.scatter(temperature, humidity, alpha=0.6, c='blue', s=20)
ax2.set_xlabel('Temperature (°C)')
ax2.set_ylabel('Humidity (%)')
ax2.set_title('Temperature vs Humidity')
ax2.grid(True, alpha=0.3)

# Pressure vs Temperature
ax3.scatter(pressure, temperature, alpha=0.6, c='green', s=20)
ax3.set_xlabel('Pressure (hPa)')
ax3.set_ylabel('Temperature (°C)')
ax3.set_title('Pressure vs Temperature')
ax3.grid(True, alpha=0.3)

# Soil Moisture Distribution
ax4.hist(soil_moisture, bins=20, alpha=0.7, color='brown', edgecolor='black')
ax4.axvline(x=np.mean(soil_moisture), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(soil_moisture):.1f}%')
ax4.set_xlabel('Soil Moisture (%)')
ax4.set_ylabel('Frequency')
ax4.set_title('Soil Moisture Distribution')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### Power Management Analysis
```python
# Battery and solar charging analysis
hours = np.arange(0, 24, 0.5)
solar_irradiance = np.maximum(0, np.sin(np.pi * (hours - 6) / 12))  # Daylight hours
solar_power = solar_irradiance * 2.5  # Watts peak

# Battery simulation
battery_capacity = 2000  # mAh
consumption_rate = 85    # mA average
charging_efficiency = 0.85

battery_level = []
current_charge = battery_capacity

for hour in hours:
    solar_hour = int(hour * 2) % len(solar_irradiance)
    charging_current = solar_power[solar_hour] * 200 * charging_efficiency  # mA
    net_current = charging_current - consumption_rate
    current_charge += net_current * 0.5  # 0.5 hour intervals
    current_charge = max(0, min(battery_capacity, current_charge))
    battery_level.append(current_charge)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

# Solar irradiance
ax1.fill_between(hours, solar_irradiance, alpha=0.6, color='gold', label='Solar Irradiance')
ax1.set_ylabel('Relative Irradiance')
ax1.set_title('Solar Energy Availability')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Power generation vs consumption
ax2.plot(hours, solar_power, 'orange', linewidth=2, label='Solar Power Generation')
ax2.axhline(y=consumption_rate/1000*3.7, color='red', linestyle='--', linewidth=2, label='Power Consumption')
ax2.set_ylabel('Power (W)')
ax2.set_title('Power Generation vs Consumption')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Battery level
battery_percentage = [(level/battery_capacity)*100 for level in battery_level]
ax3.plot(hours, battery_percentage, 'green', linewidth=2, label='Battery Level')
ax3.axhline(y=20, color='red', linestyle='--', alpha=0.7, label='Low Battery Alert')
ax3.axhline(y=80, color='blue', linestyle='--', alpha=0.7, label='Optimal Range')
ax3.set_xlabel('Hour of Day')
ax3.set_ylabel('Battery Level (%)')
ax3.set_title('Battery Charge Level Over 24 Hours')
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.set_ylim(0, 100)

plt.tight_layout()
plt.show()
```

### Data Quality & System Health Monitoring
```python
# System performance metrics
days = range(1, 31)  # 30 days of operation
uptime = np.random.normal(99.5, 0.8, 30)
uptime = np.clip(uptime, 95, 100)

packet_loss = np.random.exponential(0.3, 30)
packet_loss = np.clip(packet_loss, 0, 2)

sensor_drift = np.cumsum(np.random.normal(0, 0.02, 30))
sensor_drift = np.clip(sensor_drift, -0.5, 0.5)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

# System uptime
ax1.plot(days, uptime, 'g-', linewidth=2, marker='o', markersize=4)
ax1.axhline(y=99, color='orange', linestyle='--', alpha=0.7, label='Target Uptime')
ax1.set_ylabel('Uptime (%)')
ax1.set_title('System Uptime Performance')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_ylim(95, 100)

# Data transmission reliability
ax2.plot(days, packet_loss, 'r-', linewidth=2, marker='s', markersize=4)
ax2.axhline(y=1, color='orange', linestyle='--', alpha=0.7, label='Acceptable Loss')
ax2.set_ylabel('Packet Loss (%)')
ax2.set_title('Data Transmission Reliability')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Sensor calibration drift
ax3.plot(days, sensor_drift, 'purple', linewidth=2, marker='^', markersize=4)
ax3.axhline(y=0.3, color='red', linestyle='--', alpha=0.7, label='Recalibration Needed')
ax3.axhline(y=-0.3, color='red', linestyle='--', alpha=0.7)
ax3.set_ylabel('Calibration Drift (°C)')
ax3.set_title('Temperature Sensor Drift')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Alert frequency
alert_types = ['Temperature', 'Humidity', 'Soil Moisture', 'Battery', 'Connectivity']
alert_counts = [12, 8, 15, 3, 5]
colors = ['red', 'blue', 'brown', 'orange', 'purple']

bars = ax4.bar(alert_types, alert_counts, color=colors, alpha=0.7)
ax4.set_ylabel('Alert Count (30 days)')
ax4.set_title('Alert Frequency by Type')
ax4.tick_params(axis='x', rotation=45)

for bar, count in zip(bars, alert_counts):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, 
             str(count), ha='center', va='bottom')

plt.tight_layout()
plt.show()
```

## Performance Results

### Accuracy Validation
- **Temperature**: ±0.3°C compared to reference thermometer
- **Humidity**: ±3% compared to professional hygrometer
- **Pressure**: ±0.5 hPa compared to reference weather station
- **Soil Moisture**: ±5% validated with gravimetric method

### Reliability Metrics
- **Uptime**: 99.7% over 6-month field test
- **Data Loss**: <0.1% with redundant storage systems
- **Battery Life**: 96 hours without solar charging
- **Weather Resistance**: Survived -20°C to +45°C conditions

## Applications

### Agriculture
- **Irrigation Control**: Automated watering based on soil moisture
- **Crop Monitoring**: Growth condition optimization
- **Pest Management**: Environmental condition correlation
- **Yield Prediction**: Data-driven harvest planning

### Research
- **Climate Studies**: Long-term environmental data collection
- **Ecosystem Monitoring**: Habitat condition assessment
- **Weather Stations**: Meteorological data networks
- **Urban Planning**: Microclimate analysis

### Commercial
- **Greenhouse Automation**: Optimal growing condition maintenance
- **Solar Farm Monitoring**: Weather impact on energy production
- **Construction Sites**: Environmental compliance monitoring
- **Event Planning**: Weather-dependent activity management

## Future Enhancements

### Hardware Improvements
- **LoRaWAN Integration**: Extended range communication
- **Additional Sensors**: CO2, UV index, particulate matter
- **Edge AI Processing**: On-device machine learning
- **Modular Design**: Plug-and-play sensor modules

### Software Features
- **Machine Learning**: Predictive analytics and pattern recognition
- **Voice Integration**: Alexa/Google Assistant compatibility
- **Blockchain**: Secure data provenance and sharing
- **AR Visualization**: Augmented reality data overlay

## Lessons Learned

### Hardware Design
1. **Waterproofing**: Cable glands are critical failure points
2. **Power Management**: Solar charging requires MPPT for efficiency
3. **Sensor Placement**: Wind affects temperature readings significantly
4. **PCB Design**: Ground planes essential for noise reduction

### Software Development
1. **Error Handling**: Network failures are common in remote locations
2. **Data Validation**: Sensor drift detection prevents bad data
3. **Security**: IoT devices are attractive targets for attacks
4. **Scalability**: Database design affects query performance

