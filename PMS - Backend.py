import psycopg2
import os

class Database:
    def __init__(self, db_params):
        self.conn = psycopg2.connect(**db_params)
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    # Employee CRUD
    def create_employee(self, name, email, job_role):
        self.cur.execute(
            "INSERT INTO employees (name, email, job_role) VALUES (%s, %s, %s)",
            (name, email, job_role)
        )

    def get_all_employees(self):
        self.cur.execute("SELECT * FROM employees")
        return self.cur.fetchall()

    def get_employee_by_id(self, employee_id):
        self.cur.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
        return self.cur.fetchone()

    def update_employee(self, employee_id, name, email, job_role):
        self.cur.execute(
            "UPDATE employees SET name = %s, email = %s, job_role = %s WHERE employee_id = %s",
            (name, email, job_role, employee_id)
        )

    def delete_employee(self, employee_id):
        self.cur.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))

    # Task CRUD
    def create_task(self, employee_id, description, priority, status, outcome, date, duration):
        self.cur.execute(
            """
            INSERT INTO tasks (employee_id, task_description, priority, status, outcome, date, duration_hours)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (employee_id, description, priority, status, outcome, date, duration)
        )

    def get_tasks_by_employee(self, employee_id):
        self.cur.execute("SELECT * FROM tasks WHERE employee_id = %s", (employee_id,))
        return self.cur.fetchall()

    def update_task(self, task_id, description, priority, status, outcome, date, duration):
        self.cur.execute(
            """
            UPDATE tasks
            SET task_description = %s, priority = %s, status = %s, outcome = %s, date = %s, duration_hours = %s
            WHERE task_id = %s
            """,
            (description, priority, status, outcome, date, duration, task_id)
        )

    def delete_task(self, task_id):
        self.cur.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))

    # Goal CRUD
    def create_goal(self, employee_id, description, target_date, status):
        self.cur.execute(
            "INSERT INTO goals (employee_id, goal_description, target_date, status) VALUES (%s, %s, %s, %s)",
            (employee_id, description, target_date, status)
        )

    def get_goals_by_employee(self, employee_id):
        self.cur.execute("SELECT * FROM goals WHERE employee_id = %s", (employee_id,))
        return self.cur.fetchall()

    # Business Insights
    def get_task_counts(self):
        self.cur.execute(
            """
            SELECT e.name, COUNT(t.task_id)
            FROM employees e
            LEFT JOIN tasks t ON e.employee_id = t.employee_id
            GROUP BY e.name
            """
        )
        return self.cur.fetchall()

    def get_total_hours(self):
        self.cur.execute(
            """
            SELECT e.name, SUM(t.duration_hours)
            FROM employees e
            LEFT JOIN tasks t ON e.employee_id = t.employee_id
            GROUP BY e.name
            """
        )
        return self.cur.fetchall()

    def get_avg_task_duration(self):
        self.cur.execute(
            """
            SELECT e.name, AVG(t.duration_hours)
            FROM employees e
            JOIN tasks t ON e.employee_id = t.employee_id
            GROUP BY e.name
            """
        )
        return self.cur.fetchall()

    def get_min_max_task_duration(self):
        self.cur.execute(
            """
            SELECT e.name, MIN(t.duration_hours), MAX(t.duration_hours)
            FROM employees e
            JOIN tasks t ON e.employee_id = t.employee_id
            GROUP BY e.name
            """
        )
        return self.cur.fetchall()
