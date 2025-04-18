# 💼 NestScan | AI Check-in for Startups & Ecosystems

An AI-powered facial recognition system for seamless check-ins and attendance tracking. **NestScan** is tailored for **startup incubators, co-working spaces, events, and educational environments**, enabling effortless and secure entry using just your face.

---

## 🚀 Features

- 👤 **User Registration** with name, category (`ecell` / `startup`), roll number, and startup (if applicable)
- 🤫 **Webcam Face Capture** for user registration and verification
- 🧠 **AI Facial Recognition** using DeepFace with Facenet model
- 🔄 **Smart Check-In & Check-Out** with automatic time-stamping
- 🗕️ **Date-wise Logs** for attendance tracking
- 📄 **Excel Export** for admin or organizational reporting

---

## 🧰 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Face Recognition**: [DeepFace](https://github.com/serengil/deepface)
- **Computer Vision**: [OpenCV](https://opencv.org/)
- **Data Handling**: [Pandas](https://pandas.pydata.org/), CSV, Excel (via `openpyxl`)

---

## 🛠 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/PULKESH01/your-repository-name.git
cd your-repository-name
```

### 2. (Optional but Recommended) Create a Virtual Environment
```bash
python -m venv venv
# Activate:
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install Required Libraries
```bash
pip install -r requirements.txt
```

> Example `requirements.txt`:
```txt
streamlit
opencv-python
deepface
pandas
openpyxl
```

---

## ▶️ How to Run

```bash
streamlit run attsys.py
```

---

## 🧪 How It Works

### 📝 Register Tab
- Enter your details (name, roll number, etc.)
- Capture your face via webcam
- Image saved locally for future recognition

### 📷 Mark Attendance Tab
- Enter your visit purpose
- Scan your face
- The system checks whether you're checking in or out

### 📂 Admin Tab
- Select a date to view attendance
- Option to download the sheet as an Excel file

---

## 📁 Project Structure

```
NestScan/
├── attsys.py               # Main Streamlit application
├── users.csv               # Stores registered user details
├── attendance/             # Daily logs (auto-created)
└── face_db/                # Stores face images of registered users
```

---

## 📸 Demo

![Screenshot 2025-04-18 124621](https://github.com/user-attachments/assets/f4672521-356c-4a41-8f95-456ca73e0df7)
![Screenshot 2025-04-18 124642](https://github.com/user-attachments/assets/84110d19-6491-4cb3-abe0-6e10b8f3c3b8)
![Screenshot 2025-04-18 124700](https://github.com/user-attachments/assets/579527af-887c-4f8f-83f8-3904e8eaeebd)




---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](https://github.com/PULKESH01/your-repository-name/blob/main/LICENSE) file for more details.

