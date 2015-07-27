
DROP TABLE IF EXISTS emp;
CREATE TABLE emp
   ( emp_id integer PRIMARY KEY,
     emp_name character varying,
     manager_id integer);

INSERT INTO emp VALUES
   (1,'Tim Cook',NULL),
   (2,'Bob Mansfield',1),
   (3,'Scott Forstall',1),
   (4,'Ronald Johnson',1),
   (5,'Steve Zadesky',2),
   (6,'Dan Ricco',2),
   (7,'John Gilley',5),
   (8,'Nancy Lane',5),
   (9,'Cathy Johnson',5),
   (10,'Petery Sully',9);
   

-- Print Employee Name, Manager Name and people reporting to Employee
SELECT
   e.emp_name "Employee", 
   m.emp_name "Employee's Manager", 
   (SELECT 
      STRING_AGG(r.emp_name,' | ') 
    FROM 
       emp r 
    WHERE 
	r.manager_id=e.emp_id) "People Reporting to Employee"
FROM
   emp e
   LEFT JOIN
      emp m
   ON 
   e.manager_id=m.emp_id;	