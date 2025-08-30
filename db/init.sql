-- Create the students table
CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(100) NOT NULL,
  email VARCHAR(120) NOT NULL,
  phone VARCHAR(30) NOT NULL,
  course VARCHAR(100) NOT NULL,
  registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional seed (comment out if not needed)
-- INSERT INTO students (full_name, email, phone, course) VALUES
-- ('Jane Doe', 'jane@example.com', '+966500000001', 'Azure Fundamentals'),
-- ('John Smith', 'john@example.com', '+201100000002', 'Docker Basics');
