-- Average heart rate by activity type
SELECT AVG(avg_hr), type
FROM activities
GROUP BY type;

-- Total training load by month
SELECT SUM(training_load), strftime('%Y-%m', start_time) AS date
FROM activities
GROUP BY date;

-- Rowing sessions with above-average training load
SELECT name, start_time, training_load
FROM activities
WHERE type = 'rowing_v2'
AND training_load > (
    SELECT AVG(training_load) FROM activities WHERE type = 'rowing_v2'
);