Bonus Allocation System

Overview

The Bonus Allocation System automates the process of awarding attendance-based bonus marks to students. It also considers HoD (Head of Department) bonus and extra bonus marks to optimize student grades and SPI (Semester Performance Index). The system processes an input Excel file, applies bonus allocation rules, and generates a processed output Excel file with updated grades and SPI calculations.

Features

Upload an Excel file containing student marks.

Automatic bonus allocation based on attendance.

HoD Bonus applied if a student fails only one subject by 1 or 2 marks.

Extra Bonus applied if a student passes all subjects.

Grade Calculation based on predefined grading rules.

SPI Calculation for each student.

Downloadable processed Excel file.

Simple web-based UI for easy file upload and download.

Technologies Used

Python (for data processing)

Flask (for the web interface)

Pandas (for Excel file manipulation)

HTML/CSS (for frontend UI)

Installation & Setup

Prerequisites

Ensure you have the following installed:

Python (version 3.8 or later)

Pip (Python package manager)

Virtual environment (optional but recommended)

Steps to Set Up the Project

create a project folder named attendance bonus system

cd attendance-bonus-system

Create a Virtual Environment (Optional but Recommended)

python -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate    # For Windows

Install Dependencies

pip install -r requirements.txt

Run the Flask Application

python app.py

Access the Web Interface
Open your browser and go to:

http://127.0.0.1:5000

Usage

Upload an Excel file containing student data.

Click "Upload & Process" to apply attendance and HoD bonuses.

Download the processed output Excel file with updated marks, grades, and SPI.

Project Structure

attendance-bonus-system/
│-- app.py               # Flask backend application
│-- templates/
│   │-- index.html       # Web UI for file upload/download
│-- static/
│   │-- styles.css       # Styles for the frontend
│-- uploads/             # Folder for uploaded input files
    │-- input.xlsx       # input excel for processing
│-- processed/           # Folder for processed output files
    │-- input.xlsx       # generated output excel after processing
│-- requirements.txt     # Python dependencies
│-- README.md            # Project documentation

Future Enhancements

Implement AI-based grade prediction.

Add student performance analytics.

Improve the UI with a dashboard for better insights.

Contributors

Dhara Rawal - Lecturer at LJ Polytechnic, Ahmedabad
Bhargav Suthar - Lecturer at LJIET, Ahmedabad
