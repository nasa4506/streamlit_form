import streamlit as st
import pandas as pd
import altair as alt
from streamlit_local_storage import LocalStorage # Import the component

# --- PAGE CONFIGURATION AND INITIALIZATION ---
st.set_page_config(layout="wide")
localS = LocalStorage() # Create a LocalStorage instance

# --- INITIALIZE SESSION STATE FROM LOCAL STORAGE ---
if 'responses' not in st.session_state:
    # Try to get data from local storage
    data_from_storage = localS.getItem('responses')
    if data_from_storage is not None:
        # If data exists, load it from JSON into a DataFrame
        st.session_state.responses = pd.read_json(data_from_storage)
    else:
        # If no data exists, initialize an empty DataFrame
        st.session_state.responses = pd.DataFrame()

# --- SCORING CONSTANTS ---
se_score_map = {"Strongly Agree": 4, "Agree": 3, "Disagree": 2, "Strongly Disagree": 1}
se_reverse_score_map = {"Strongly Agree": 1, "Agree": 2, "Disagree": 3, "Strongly Disagree": 4}
reverse_scored_items = [2, 5, 6, 8, 9]

# --- HELPER FUNCTIONS ---
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def delete_entry(index):
    """Deletes a row and saves the updated state to local storage."""
    st.session_state.responses = st.session_state.responses.drop(index).reset_index(drop=True)
    # Save updated data back to local storage
    localS.setItem('responses', st.session_state.responses.to_json())

# --- QUESTIONNAIRE UI ---
st.title("📊 Persistent Social Media & Self-Esteem Study")
st.markdown("---")
st.header("✍️ Participant Questionnaire")

with st.form(key='survey_form', clear_on_submit=True):
    # (The form code is identical to the previous version, so it's kept brief here)
    gender = st.radio("**What is your gender?**", ("Male", "Female", "Other"), horizontal=True)
    st.markdown("---")
    st.subheader("Part 1: Social Media Engagement Questionnaire (SMEQ)")
    smeq_questions = {1: "Before sleep", 2: "After waking up", 3: "During breakfast", 4: "During lunch", 5: "During supper"}
    smeq_cols = st.columns(len(smeq_questions))
    smeq_responses = {i + 1: col.number_input(f"{i+1}. {q}", 0, 7, 1, key=f"smeq_{i+1}") for i, (col, q) in enumerate(zip(smeq_cols, smeq_questions.values()))}
    st.markdown("---")
    st.subheader("Part 2: Self-Esteem Scale")
    se_questions = {1: "Satisfied w/ myself", 2: "No good at all", 3: "Have good qualities", 4: "Can do things well", 5: "Not proud", 6: "Feel useless", 7: "Am a person of worth", 8: "Want more self-respect", 9: "Am a failure", 10: "Positive attitude"}
    options = ["Strongly Disagree", "Disagree", "Agree", "Strongly Agree"]
    se_responses = {i: st.radio(q, options, horizontal=True, key=f"se_{i}") for i, q in se_questions.items()}
    submitted = st.form_submit_button("Submit My Responses")

# --- FORM PROCESSING LOGIC ---
if submitted:
    smeq_score = sum(smeq_responses.values())
    self_esteem_score = sum(se_reverse_score_map[r] if i in reverse_scored_items else se_score_map[r] for i, r in se_responses.items())
    columns = ['gender'] + [f'smeq_{i}' for i in range(1, 6)] + [f'se_{i}' for i in range(1, 11)] + ['SMEQ_Score', 'Self_Esteem_Score']
    new_data_dict = {'gender': gender, **{f'smeq_{k}': v for k, v in smeq_responses.items()}, **{f'se_{k}': v for k, v in se_responses.items()}, 'SMEQ_Score': smeq_score, 'Self_Esteem_Score': self_esteem_score}
    
    if st.session_state.responses.empty:
        st.session_state.responses = pd.DataFrame(columns=columns)
    
    st.session_state.responses = pd.concat([st.session_state.responses, pd.DataFrame([new_data_dict])], ignore_index=True)
    
    # **SAVE TO LOCAL STORAGE AFTER SUBMISSION**
    localS.setItem('responses', st.session_state.responses.to_json())
    st.success("Response recorded and saved to your browser!")

# --- LIVE RESULTS DISPLAY ---
# (This section is mostly unchanged, but now reflects the persistent data)
st.markdown("---")
st.header("📈 Live Study Results")
if st.session_state.responses.empty:
    st.info("No data submitted yet. Your first entry will be saved in your browser.")
else:
    # Dashboard, Visuals, and Data Table are the same as before...
    st.subheader("Dashboard Cards")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Entries Submitted", len(st.session_state.responses))
    col2.metric("Average Social Media Score", f"{st.session_state.responses['SMEQ_Score'].mean():.2f} / 35")
    col3.metric("Average Self-Esteem Score", f"{st.session_state.responses['Self_Esteem_Score'].mean():.2f} / 40")
    st.markdown("---")

    st.subheader("Data Table with Deletion")
    display_df = st.session_state.responses.copy()
    display_df['Delete'] = [False] * len(display_df)
    edited_df = st.data_editor(display_df, column_config={"Delete": st.column_config.CheckboxColumn(required=True)}, disabled=st.session_state.responses.columns, hide_index=True)
    
    delete_indices = edited_df[edited_df['Delete']].index
    if not delete_indices.empty:
        delete_entry(delete_indices[0])
        st.rerun()

    # CSV Download Button
    csv_data = convert_df_to_csv(st.session_state.responses)
    st.download_button(label="📥 Download all data as CSV", data=csv_data, file_name='persistent_study_responses.csv', mime='text/csv')