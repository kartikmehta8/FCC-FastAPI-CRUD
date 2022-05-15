#RUN - python3 -m uvicorn API:app --reload

from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "Kartik Mehta",
        "age": 19,
        "college": "KIET"
    },
    2: {
        "name": "Kunal Mehta",
        "age": 25,
        "college": "AKGEC"
    }
}

#CLASS FOR POST METHOD DEMONSTRATION
class Student(BaseModel):
    name: str
    age: int
    college: str

#CLASS FOR PUT METHOD DEMONSTRATION
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    college: Optional[str] = None

#HOME PAGE 
@app.get("/")
def index():
    return {"creator": "Kartik Mehta"}

#GET REQUEST FOR PATICULAR STUDENT INFORMATION QUERIED BY ID
@app.get("/student/{id}")
def getStudent(id: int = Path(None, description = "Specify the ID of the Student", gt = 0, le = 10)):
    return students[id]

#GET REQUEST FOR PARTICULAR STUDENT INFORMATION QUERIED BY NAME
@app.get("/name")
def getStudentByName(*, name: Optional[str] = None):
    for studentId in students:
        if students[studentId]["name"] == name:
            return students[studentId]
    return {"Data": "Not Found"}

#COMBINING PATH PARAMETER AND QUERY PARAMETER
@app.get("/student-name/{studentId}")
def getStudentByNameAndID(*, studentId: int ,name: Optional[str] = None):
    if students[studentId]["name"] == name:
        return students[studentId]
    return {"Data": "Not Found"}

#POST REQUEST FOR ADDING A NEW STUDENT DETAIL
@app.post("/new-student/{studentId}")
def createStudent(studentId: int, student: Student):
    if studentId in students:
        return {"Error": "ID Exists"}
    students[studentId] = student
    return students[studentId]

#UPDATE CURRENT STUDENT INFORMATION
@app.put("/update-student/{studentId}")
def updateStudent(studentId: int, student: UpdateStudent):
    if studentId not in students:
        return {"Error": "ID does not exist"}
    
    if student.name != None:
        students[studentId].name = student.name
    if student.age != None:
        students[studentId].age = student.age
    if student.college != None:
        students[studentId].college = student.college
    
    return students[studentId]

#DELETING THE EXISTING STUDENT DATA
@app.delete("/delete/{studentId}")
def deleteStudent(studentId: int):
    if studentId not in students:
        return {"Error": "ID doest not exist"}

    del students[studentId]
    return {"Success": "Student Information deleted successfully!"}