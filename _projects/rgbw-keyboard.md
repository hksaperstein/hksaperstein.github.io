---
layout: project
title: "RGBW Mechanical Keyboard"
description: "Designing a custom mechanical keyboard from the ground up."
date: 2024-10-15
categories: [Arduino, Electronics, 3D Printing]
featured_image: "/assets/images/projects/rgbw-keyboard/featured.jpg"
github_url: "https://github.com/hksaperstein/keyboard"
demo_url: "#"

# 3D Models - Support for STL, OBJ, GLTF, GLB formats
# models:
#   - file: "/assets/models/line-robot/chassis.gltf"
#     description: "3D printed robot chassis with integrated sensor mounts"
#   - file: "/assets/models/line-robot/wheel-assembly.gltf"
#     description: "Custom wheel assembly with encoder integration"

# Circuit Schematics - PNG, JPG, SVG, PDF formats
schematics:
  - file: "/assets/schematics/rgbw-keyboard/main-circuit.svg"
    description: "Main control circuit with Arduino Uno and motor driver"


# Components and materials list
# components:
#   - name: "Arduino Uno R3"
#     quantity: 1
#     description: "Main microcontroller board"
#     link: "https://store.arduino.cc/products/arduino-uno-rev3"
  
#   - name: "L298N Motor Driver"
#     quantity: 1
#     description: "Dual H-bridge motor driver for DC motors"
#     link: "https://example.com/l298n"
    
#   - name: "IR Sensor Array"
#     quantity: 1
#     description: "5-channel infrared sensor array for line detection"
    
#   - name: "DC Geared Motors (6V)"
#     quantity: 2
#     description: "High-torque geared motors with mounting brackets"
    
#   - name: "Robot Wheels"
#     quantity: 2
#     description: "65mm diameter wheels with rubber tires"
    
#   - name: "LiPo Battery (7.4V 2200mAh)"
#     quantity: 1
#     description: "Rechargeable battery pack with JST connector"
    
#   - name: "Ultrasonic Sensor HC-SR04"
#     quantity: 1
#     description: "For obstacle detection and avoidance"
    
#   - name: "Breadboard & Jumper Wires"
#     quantity: 1
#     description: "For prototyping and connections"

# Media gallery with images, videos, and GIFs
gallery:
  - type: "image"
    file: "/assets/images/projects/rgbw-keyboard/featured.jpg"
    description: "Line following robot overview"
---

## Project Overview

This project was an attempt to solve a real world problem. I wanted a mechanical keyboard with a 65% compact, in-line layout, hot-swap mechanical switches, and most importantly, backlit with RGB-W LEDs

## Key Features

### KEY Features
- **RGBW LEDs**: RGB LEDs with a dedicated W channel for white. Cool, neutral, and warm white are all considered.
- **Sensor Fusion**: Uses a 5-sensor IR array for accurate line position detection
- **Adaptive Speed**: Automatically adjusts speed based on track curvature

### Wireless Monitoring
- **Real-time Telemetry**: Sends sensor data and control parameters via Bluetooth
- **Parameter Tuning**: Live PID parameter adjustment using custom Python GUI
- **Performance Logging**: Records track performance for analysis and optimization

### Safety Features
- **Obstacle Detection**: Ultrasonic sensor for collision avoidance
- **Battery Management**: Low voltage detection and automatic shutdown
- **Emergency Stop**: Wireless emergency stop functionality

## Technical Specifications

| Specification | Value |
|---------------|-------|
| **Microcontroller** | Arduino Uno R3 (ATmega328P) |
| **Operating Voltage** | 7.4V (2S LiPo) |
| **Maximum Speed** | 1.2 m/s |
| **Line Detection Range** | 12cm wide sensor array |
| **Battery Life** | 45 minutes continuous operation |
| **Weight** | 485g |
| **Dimensions** | 18cm x 12cm x 8cm |

## Algorithm Implementation

The robot uses a weighted average algorithm to determine line position:

1. **Sensor Reading**: Five IR sensors provide analog values (0-1023)
2. **Thresholding**: Convert analog values to binary (line/no line)
3. **Position Calculation**: Weighted average gives position (-2 to +2)
4. **PID Control**: Error correction using PID algorithm
5. **Motor Control**: Differential steering based on PID output

# Data Visualization & Analysis

## Real-time Performance Plots



## Performance Results

After extensive testing and PID tuning, the robot achieved:
- **Line Following Accuracy**: 95% on standard tracks
- **Maximum Track Speed**: Successfully follows lines at 80cm/s
- **Curve Handling**: Navigates 90° turns without losing the line
- **Obstacle Response**: Stops within 10cm of detected obstacles

## Lessons Learned

1. **PID Tuning**: Start with proportional control only, then add integral and derivative terms
2. **Sensor Calibration**: Regular calibration is crucial for consistent performance
3. **Power Management**: Use voltage regulators for stable sensor readings
4. **Mechanical Design**: Proper wheel alignment significantly improves tracking accuracy

## Future Improvements

- **Machine Learning**: Implement adaptive PID parameters using reinforcement learning
- **Multi-Line Support**: Add capability to handle intersections and multiple line paths
- **Wireless Communication**: Upgrade to WiFi for remote monitoring and control
- **Advanced Sensors**: Add color sensors for enhanced track detection

## Build Instructions


<details class="assembly-details">
<summary>Assembly Instructions</summary>
<div class="assembly-content" markdown="1">

### Step 1: Mechanical Assembly
1. 3D print the chassis using the provided STL files
2. Mount the motors and wheels to the chassis
3. Install the sensor array at the front of the robot
4. Secure the Arduino and motor driver board

### Step 2: Electronics
1. Follow the circuit schematic to connect all components
2. Use the custom PCB design for a cleaner installation
3. Test all connections before powering on
4. Upload the Arduino code and calibrate sensors

### Step 3: Software Setup
1. Install the Arduino IDE and required libraries
2. Upload the main control code to the Arduino
3. Install Python dependencies for the tuning interface
4. Run initial calibration and PID tuning procedures

</div>
</details>

