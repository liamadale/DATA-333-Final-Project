import gradio as gr
from collections import defaultdict

# Define exercises
exercise_dict = {
    "Warm-Up": ["Arm Circles", "Hip Circles", "Leg Swings (Front-to-Back and Side-to-Side)", "March in Place", "Jog in Place", "Shoulder Rolls", "Bodyweight Squats", "RunnerΓÇÖs Lunge with Twist", "Squat to Reach", "Side Reaches", "Toe Touches", "Bird Dogs", "Glute Bridges", "Inchworms", "Carioca", "Squat Matrix"],
    "Yoga/Stretching": ["ChildΓÇÖs Pose", "Cat-Cow", "Thread the Needle", "Downward Facing Dog", "Cobra Pose", "Chair Pose", "Upward Facing Dog", "Low Lunge Twist", "Low Warrior with Hands Behind Back", "Half Split", "Seated Forward Fold", "Reclining Hand-to-Big-Toe Pose", "Toes Squat to Ankle Stretch", "Standing Forward Fold", "Triangle Pose", "Butterfly Stretch"],
    "Strength": ["Barbell Back Squat", "Dumbbell Chest Press", "Barbell Prone Row", "Kettlebell Romanian Deadlift", "Push-Up", "Pull-Up", "Dumbbell Row", "Single-Leg Deadlift", "Hip Lift", "Glute Bridge", "Bulgarian Split Squat", "Leg Press", "Leg Extension", "Wall Sit", "Deadlift", "Stiff-Legged Deadlift", "Leg Curl", "Standing Calf Raise", "Seated Calf Raise", "Bench Press", "Incline Bench Press", "Decline Bench Press", "Chest Fly", "Cable Crossover", "Dips", "Lat Pulldown", "Chin-Up", "Bent-Over Row", "Cable Row", "Upright Row", "Shoulder Press", "Military Press", "Arnold Press", "Lateral Raise", "Front Raise", "Triceps Pushdown", "Triceps Extension", "Preacher Curl", "Barbell Curl", "Hammer Curl", "Zottman Curl", "Crunch", "Reverse Crunch", "Russian Twist", "Leg Raise", "Plank", "Back Extension"],
    "Cardio": ["Jump Rope", "Dancing", "Power Walking", "Swimming", "Boxing", "Jogging in Place", "Air Jump Rope", "Jumping Jacks", "Squat to Front Kick", "Stair Climb", "Lateral Shuffles", "Mountain Climbers", "Burpees", "High Knees", "Sled Push", "Cycling Sprints", "Rowing Machine", "Explosive Circuits", "HIIT", "Step Mill"]
}

# Initialize the full workout plan
# This will hold the final published workout plan
full_plan = []

# Allow user to stage workouts before publishing
# This will hold the staged workout plan
staged_plan = []

# Function to get exercises based on category
def get_exercises(category):
    """
    Returns a list of exercises based on the selected category.
    """
    return gr.update(choices=exercise_dict[category], value=exercise_dict[category][0])

# Function to add a workout entry to the staged plan
def add_workout(section_label, category, exercise, sets, reps):
    """
    Adds a workout entry to the staged plan based on user input.
    """
    if sets == "None" or reps == "None":
        entry = f"{section_label} - {category}: {exercise} (timed/no reps)"
    else:
        entry = f"{section_label} - {category}: {exercise} {sets}x{reps}"
    staged_plan.append(entry)
    return format_staged_plan()

# Function to format the staged plan for display
def format_staged_plan():
    """
    Formats the staged plan for display in the output textbox.
    Returns a string representation of the staged plan.
    """
    return "\n".join([f"[{i}] {entry}" for i, entry in enumerate(staged_plan)])

# Function to delete an entry from the staged plan
def delete_entry(index):
    """
    Deletes an entry from the staged plan based on the provided index.
    """
    try:
        staged_plan.pop(int(index))
    except:
        pass
    return format_staged_plan()

# Function to clear the staged plan
def clear_plan():
    staged_plan.clear()
    return ""

# Function to publish the staged plan to the full plan
def publish_plan():
    full_plan.clear()
    full_plan.extend(staged_plan)
    return "\n".join(full_plan)

# Function to reset both staged and published plans
def reset_plan():
    """Clear both staged and final workout plans."""
    staged_plan.clear()
    full_plan.clear()
    return "", ""

# Function to reset the staged plan
with gr.Blocks() as demo:
    # Title and description
    gr.Markdown("# ≡ƒÅï∩╕Å RepShare - Workout Builder Demo")

    # Input fields for workout plan
    with gr.Row():
        section_label = gr.Dropdown(label="Section Label", choices=["Warmup", "Explosive Exercises", "Strength Set", "Cardio"], value="Warmup")
        category_dropdown = gr.Dropdown(label="Category", choices=list(exercise_dict.keys()), value="Warm-Up")
        exercise_dropdown = gr.Dropdown(label="Exercise", choices=exercise_dict["Warm-Up"])

    # Dropdowns for sets and reps
    with gr.Row():
        sets_dropdown = gr.Dropdown(label="Sets", choices=["None"] + [str(i) for i in range(1, 6)], value="None")
        reps_dropdown = gr.Dropdown(label="Reps", choices=["None"] + [str(i * 2) for i in range(1, 9)], value="None")

    # Buttons for adding, clearing, deleting, and publishing
    add_button = gr.Button("Γ₧ò Add to Staged Plan")
    clear_button = gr.Button("≡ƒ¬⌐ Clear Staged Plan")
    publish_button = gr.Button("Γ£à Publish Workout Plan")
    reset_button = gr.Button("🔄 Reset Plans")

    # Output areas for staged and published plans
    staged_output = gr.Textbox(label="Staged Workout Plan", lines=15)
    delete_index = gr.Textbox(label="Index to Delete", placeholder="Enter index number to delete")
    delete_button = gr.Button("≡ƒùæ∩╕Å Delete Entry")
    published_output = gr.Textbox(label="Final Published Plan", lines=10)

    # Set up event listeners for dropdowns and buttons
    category_dropdown.change(fn=get_exercises, inputs=category_dropdown, outputs=exercise_dropdown)
    add_button.click(fn=add_workout,
                     inputs=[section_label, category_dropdown, exercise_dropdown, sets_dropdown, reps_dropdown],
                     outputs=staged_output)
    delete_button.click(fn=delete_entry, inputs=delete_index, outputs=staged_output)
    clear_button.click(fn=clear_plan, outputs=staged_output)
    publish_button.click(fn=publish_plan, outputs=published_output)
    reset_button.click(fn=reset_plan, outputs=[staged_output, published_output])

demo.launch() 
