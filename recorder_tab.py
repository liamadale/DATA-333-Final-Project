import gradio as gr
import pandas as pd
from datetime import datetime
import os

from utils.export import export_to_csv

folder_path = "logs"  # Relative folder path
os.makedirs(folder_path, exist_ok=True)  # Ensure folder exists

LOG_FILE = os.path.join(folder_path, "workout_log.csv")  # Relative file path

# ---------- Exercise Dictionary ----------

exercise_dict = {
    "Chest": [
        "Bench Press", "Incline Bench Press", "Dumbbell Press", "Incline Dumbbell Press", "Chest Fly",
        "Cable Crossover", "Push-Up", "Pec Deck", "Dips", "Decline Press"
    ],
    "Back": [
        "Deadlift", "Pull-Up", "Bent-Over Row", "Lat Pulldown", "Seated Row",
        "T-Bar Row", "Cable Row", "Chin-Up", "Straight-Arm Pulldown", "Face Pull"
    ],
    "Quads": ["Squat", "Leg Press", "Lunges", "Bulgarian Split Squat", "Front Squat"],
    "Hamstrings": ["Romanian Deadlift", "Leg Curl", "Good Morning", "Glute Bridge", "Kettlebell Swing"],
    "Shoulders": ["Overhead Press", "Lateral Raise", "Front Raise", "Arnold Press", "Reverse Pec Deck"],
    "Biceps": ["Barbell Curl", "Dumbbell Curl", "Preacher Curl", "Hammer Curl", "Cable Curl"],
    "Triceps": ["Tricep Pushdown", "Skull Crushers", "Overhead Extension", "Close-Grip Bench", "Dips"]
}

default_exercise_dict = {
    "Chest": "Bench Press",
    "Back": "Deadlift",
    "Quads": "Squat",
    "Hamstrings": "Romanian Deadlift",
    "Shoulders": "Overhead Press",
    "Biceps": "Barbell Curl",
    "Triceps": "Tricep Pushdown"
}

# ---------- Data Initialization ----------

# Load existing log if available
if os.path.exists(LOG_FILE):
    log = pd.read_csv(LOG_FILE).to_dict(orient="records")
else:
    log = []

# ---------- Functions ----------

def update_exercises(body_part):
    return gr.update(
        choices=exercise_dict.get(body_part, []),
        value=default_exercise_dict.get(body_part, None)
    )

def add_entry(date, body_part, exercise, sets, reps, weight):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return pd.DataFrame(log)

    entry = {
        "Date": date,
        "Body Part": body_part,
        "Exercise": exercise,
        "Sets": sets,
        "Reps": reps,
        "Weight": weight
    }
    log.append(entry)
    df = export_to_csv(log, LOG_FILE)
    return df

def download_log():
    if not log:
        return None
    export_to_csv(log, LOG_FILE)
    return LOG_FILE

def clear_log():
    global log
    log = []
    return pd.DataFrame()

def reset_log():
    global log
    log = []
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    return pd.DataFrame()

# ---------- Gradio UI ----------

default_body_part = "Chest"
today_str = datetime.today().strftime("%Y-%m-%d")

def recorder_app():
    gr.Markdown("## 🏋️ Workout Recorder")
    gr.Markdown("Log your workouts by body part, sets, reps, and weight.")

    date_input = gr.Textbox(label="Date (YYYY-MM-DD)", value=today_str)

    with gr.Row():
        body_part = gr.Dropdown(label="Body Part", choices=list(exercise_dict.keys()), value=default_body_part)
        exercise = gr.Dropdown(label="Exercise", choices=exercise_dict[default_body_part], value=default_exercise_dict[default_body_part])

    body_part.change(fn=update_exercises, inputs=body_part, outputs=exercise)

    with gr.Row():
        sets = gr.Dropdown(label="Sets", choices=list(range(1, 51)), value=3)
        reps = gr.Dropdown(label="Reps", choices=list(range(1, 101)), value=10)
        weight = gr.Dropdown(label="Weight (lbs)", choices=[round(x * 0.5, 1) for x in range(1, 2001)], value=100)

    submit_btn = gr.Button("Log Entry")
    output_table = gr.Dataframe(label="Workout Log")

    submit_btn.click(fn=add_entry, inputs=[date_input, body_part, exercise, sets, reps, weight], outputs=output_table)

    gr.Markdown("### 📁 Download or Manage Your Log")

    # Download section
    download_btn = gr.Button("Download Log as CSV")
    file_output = gr.File(label="Click to Download")

    download_btn.click(fn=download_log, outputs=file_output)

    # Clear and reset buttons
    clear_btn = gr.Button("Clear Log (Clears current entry. Does not affect file)")
    clear_btn.click(fn=clear_log, outputs=output_table)

    reset_btn = gr.Button("Reset Log (Clears current entry + deletes file)")
    reset_btn.click(fn=reset_log, outputs=output_table)

def recorder_tab():
    with gr.TabItem("📝 Recorder"):
        recorder_app()