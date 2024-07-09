--https://leetcode.com/problems/students-and-examinations/description/?envType=study-plan-v2&envId=top-sql-50

--Wrong answer (doesnt give subjects with 0 attempts in examination)
 SELECT val1.student_id, val1.student_name, val1.subject_name, val2.attempts as attended_exams FROM (SELECT student_id, student_name, subject_name FROM Students t1
 CROSS JOIN Subjects t2
 ORDER BY student_id, subject_name) val1
 LEFT JOIN
 (SELECT Examinations.student_id, Examinations.subject_name, Students.student_name, count(1) as attempts FROM Examinations
 JOIN Students ON Students.student_id = Examinations.student_id
  GROUP BY Examinations.student_id, Examinations.subject_name, Students.student_name) val2
 ON val1.student_id = val2.student_id AND val1.subject_name = val2.subject_name


--above soln fixed by using left join and coalesce
SELECT val1.student_id, val1.student_name, val1.subject_name, coalesce(val2.attempts, 0) as attended_exams FROM (SELECT student_id, student_name, subject_name FROM Students t1
 CROSS JOIN Subjects t2
 ORDER BY student_id, subject_name) val1
 LEFT JOIN
 (SELECT Examinations.student_id, Examinations.subject_name, Students.student_name, count(1) as attempts FROM Examinations
 JOIN Students ON Students.student_id = Examinations.student_id
  GROUP BY Examinations.student_id, Examinations.subject_name, Students.student_name) val2
 ON val1.student_id = val2.student_id AND val1.subject_name = val2.subject_name


--other simple solution
SELECT s.student_id, s.student_name, sub.subject_name, COUNT(e.student_id) AS attended_exams
FROM Students s
CROSS JOIN Subjects sub
LEFT JOIN Examinations e ON s.student_id = e.student_id AND sub.subject_name = e.subject_name
GROUP BY s.student_id, s.student_name, sub.subject_name
ORDER BY s.student_id, sub.subject_name;

--more optimized solution
WITH
students_with_subj AS (
SELECT DISTINCT s.student_id,
       s.student_name,
       Subjects.subject_name
FROM Students AS s
CROSS JOIN Subjects)


SELECT s.student_id,
       s.student_name,
       s.subject_name,
       COUNT(e.subject_name) AS attended_exams
FROM students_with_subj AS s
LEFT JOIN Examinations AS e ON e.student_id = s.student_id
                           AND e.subject_name = s.subject_name
GROUP BY s.student_id, s.student_name, s.subject_name
ORDER BY s.student_id, s.subject_name