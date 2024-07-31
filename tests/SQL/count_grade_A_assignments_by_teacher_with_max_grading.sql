-- Step 1: Find the teacher with the maximum number of graded assignments
WITH TeacherMaxGradedAssignments AS (
    SELECT teacher_id, COUNT(*) AS graded_count
    FROM Assignment
    WHERE grade IS NOT NULL
    GROUP BY teacher_id
    ORDER BY graded_count DESC
    LIMIT 1
)

-- Step 2: Count the number of assignments graded with an "A" by this teacher
SELECT COUNT(*) AS grade_A_assignments_count
FROM Assignment
WHERE teacher_id = (SELECT teacher_id FROM TeacherMaxGradedAssignments)
  AND grade = 'A';
