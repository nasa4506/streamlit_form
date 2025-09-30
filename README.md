📊 Persistent Social Media & Self-Esteem Study

This project is an interactive Streamlit web app designed to collect and analyze questionnaire responses about social media engagement and self-esteem.

The app supports persistent storage using browser LocalStorage, so responses remain saved across sessions without requiring a backend database.

🚀 Features

📋 Questionnaire Form

Collects demographic info (gender).

Measures Social Media Engagement Questionnaire (SMEQ) scores.

Measures Self-Esteem Scale (Rosenberg-based) with reverse-scored items.

💾 Persistent Data Storage

Responses are stored in the browser’s LocalStorage.

Entries are preserved even after page reloads or browser restarts.

📈 Live Results Dashboard

Displays real-time metrics:

Total responses collected

Average SMEQ score

Average Self-Esteem score

Interactive data table with row deletion support.

📥 Data Export

Download all responses as a CSV file.

🛠️ Tech Stack

Streamlit
 – Web framework

Pandas
 – Data handling

Altair
 – Visualization

streamlit-local-storage
 – Browser persistence

📂 Project Structure
.
├── app.py         # Main Streamlit application
├── README.md      # Project documentation

⚡ Installation & Setup

Clone this repo

git clone https://github.com/yourusername/social-media-selfesteem-study.git
cd social-media-selfesteem-study


Create virtual environment (recommended)

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


Install dependencies

pip install -r requirements.txt


Example requirements.txt:

streamlit
pandas
altair
streamlit-local-storage


Run the app

streamlit run app.py

📊 Questionnaire Details

Social Media Engagement Questionnaire (SMEQ)

Measures usage frequency at specific times (before sleep, after waking, meals, etc.).

Responses range from 0–7 scale.

Self-Esteem Scale

Based on Rosenberg Self-Esteem Scale (10 items).

Uses reverse scoring for negatively worded items (Q2, Q5, Q6, Q8, Q9).

Final score range: 10–40 (higher = higher self-esteem).

🧹 Data Management

Delete Entries: Use the checkbox in the table to remove specific responses.

Download Data: Export all collected responses as a CSV.

📌 Notes

This is a client-side only app — all data is stored in the participant’s browser.

For multi-user or production scenarios, you should replace LocalStorage with a proper database backend (e.g., SQLite, PostgreSQL, Firebase).

📜 License

This project is open-source under the MIT License.
