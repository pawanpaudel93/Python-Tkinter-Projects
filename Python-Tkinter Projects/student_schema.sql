BEGIN;
--Create Student Table--
create table Student (studid int PRIMARY KEY,
  first_name VARCHAR(20),
  middle_name VARCHAR(20),
  last_name VARCHAR(20),
  address VARCHAR(30),
  phone_no NUMERIC(15,0),
  dob date,
  class VARCHAR(15),
  rollno VARCHAR(20),
  gender VARCHAR(10),
  photo VARCHAR(100)
);
COMMIT;