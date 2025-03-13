import pymongo

# Establishing connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["quiz_management"]

# Collections
students_col = db["students"]
teachers_col = db["teachers"]
courses_col = db["courses"]

# Functions for Teacher

def add_student():
    name = input("Enter student name: ")
    roll_number = int(input("Enter student roll number: "))
    students_col.insert_one({"name": name, "roll_number": roll_number})
    print("Student added successfully!")

def delete_student():
    roll_number = int(input("Enter student roll number to delete: "))
    students_col.delete_one({"roll_number": roll_number})
    print("Student deleted successfully!")

def view_students():
    print("Students:")
    for student in students_col.find():
        print(student)

def add_course():
    course_name = input("Enter course name: ")
    if courses_col.find_one({"name": course_name}):
        print("Course with the same name already exists!")
    else:
        courses_col.insert_one({"name": course_name, "tests": []})
        print("Course added successfully!")

def delete_course():
    course_name = input("Enter course name to delete: ")
    courses_col.delete_one({"name": course_name})
    print("Course deleted successfully!")

def view_courses():
    print("Courses:")
    for course in courses_col.find():
        print(course)

def update_course():
    course_name = input("Enter course name to update: ")
    new_name = input("Enter new course name: ")
    courses_col.update_one({"name": course_name}, {"$set": {"name": new_name}})
    print("Course updated successfully!")

def add_test():
    course_name = input("Enter course name to add test to: ")
    test_name = input("Enter test name: ")
    questions = []
    while True:
        question_text = input("Enter question text (or type 'done' to finish adding questions): ")
        if question_text.lower() == "done":
            break
        options = []
        for i in range(4):
            option = input(f"Enter option {i+1}: ")
            options.append(option)
        correct_option = int(input("Enter correct option number: "))
        questions.append({"text": question_text, "options": options, "correct_option": correct_option})
    courses_col.update_one({"name": course_name}, {"$push": {"tests": {"name": test_name, "questions": questions}}})
    print("Test added successfully!")

def delete_test():
    course_name = input("Enter course name to delete test from: ")
    test_name = input("Enter test name to delete: ")
    courses_col.update_one({"name": course_name}, {"$pull": {"tests": {"name": test_name}}})
    print("Test deleted successfully!")

def view_tests():
    print("Tests:")
    for course in courses_col.find():
        print(f"Course: {course['name']}")
        for test in course['tests']:
            print(f"Test: {test['name']}")

def update_test():
    course_name = input("Enter course name to update test in: ")
    test_name = input("Enter test name to update: ")
    new_test_name = input("Enter new test name: ")
    courses_col.update_one({"name": course_name, "tests.name": test_name},
                           {"$set": {"tests.$.name": new_test_name}})
    print("Test updated successfully!")

def view_student_marks():
    roll_number = int(input("Enter student's roll number to view marks: "))
    student = students_col.find_one({"roll_number": roll_number})
    if student:
        print(f"Student: {student['name']}, Roll Number: {student['roll_number']}")
        print("\nMarks:")
        print("{:<20} {:<20} {:<10}".format("Course", "Test", "Marks"))
        print("-" * 50)
        for course in courses_col.find():
            for test in course['tests']:
                marks = calculate_marks_for_test(student['_id'], test['_id'])
                print("{:<20} {:<20} {:<10}".format(course['name'], test['name'], marks))
    else:
        print("Student not found!")

# Main menu for Teacher
def teacher_menu():
    while True:
        print("\nTeacher Menu:")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. View Students")
        print("4. Add Course")
        print("5. Delete Course")
        print("6. View Courses")
        print("7. Update Course")
        print("8. Add Test")
        print("9. Delete Test")
        print("10. View Tests")
        print("11. Update Test")
        print("12. View Student marks")
        print("13. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            delete_student()
        elif choice == "3":
            view_students()
        elif choice == "4":
            add_course()
        elif choice == "5":
            delete_course()
        elif choice == "6":
            view_courses()
        elif choice == "7":
            update_course()
        elif choice == "8":
            add_test()
        elif choice == "9":
            delete_test()
        elif choice == "10":
            view_tests()
        elif choice == "11":
            update_test()
        elif choice == "12":
            view_student_marks()
        elif choice == "13":
            break
        else:
            print("Invalid choice! Please try again.")

# Functions for Student
def student_login():
    name = input("Enter your name: ")
    roll_number = int(input("Enter your roll number: "))
    return name, roll_number

def view_tests():
    print("Tests:")
    for course in courses_col.find():
        print(f"Course: {course['name']}")
        for test in course['tests']:
            print(f"Test: {test['name']}")

def take_test(course_name):
    for course in courses_col.find({"name": course_name}):
        total_marks = 0
        obtained_marks = 0
        print(f"Course: {course['name']}")
        for test in course['tests']:
            print(f"Test: {test['name']}")
            for question in test['questions']:
                print(question['text'])
                for i, option in enumerate(question['options']):
                    print(f"{i+1}. {option}")
                answer = int(input("Enter your answer: "))
                if answer == question['correct_option']:
                    obtained_marks += 1
                total_marks += 1
        percentage = (obtained_marks / total_marks) * 100
        if percentage >= 50:
            print("Congratulations! You passed the test.")
        else:
            print("Sorry! You failed the test.")

# Main menu for Student
def student_menu():
    name, roll_number = student_login()
    while True:
        print("\nStudent Menu:")
        print("1. View Tests")
        print("2. Take Test")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_tests()
        elif choice == "2":
            course_name = input("Enter the course name to take test: ")
            take_test(course_name)
        elif choice == "3":
            break
        else:
            print("Invalid choice! Please try again.")

# Main menu
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Teacher Login")
        print("2. Student Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            teacher_menu()
        elif choice == "2":
            student_menu()
        elif choice == "3":
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()
