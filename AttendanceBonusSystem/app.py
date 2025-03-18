from flask import Flask, render_template, request, send_file
import os
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def get_grade(marks):
    grades = [
        (95, 100, 'O+++', 10), (90, 94, 'O++', 9.5), (85, 89, 'O+', 9),
        (80, 84, 'O', 8.5), (75, 79, 'A++', 8), (70, 74, 'A+', 7.5),
        (65, 69, 'A', 7), (60, 64, 'B++', 6.5), (55, 59, 'B+', 6),
        (50, 54, 'B', 5.5), (45, 49, 'C', 5), (40, 44, 'D', 4.5),
        (35, 39, 'E', 4), (0, 34, 'F', 0)
    ]
    for lower, upper, grade, points in grades:
        if lower <= marks <= upper:
            return grade, points
    return 'F', 0

def process_excel(input_file):
    df = pd.read_excel(input_file)
    
    df['Total Credits'] = df['Theory Credits'].fillna(0) + df['Practical Credits'].fillna(0)
    df['Final Marks'] = df['Theory Marks'].fillna(0) + df['Practical Marks'].fillna(0) + df['Attendance Bonus'].fillna(0)
    
    df[['Grade', 'Grade Points']] = df['Final Marks'].apply(lambda x: pd.Series(get_grade(x)))
    
    # Apply HoD Bonus logic
    df['HoD Bonus'] = 0
    students = df['Student ID'].unique()
    for student in students:
        student_df = df[df['Student ID'] == student]
        failing_subjects = student_df[student_df['Grade'] == 'F']
        if len(failing_subjects) == 1:
            failing_index = failing_subjects.index[0]
            if 33 <= df.loc[failing_index, 'Final Marks'] <= 34:
                df.at[failing_index, 'HoD Bonus'] = min(2, 35 - df.at[failing_index, 'Final Marks'])
                df.at[failing_index, 'Final Marks'] += df.at[failing_index, 'HoD Bonus']

    # Recalculate grades
    df[['Grade', 'Grade Points']] = df['Final Marks'].apply(lambda x: pd.Series(get_grade(x)))
    
    # Extra Bonus if all subjects are passed
    df['Extra Bonus'] = 0
    for student in students:
        student_df = df[df['Student ID'] == student]
        if all(student_df['Grade'] != 'F'):
            df.loc[df['Student ID'] == student, 'Extra Bonus'] = 2

    df['Final Marks'] += df['Extra Bonus']
    df[['Grade', 'Grade Points']] = df['Final Marks'].apply(lambda x: pd.Series(get_grade(x)))  # Recalculate grades

    # SPI Calculation
    spi_values = df.groupby('Student ID').apply(lambda g: (g['Grade Points'] * g['Total Credits']).sum() / g['Total Credits'].sum())
    df['SPI'] = ''
    for student in students:
        last_index = df[df['Student ID'] == student].index[-1]
        df.at[last_index, 'SPI'] = round(spi_values[student], 2)

    output_file = os.path.join(PROCESSED_FOLDER, "output.xlsx")
    df.to_excel(output_file, index=False)
    return output_file

@app.route("/", methods=["GET", "POST"])
def upload_and_process():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith((".xlsx", ".xls")):
            file_path = os.path.join(UPLOAD_FOLDER, "input.xlsx")
            file.save(file_path)

            output_file = process_excel(file_path)
            return send_file(output_file, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
