-- Average heart rate by activity type
SELECT AVG(avg_hr), type
FROM activities
GROUP BY type;

-- Total training load by month
SELECT SUM(training_load), strftime('%Y-%m', start_time) AS date
FROM activities
GROUP BY date;