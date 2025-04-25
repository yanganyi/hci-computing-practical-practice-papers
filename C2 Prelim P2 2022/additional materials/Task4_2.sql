SELECT 
    Student.Name, 
    Student.Gender, 
    StudentHealthRecord.Weight, 
    StudentHealthRecord.Height
FROM 
    Student
LEFT JOIN 
    StudentHealthRecord ON Student.StudentID = StudentHealthRecord.StudentID
ORDER BY 
    Student.Gender ASC, 
    Student.Name DESC;