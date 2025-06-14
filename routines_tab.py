import gradio as gr
import pandas as pd
import os

from utils.export import export_to_csv

# Define exercises for the workout routine builder
exercise_dict = {
    "Warm-Up": [
        "Arm Circles",
        "Hip Circles",
        "Leg Swings (Front-to-Back and Side-to-Side)",
        "March in Place",
        "Jog in Place",
        "Shoulder Rolls",
        "Bodyweight Squats",
        "Runner’s Lunge with Twist",
        "Squat to Reach",
        "Side Reaches",
        "Toe Touches",
        "Bird Dogs",
        "Glute Bridges",
        "Inchworms",
        "Carioca",
        "Squat Matrix",
    ],
    "Yoga/Stretching": [
        "Child’s Pose",
        "Cat-Cow",
        "Thread the Needle",
        "Downward Facing Dog",
        "Cobra Pose",
        "Chair Pose",
        "Upward Facing Dog",
        "Low Lunge Twist",
        "Low Warrior with Hands Behind Back",
        "Half Split",
        "Seated Forward Fold",
        "Reclining Hand-to-Big-Toe Pose",
        "Toes Squat to Ankle Stretch",
        "Standing Forward Fold",
        "Triangle Pose",
        "Butterfly Stretch",
    ],
    "Strength": [
        "Barbell Back Squat",
        "Dumbbell Chest Press",
        "Barbell Prone Row",
        "Kettlebell Romanian Deadlift",
        "Push-Up",
        "Pull-Up",
        "Dumbbell Row",
        "Single-Leg Deadlift",
        "Hip Lift",
        "Glute Bridge",
        "Bulgarian Split Squat",
        "Leg Press",
        "Leg Extension",
        "Wall Sit",
        "Deadlift",
        "Stiff-Legged Deadlift",
        "Leg Curl",
        "Standing Calf Raise",
        "Seated Calf Raise",
        "Bench Press",
        "Incline Bench Press",
        "Decline Bench Press",
        "Chest Fly",
        "Cable Crossover",
        "Dips",
        "Lat Pulldown",
        "Chin-Up",
        "Bent-Over Row",
        "Cable Row",
        "Upright Row",
        "Shoulder Press",
        "Military Press",
        "Arnold Press",
        "Lateral Raise",
        "Front Raise",
        "Triceps Pushdown",
        "Triceps Extension",
        "Preacher Curl",
        "Barbell Curl",
        "Hammer Curl",
        "Zottman Curl",
        "Crunch",
        "Reverse Crunch",
        "Russian Twist",
        "Leg Raise",
        "Plank",
        "Back Extension",
    ],
    "Cardio": [
        "Jump Rope",
        "Dancing",
        "Power Walking",
        "Swimming",
        "Boxing",
        "Jogging in Place",
        "Air Jump Rope",
        "Jumping Jacks",
        "Squat to Front Kick",
        "Stair Climb",
        "Lateral Shuffles",
        "Mountain Climbers",
        "Burpees",
        "High Knees",
        "Sled Push",
        "Cycling Sprints",
        "Rowing Machine",
        "Explosive Circuits",
        "HIIT",
        "Step Mill",
    ],
}

# Lists to hold staged and published workout routines
full_plan = pd.DataFrame(columns=["Section", "Category", "Exercise", "Sets", "Reps"])
staged_plan = pd.DataFrame(columns=["Section", "Category", "Exercise", "Sets", "Reps"])

# File path for exporting published routines
folder_path = "logs"
os.makedirs(folder_path, exist_ok=True)
ROUTINE_FILE = os.path.join(folder_path, "workout_routines.csv")

def get_exercises(category: str):
    """Return available exercises for the selected category."""
    return gr.update(choices=exercise_dict[category], value=exercise_dict[category][0])

def add_workout(section_label: str, category: str, exercise: str, sets: str, reps: str):
    """Add a workout entry to the staged plan."""
    global staged_plan
    row = {
        "Section": section_label,
        "Category": category,
        "Exercise": exercise,
        "Sets": sets,
        "Reps": reps,
    }
    staged_plan.loc[len(staged_plan)] = row
    return format_staged_plan()

def format_staged_plan():
    """Return the staged plan DataFrame with an index column for easy deletion."""
    return staged_plan.reset_index().rename(columns={"index": "Index"})

def delete_entry(index: str):
    """Delete an entry from the staged plan by index."""
    global staged_plan
    try:
        staged_plan.drop(index=int(index), inplace=True)
        staged_plan.reset_index(drop=True, inplace=True)
    except Exception:
        pass
    return format_staged_plan()

def clear_plan():
    """Clear the staged plan."""
    global staged_plan
    staged_plan = staged_plan.iloc[0:0].copy()
    return format_staged_plan()

def publish_plan():
    """Publish the staged plan to the final plan and save to CSV."""
    global full_plan
    full_plan = staged_plan.copy()
    export_to_csv(full_plan, ROUTINE_FILE)
    return full_plan


def download_plan():
    """Return the CSV file containing the published plan for download."""
    if full_plan.empty:
        return None
    export_to_csv(full_plan, ROUTINE_FILE)
    return ROUTINE_FILE

def reset_plan():
    """Reset both staged and published plans."""
    global staged_plan, full_plan
    staged_plan = staged_plan.iloc[0:0].copy()
    full_plan = full_plan.iloc[0:0].copy()
    if os.path.exists(ROUTINE_FILE):
        os.remove(ROUTINE_FILE)
    return format_staged_plan(), full_plan

def routine_builder():
    """Create the workout routine builder interface."""

    gr.Markdown("## ⌛ Workout Routine Builder")
    gr.Markdown("### Create your custom workout routine by adding exercises to the staged plan. You can then publish it to finalize your workout plan.")

    with gr.Row():
        section_label = gr.Dropdown(
            label="Section Label",
            choices=["Warmup", "Explosive Exercises", "Strength Set", "Cardio"],
            value="Warmup",
        )
        category_dropdown = gr.Dropdown(
            label="Category", choices=list(exercise_dict.keys()), value="Warm-Up"
        )
        exercise_dropdown = gr.Dropdown(
            label="Exercise", choices=exercise_dict["Warm-Up"]
        )

    with gr.Row():
        sets_dropdown = gr.Dropdown(
            label="Sets", choices=["None"] + [str(i) for i in range(1, 6)], value="None"
        )
        reps_dropdown = gr.Dropdown(
            label="Reps",
            choices=["None"] + [str(i * 2) for i in range(1, 9)],
            value="None",
        )

    add_button = gr.Button("➕ Add to Staged Plan")
    clear_button = gr.Button("🗑️ Clear Staged Plan")
    publish_button = gr.Button("📣 Publish Workout Plan")
    reset_button = gr.Button("🔄 Reset Plans")

    staged_output = gr.DataFrame(
        headers=["Index", "Section", "Category", "Exercise", "Sets", "Reps"],
        label="Staged Workout Plan",
        interactive=True,
    )
    delete_index = gr.Textbox(
        label="Index to Delete", placeholder="Enter index number to delete"
    )
    delete_button = gr.Button("❌ Delete Entry")
    published_output = gr.DataFrame(
        headers=["Section", "Category", "Exercise", "Sets", "Reps"],
        label="Final Published Plan",
        interactive=False,
    )

    gr.Markdown("### 📁 Download or Manage Your Plan")
    download_button = gr.Button("Download Plan as CSV")
    file_output = gr.File(label="Click to Download")

    category_dropdown.change(
        fn=get_exercises, inputs=category_dropdown, outputs=exercise_dropdown
    )
    add_button.click(
        fn=add_workout,
        inputs=[section_label, category_dropdown, exercise_dropdown, sets_dropdown, reps_dropdown],
        outputs=staged_output,
    )
    delete_button.click(fn=delete_entry, inputs=delete_index, outputs=staged_output)
    clear_button.click(fn=clear_plan, outputs=staged_output)
    publish_button.click(fn=publish_plan, outputs=published_output)
    download_button.click(fn=download_plan, outputs=file_output)
    reset_button.click(fn=reset_plan, outputs=[staged_output, published_output])

def routines_tab():
    """Tab wrapper used in the main application."""
    with gr.TabItem("⌛ Routines"):
        routine_builder()
