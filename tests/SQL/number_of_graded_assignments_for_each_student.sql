SELECT student_id, COUNT(*) AS graded_assignments_count
FROM assignments
WHERE grade IS NOT NULL
GROUP BY student_id;
