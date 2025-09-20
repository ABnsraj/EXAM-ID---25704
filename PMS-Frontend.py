import streamlit as st
import pandas as pd
from backend import Database

# --- Database Connection ---
db_params = {
    'dbname': 'performance',
    'user': 'postgres',
    'password': 'Xime@2005',
    'host': 'localhost',
    'port': '5432'
}

# --- App ---
st.set_page_config(page_title="Performance Management System", layout="wide")
st.title("Performance Management System")

menu = [
    "Employee Profiles",
    "Task Tracking",
    "Goal Setting",
    "Leaderboard",
    "Business Insights",
    "Performance Reporting"  # New menu item
]
choice = st.sidebar.selectbox("Menu", menu)

with Database(db_params) as db:
    if choice == "Employee Profiles":
        st.subheader("Employee Profiles")
        employees = db.get_all_employees()
        df_employees = pd.DataFrame(employees, columns=['ID', 'Name', 'Email', 'Job Role'])
        st.dataframe(df_employees)

        with st.expander("Add New Employee"):
            with st.form("new_employee_form"):
                name = st.text_input("Name")
                email = st.text_input("Email")
                job_role = st.text_input("Job Role")
                submitted = st.form_submit_button("Add Employee")
                if submitted:
                    db.create_employee(name, email, job_role)
                    st.success("Employee added successfully!")

    elif choice == "Task Tracking":
        st.subheader("Task Tracking")
        employee_list = db.get_all_employees()
        employee_names = {emp[1]: emp[0] for emp in employee_list}
        selected_employee_name = st.selectbox("Select Employee", list(employee_names.keys()))
        selected_employee_id = employee_names[selected_employee_name]

        tasks = db.get_tasks_by_employee(selected_employee_id)
        df_tasks = pd.DataFrame(tasks, columns=['ID', 'Emp ID', 'Description', 'Priority', 'Status', 'Outcome', 'Date', 'Duration (hrs)', 'Goal ID', 'Approved'])
        st.dataframe(df_tasks)

        with st.expander("Propose New Task"):
            with st.form("new_task_form"):
                description = st.text_area("Task Description")
                priority = st.selectbox("Priority", ["High", "Medium", "Low"])
                status = st.selectbox("Status", ["To Do", "In Progress", "Done"])
                outcome = st.text_input("Outcome")
                date = st.date_input("Date")
                duration = st.number_input("Duration (hours)", min_value=0.0, step=0.5)
                goal_id = st.selectbox("Associated Goal", [g[0] for g in db.get_goals_by_employee(selected_employee_id)])
                submitted = st.form_submit_button("Propose Task")
                if submitted:
                    db.create_task(selected_employee_id, description, priority, status, outcome, date, duration, goal_id, approved=False)
                    st.success("Task proposed! Awaiting manager approval.")

    elif choice == "Goal Setting":
        st.subheader("Goal Setting")
        employee_list = db.get_all_employees()
        employee_names = {emp[1]: emp[0] for emp in employee_list}
        selected_employee_name = st.selectbox("Select Employee", list(employee_names.keys()))
        selected_employee_id = employee_names[selected_employee_name]

        goals = db.get_goals_by_employee(selected_employee_id)
        df_goals = pd.DataFrame(goals, columns=['ID', 'Emp ID', 'Description', 'Target Date', 'Status'])
        st.dataframe(df_goals)

        # Progress bar for each goal
        for _, row in df_goals.iterrows():
            st.write(f"Goal: {row['Description']}")
            progress = db.get_goal_progress(row['ID'])  # Implement in backend
            st.progress(progress)

        with st.expander("Set New Goal"):
            with st.form("new_goal_form"):
                description = st.text_area("Goal Description")
                target_date = st.date_input("Target Date")
                status = st.selectbox("Status", ["Draft", "In Progress", "Completed", "Cancelled"])
                submitted = st.form_submit_button("Set Goal")
                if submitted:
                    db.create_goal(selected_employee_id, description, target_date, status)
                    st.success("Goal set successfully!")

        # Feedback section
        st.markdown("### Provide Feedback")
        goal_ids = [g[0] for g in goals]
        selected_goal_id = st.selectbox("Select Goal for Feedback", goal_ids)
        feedback_text = st.text_area("Feedback")
        if st.button("Submit Feedback"):
            db.add_feedback(selected_employee_id, selected_goal_id, feedback_text)  # Implement in backend
            st.success("Feedback submitted!")

    elif choice == "Leaderboard":
        st.subheader("Leaderboard")
        task_counts = db.get_task_counts()
        df_leaderboard = pd.DataFrame(task_counts, columns=['Employee', 'Tasks Completed'])
        df_leaderboard = df_leaderboard.sort_values(by="Tasks Completed", ascending=False)
        st.dataframe(df_leaderboard)

    elif choice == "Business Insights":
        st.subheader("Business Insights")

        st.markdown("### Task Counts per Employee")
        task_counts = db.get_task_counts()
        df_task_counts = pd.DataFrame(task_counts, columns=['Employee', 'Number of Tasks'])
        st.bar_chart(df_task_counts.set_index('Employee'))

        st.markdown("### Total Hours Worked per Employee")
        total_hours = db.get_total_hours()
        df_total_hours = pd.DataFrame(total_hours, columns=['Employee', 'Total Hours'])
        st.bar_chart(df_total_hours.set_index('Employee'))

        st.markdown("### Average Task Duration per Employee")
        avg_duration = db.get_avg_task_duration()
        df_avg_duration = pd.DataFrame(avg_duration, columns=['Employee', 'Average Duration (hrs)'])
        st.bar_chart(df_avg_duration.set_index('Employee'))

        st.markdown("### Min and Max Task Duration per Employee")
        min_max_duration = db.get_min_max_task_duration()
        df_min_max = pd.DataFrame(min_max_duration, columns=['Employee', 'Min Duration', 'Max Duration'])
        st.dataframe(df_min_max)

    elif choice == "Performance Reporting":
        st.subheader("Performance Reporting")
        employee_list = db.get_all_employees()
        employee_names = {emp[1]: emp[0] for emp in employee_list}
        selected_employee_name = st.selectbox("Select Employee", list(employee_names.keys()))
        selected_employee_id = employee_names[selected_employee_name]

        st.markdown("### Goals History")
        goals = db.get_goals_by_employee(selected_employee_id)
        df_goals = pd.DataFrame(goals, columns=['ID', 'Emp ID', 'Description', 'Target Date', 'Status'])
        st.dataframe(df_goals)

        st.markdown("### Tasks History")
        tasks = db.get_tasks_by_employee(selected_employee_id)
        df_tasks = pd.DataFrame(tasks, columns=['ID', 'Emp ID', 'Description', 'Priority', 'Status', 'Outcome', 'Date', 'Duration (hrs)', 'Goal ID', 'Approved'])
        st.dataframe(df_tasks)

        st.markdown("### Feedback History")
        feedbacks = db.get_feedback_by_employee(selected_employee_id)  # Implement in backend
        df_feedback = pd.DataFrame(feedbacks, columns=['ID', 'Goal ID', 'Feedback', 'Date'])
        st.dataframe(df_feedback)
