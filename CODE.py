import streamlit as st
import cv2
import os
import pandas as pd
from deepface import DeepFace
from datetime import datetime
from io import BytesIO

# Paths
USERS_FILE = 'users.csv'
FACE_DB_PATH = 'face_db'
ATTENDANCE_DIR = 'attendance'

# Ensure folders exist
os.makedirs(FACE_DB_PATH, exist_ok=True)
os.makedirs(ATTENDANCE_DIR, exist_ok=True)

# Save user image to folder
def save_user_image_streamlit(name):
    cap = cv2.VideoCapture(0)
    st.info("Press SPACE to capture the face. Press Q to quit.")
    img_saved = False

    while not img_saved:
        ret, frame = cap.read()
        cv2.imshow("Press SPACE to capture", frame)
        key = cv2.waitKey(1)

        if key == ord(' '):
            face_file = os.path.join(FACE_DB_PATH, f"{name}.jpg")
            cv2.imwrite(face_file, frame)
            st.success("Face image captured!")
            img_saved = True
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Register face with details
def register_face(name, category, startup, roll_number):
    if not name or not roll_number:
        st.error("Name and Roll Number are required.")
        return

    users_df = pd.read_csv(USERS_FILE) if os.path.exists(USERS_FILE) else pd.DataFrame(columns=['name', 'category', 'startup', 'roll_number'])

    if name in users_df['name'].values:
        st.error("User already registered.")
        return

    users_df.loc[len(users_df)] = [name, category, startup, roll_number]
    users_df.to_csv(USERS_FILE, index=False)
    save_user_image_streamlit(name)
    st.success(f"{name} registered successfully!")

# Mark attendance
def mark_attendance(purpose):
    if not purpose.strip():
        st.error("Purpose is required before scanning.")
        return

    if not os.listdir(FACE_DB_PATH):
        st.error("No registered users found.")
        return

    cap = cv2.VideoCapture(0)
    st.info("Press SPACE to scan face. Press Q to quit.")
    match_found = False

    while not match_found:
        ret, frame = cap.read()
        cv2.imshow("Scan Face - Press SPACE", frame)
        key = cv2.waitKey(1)

        if key == ord(' '):
            temp_path = "temp_scan.jpg"
            cv2.imwrite(temp_path, frame)

            try:
                result = DeepFace.find(img_path=temp_path, db_path=FACE_DB_PATH, enforce_detection=True,
                                       detector_backend='opencv', model_name='Facenet', silent=True)

                if len(result[0]) > 0:
                    file_path = result[0].iloc[0]['identity']
                    name = os.path.splitext(os.path.basename(file_path))[0]
                    users_df = pd.read_csv(USERS_FILE)
                    user_data = users_df[users_df['name'] == name].iloc[0]
                    category = user_data['category']
                    startup = user_data['startup']
                    roll_number = user_data['roll_number']

                    date_str = datetime.now().strftime('%Y-%m-%d')
                    time_str = datetime.now().strftime('%H:%M:%S')
                    att_path = os.path.join(ATTENDANCE_DIR, f'attendance_{date_str}.csv')

                    if os.path.exists(att_path):
                        df = pd.read_csv(att_path)
                    else:
                        df = pd.DataFrame(columns=['name', 'category', 'startup','roll_number', 'purpose', 'in_time', 'out_time'])

                    name_records = df[df['name'] == name]
                    if name_records.empty or not pd.isna(name_records.iloc[-1]['out_time']) and name_records.iloc[-1]['out_time'] != '':
                        df.loc[len(df)] = [name, category, startup, roll_number, purpose, time_str, '']
                        st.success(f"{name} Checked IN at {time_str}")
                    else:
                        last_index = name_records.index[-1]
                        df.at[last_index, 'out_time'] = time_str
                        st.success(f"{name} Checked OUT at {time_str}")

                    df.to_csv(att_path, index=False)
                    match_found = True
                else:
                    st.warning("Face not recognized.")

            except Exception as e:
                st.error(f"Face not detected or error occurred.\n{e}")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# View attendance for given date
def view_attendance(date_str):
    path = os.path.join(ATTENDANCE_DIR, f'attendance_{date_str}.csv')
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

# Export attendance to Excel
def export_to_excel(date_str):
    df = view_attendance(date_str)
    if df is not None:
        buffer = BytesIO()
        df.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)
        st.download_button(
            label=f"Download attendance_{date_str}.xlsx",
            data=buffer,
            file_name=f"attendance_{date_str}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("No data found for that date.")

# --- Streamlit UI ---

st.set_page_config(page_title="VentureNest Attendance", layout="centered")
st.title("VentureNest Attendance System")

tabs = st.tabs(["📝 Register", "📷 Mark Attendance", "🗂 Admin"])

# Register tab
with tabs[0]:
    st.subheader("Register New User")
    name = st.text_input("Name")
    category = st.selectbox("Category", ["ecell", "startup"])
    roll_number = st.text_input("Roll Number")
    startup = ""
    if category == "startup":
        startup = st.text_input("Startup Name")
    if st.button("Register"):
        register_face(name.strip(), category, startup.strip(), roll_number.strip())

# Mark Attendance tab
with tabs[1]:
    st.subheader("Scan Your Face")
    purpose = st.text_input("Enter Purpose")
    if st.button("Scan Face"):
        mark_attendance(purpose.strip())

# Admin tab
with tabs[2]:
    st.subheader("View / Export Attendance")
    date_input = st.date_input("Select Date")
    date_str = date_input.strftime('%Y-%m-%d')

    df = view_attendance(date_str)
    if df is not None:
        st.dataframe(df)
        export_to_excel(date_str)
    else:
        st.info("No attendance data found for this date.")
