import numpy as np
import pandas as pd
from datetime import datetime

# Initialize data structures as empty lists first
students_data = []
teachers_data = []
attendance_data = []
marks_data = []


def add_student():
    """Add a new student to the system"""
    print("\n--- Add New Student ---")
    student_id = len(students_data) + 1001
    name = input("Enter student name: ")
    age = int(input("Enter age: "))
    grade = input("Enter grade (e.g., A, B, C): ")
    class_name = input("Enter class (e.g., 10A, 9B): ")
    address = input("Enter address: ")
    phone = input("Enter phone number: ")

    student = {
        'student_id': student_id,
        'name': name,
        'age': age,
        'grade': grade,
        'class': class_name,
        'address': address,
        'phone': phone
    }
    students_data.append(student)
    print(f"Student added successfully with ID: {student_id}")


def add_teacher():
    """Add a new teacher to the system"""
    print("\n--- Add New Teacher ---")
    teacher_id = len(teachers_data) + 2001
    name = input("Enter teacher name: ")
    subject = input("Enter subject: ")
    qualification = input("Enter qualification: ")
    phone = input("Enter phone number: ")
    salary = float(input("Enter salary: "))

    teacher = {
        'teacher_id': teacher_id,
        'name': name,
        'subject': subject,
        'qualification': qualification,
        'phone': phone,
        'salary': salary
    }
    teachers_data.append(teacher)
    print(f"Teacher added successfully with ID: {teacher_id}")


def view_students():
    """View all students"""
    if not students_data:
        print("\nNo students found!")
    else:
        print("\n--- Students List ---")
        df = pd.DataFrame(students_data)
        print(df.to_string(index=False))


def view_teachers():
    """View all teachers"""
    if not teachers_data:
        print("\nNo teachers found!")
    else:
        print("\n--- Teachers List ---")
        df = pd.DataFrame(teachers_data)
        print(df.to_string(index=False))


def search_student():
    """Search for a student by ID or name"""
    print("\n--- Search Student ---")
    print("1. Search by ID")
    print("2. Search by Name")
    choice = input("Enter your choice: ")

    if choice == '1':
        try:
            student_id = int(input("Enter student ID: "))
            df = pd.DataFrame(students_data)
            result = df[df['student_id'] == student_id]
        except:
            print("Invalid input!")
            return
    elif choice == '2':
        name = input("Enter student name: ")
        df = pd.DataFrame(students_data)
        result = df[df['name'].str.contains(name, case=False, na=False)]
    else:
        print("Invalid choice!")
        return

    if result.empty:
        print("No student found!")
    else:
        print("\n--- Search Results ---")
        print(result.to_string(index=False))


def mark_attendance():
    """Mark attendance for students"""
    print("\n--- Mark Attendance ---")
    date = datetime.now().strftime("%Y-%m-%d")
    print(f"Date: {date}")

    if not students_data:
        print("No students to mark attendance!")
        return

    for student in students_data:
        print(f"\nStudent: {student['name']} (ID: {student['student_id']})")
        status = input("Enter status (P for Present, A for Absent): ").upper()

        if status in ['P', 'A']:
            attendance = {
                'date': date,
                'student_id': student['student_id'],
                'student_name': student['name'],
                'status': 'Present' if status == 'P' else 'Absent'
            }
            attendance_data.append(attendance)

    print("Attendance marked successfully!")


def view_attendance():
    """View attendance records"""
    print("\n--- Attendance Records ---")
    if not attendance_data:
        print("No attendance records found!")
        return

    df = pd.DataFrame(attendance_data)
    print(df.to_string(index=False))


def add_marks():
    """Add marks for students"""
    print("\n--- Add Marks ---")
    if not students_data:
        print("No students found!")
        return

    try:
        student_id = int(input("Enter student ID: "))
        student = None
        for s in students_data:
            if s['student_id'] == student_id:
                student = s
                break

        if student is None:
            print("Student not found!")
            return

        subject = input("Enter subject: ")
        exam_type = input("Enter exam type (Mid-term/Final/Quiz): ")
        marks = float(input("Enter marks (0-100): "))

        if marks < 0 or marks > 100:
            print("Marks should be between 0 and 100!")
            return

        mark_entry = {
            'student_id': student_id,
            'student_name': student['name'],
            'subject': subject,
            'marks': marks,
            'exam_type': exam_type,
            'date': datetime.now().strftime("%Y-%m-%d")
        }
        marks_data.append(mark_entry)
        print("Marks added successfully!")
    except ValueError:
        print("Invalid input! Please enter correct values.")


def view_marks():
    """View marks for all students"""
    print("\n--- Marks Records ---")
    if not marks_data:
        print("No marks records found!")
        return

    df = pd.DataFrame(marks_data)

    # Calculate statistics using numpy
    if not marks_data:
        print("No marks data available!")
    else:
        marks_array = np.array([m['marks'] for m in marks_data])
        print(f"\nMarks Statistics:")
        print(f"Average Marks: {np.mean(marks_array):.2f}")
        print(f"Highest Marks: {np.max(marks_array)}")
        print(f"Lowest Marks: {np.min(marks_array)}")
        print(f"Standard Deviation: {np.std(marks_array):.2f}")
        print(f"Total Entries: {len(marks_array)}")

    print("\n--- Detailed Marks ---")
    print(df.to_string(index=False))


def student_performance():
    """Analyze student performance"""
    print("\n--- Student Performance Analysis ---")

    if not marks_data:
        print("No marks data available!")
        return

    df = pd.DataFrame(marks_data)

    # Group by student and calculate average marks
    performance = df.groupby(['student_id', 'student_name'])['marks'].agg(['mean', 'max', 'min', 'count']).round(2)
    performance.columns = ['Average', 'Highest', 'Lowest', 'Total Exams']
    performance = performance.reset_index()

    print("\nPerformance Summary:")
    print(performance.to_string(index=False))


def delete_student():
    """Delete a student from the system"""
    print("\n--- Delete Student ---")
    try:
        student_id = int(input("Enter student ID to delete: "))

        # Find student
        student_found = False
        for i, student in enumerate(students_data):
            if student['student_id'] == student_id:
                students_data.pop(i)
                student_found = True
                break

        if student_found:
            # Remove related records
            global attendance_data, marks_data
            attendance_data = [a for a in attendance_data if a['student_id'] != student_id]
            marks_data = [m for m in marks_data if m['student_id'] != student_id]
            print("Student deleted successfully!")
        else:
            print("Student not found!")
    except ValueError:
        print("Invalid input!")


def generate_report():
    """Generate school report"""
    print("\n--- School Report ---")
    print(f"Total Students: {len(students_data)}")
    print(f"Total Teachers: {len(teachers_data)}")

    if students_data:
        df_students = pd.DataFrame(students_data)
        print(f"\nAverage Student Age: {df_students['age'].mean():.1f}")
        print(f"Student Age Range: {df_students['age'].min()} - {df_students['age'].max()}")

        # Class distribution
        class_dist = df_students['class'].value_counts()
        print(f"\nClass Distribution:")
        for class_name, count in class_dist.items():
            print(f"  Class {class_name}: {count} students")

    if marks_data:
        df_marks = pd.DataFrame(marks_data)
        print(f"\nOverall Average Marks: {df_marks['marks'].mean():.2f}")

        # Subject wise performance
        subject_perf = df_marks.groupby('subject')['marks'].agg(['mean', 'max', 'min']).round(2)
        print(f"\nSubject-wise Performance:")
        print(subject_perf.to_string())

    if teachers_data:
        df_teachers = pd.DataFrame(teachers_data)
        print(f"\nAverage Teacher Salary: ${df_teachers['salary'].mean():.2f}")


def backup_data():
    """Backup all data to CSV files"""
    print("\n--- Backup Data ---")
    try:
        if students_data:
            pd.DataFrame(students_data).to_csv('students_backup.csv', index=False)
        if teachers_data:
            pd.DataFrame(teachers_data).to_csv('teachers_backup.csv', index=False)
        if attendance_data:
            pd.DataFrame(attendance_data).to_csv('attendance_backup.csv', index=False)
        if marks_data:
            pd.DataFrame(marks_data).to_csv('marks_backup.csv', index=False)
        print("Data backed up successfully to CSV files!")
    except Exception as e:
        print(f"Error during backup: {e}")


def main_menu():
    """Display main menu and handle user input"""
    while True:
        print("\n" + "=" * 50)
        print("SCHOOL MANAGEMENT SYSTEM")
        print("=" * 50)
        print("1. Add Student")
        print("2. Add Teacher")
        print("3. View All Students")
        print("4. View All Teachers")
        print("5. Search Student")
        print("6. Mark Attendance")
        print("7. View Attendance")
        print("8. Add Marks")
        print("9. View Marks")
        print("10. Student Performance Analysis")
        print("11. Delete Student")
        print("12. Generate School Report")
        print("13. Backup Data")
        print("14. Exit")
        print("=" * 50)

        choice = input("Enter your choice (1-14): ")

        if choice == '1':
            add_student()
        elif choice == '2':
            add_teacher()
        elif choice == '3':
            view_students()
        elif choice == '4':
            view_teachers()
        elif choice == '5':
            search_student()
        elif choice == '6':
            mark_attendance()
        elif choice == '7':
            view_attendance()
        elif choice == '8':
            add_marks()
        elif choice == '9':
            view_marks()
        elif choice == '10':
            student_performance()
        elif choice == '11':
            delete_student()
        elif choice == '12':
            generate_report()
        elif choice == '13':
            backup_data()
        elif choice == '14':
            # Ask for backup before exit
            backup = input("Do you want to backup data before exit? (y/n): ").lower()
            if backup == 'y':
                backup_data()
            print("\nThank you for using School Management System!")
            break
        else:
            print("\nInvalid choice! Please try again.")

        input("\nPress Enter to continue...")


# Run the program
if __name__ == "__main__":
    print("Welcome to School Management System!")
    print("This system uses NumPy and Pandas for data management.\n")
    main_menu()