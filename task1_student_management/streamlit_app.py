import os
import requests
import streamlit as st

API_URL = os.getenv("STUDENT_API_URL", "http://127.0.0.1:5001")
st.set_page_config(page_title="Student Management", page_icon="🎓")
st.title("🎓 Student Management")


def fetch_students():
    response = requests.get(f"{API_URL}/students", timeout=5)
    response.raise_for_status()
    return response.json()


def show_error(response):
    try:
        st.error(response.json().get("error", response.text))
    except ValueError:
        st.error(response.text)


try:
    students = fetch_students()
except requests.RequestException as exc:
    st.error(f"Cannot connect to Flask API at {API_URL}: {exc}")
    st.stop()

st.subheader("All students")
st.dataframe(students, use_container_width=True, hide_index=True)

with st.expander("Add a new student"):
    with st.form("add_student"):
        name = st.text_input("Name")
        department = st.text_input("Department")
        email = st.text_input("Email")
        if st.form_submit_button("Add student"):
            response = requests.post(f"{API_URL}/students", json={"name": name, "department": department, "email": email}, timeout=5)
            if response.ok:
                st.success("Student added")
                st.rerun()
            else:
                show_error(response)

if students:
    by_id = {student["id"]: student for student in students}
    selected_id = st.selectbox("Select a student", list(by_id), format_func=lambda value: f"{value} — {by_id[value]['name']}")
    selected = by_id[selected_id]

    with st.form("edit_student"):
        edit_name = st.text_input("Name", value=selected["name"])
        edit_department = st.text_input("Department", value=selected["department"])
        edit_email = st.text_input("Email", value=selected["email"])
        col1, col2 = st.columns(2)
        with col1:
            update = st.form_submit_button("Update student")
        with col2:
            delete = st.form_submit_button("Delete student")
        if update:
            response = requests.put(f"{API_URL}/students/{selected_id}", json={"name": edit_name, "department": edit_department, "email": edit_email}, timeout=5)
            if response.ok:
                st.success("Student updated")
                st.rerun()
            else:
                show_error(response)
        if delete:
            response = requests.delete(f"{API_URL}/students/{selected_id}", timeout=5)
            if response.ok:
                st.success("Student deleted")
                st.rerun()
            else:
                show_error(response)

