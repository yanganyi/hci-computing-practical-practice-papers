SELECT 
    Student.Gender,
    COUNT(Student.StudentID) AS TotalStudents,
    AVG(StudentHealthRecord.Weight) AS AverageWeight,
    AVG(StudentHealthRecord.Height) AS AverageHeight
FROM 
    Student
LEFT JOIN 
    StudentHealthRecord ON Student.StudentID = StudentHealthRecord.StudentID
GROUP BY 
    Student.Gender;