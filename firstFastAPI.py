from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Define the Student model using Pydantic
class Student(BaseModel):
    name: str
    age: int
    department: str

# Initial student data randomly 
students = [
    {"name": "Ahmet", "age": 29, "department": "Chemisty"},
    {"name": "Mehmed", "age": 30, "department": "AI"},
    {"name": "Ayşe", "age": 23, "department": "EEE"},
    {"name": "Selma", "age": 22, "department": "Finance"},
    # Add more students here
]

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Student API!"}

# Get all students
@app.get("/students/", response_model=List[Student])
def get_all_students():
    return students

# Get a student by ID
@app.get("/students/{id}", response_model=Student)
def get_student_by_id(id: int):
    try:
        student = students[id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Create a new student
@app.post("/students/", response_model=Student)
def create_student(student: Student):
    students.append(student.dict())
    return student

# Update a student by ID
@app.put("/students/{id}", response_model=Student)
def update_student(id: int, student: Student):
    try:
        students[id] = student.dict()
    except IndexError:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Delete a student by the ID
@app.delete("/students/{id}")
def delete_student(id: int):
    try:
        deleted_student = students.pop(id)
    except IndexError:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "message": "Student deleted successfully",
        "deleted_student": deleted_student,
        "students_after_delete": students
    }