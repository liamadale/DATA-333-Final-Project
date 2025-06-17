import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats


def track_exercise_weights(file_path, exercise_name):
    try:
        # Load the CSV file
        df = pd.read_csv(file_path.name)
        
        # Filter data for the specified exercise
        filtered_df = df[df['Exercise'] == exercise_name]
        
        if filtered_df.empty:
            return f"No data found for exercise: {exercise_name}"
        
        # Convert date strings to datetime objects
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
        
        # Sort by date
        filtered_df = filtered_df.sort_values('Date')
        
        # Extract data for plotting
        date = filtered_df['Date']
        pounds = filtered_df['Weight']
        
        # Convert dates to numeric values for regression
        date_nums = mdates.date2num(date)
        
        # Calculate linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(date_nums, pounds)
        
        # Create regression line
        regression_line = slope * date_nums + intercept
        
        # Create the plot
        plt.figure(figsize=(12, 6))
        plt.title(f'{exercise_name} Weight Progress')
        plt.xlabel('Date')
        plt.ylabel('Weight (lbs)')
        plt.grid(True)
        plt.xticks(rotation=45)
        
        # Plot scatter points only (no line connecting them)
        plt.scatter(date, pounds, color='blue', label='Data points')
        
        # Add regression line
        plt.plot(date, regression_line, color='red', label=f'Trend') 
        
        plt.legend()
        plt.tight_layout()
        
        # Calculate statistics
        stats_data = {
            "Current Weight": f"{filtered_df['Weight'].iloc[-1]} lbs",
            "Starting Weight": f"{filtered_df['Weight'].iloc[0]} lbs",
            "Progress": f"{filtered_df['Weight'].iloc[-1] - filtered_df['Weight'].iloc[0]} lbs",
            "Average Weight": f"{filtered_df['Weight'].mean():.2f} lbs",
            "Max Weight": f"{filtered_df['Weight'].max()} lbs"
        }
        
        stats_text = "\n".join([f"{k}: {v}" for k, v in stats_data.items()])
        
        return plt.gcf(), stats_text
    
    except Exception as e:
        return None, f"Error: {str(e)}"

def prediction_app():
    with gr.Row():
        with gr.Column():
            file_input = gr.File(label="Upload CSV File")
            exercise_input = gr.Textbox(label="Exercise Name")
            submit_btn = gr.Button("Track Progress")
        
        with gr.Column():
            stats_output = gr.Textbox(label="Statistics", lines=6)
            plot_output = gr.Plot(label="Progress Chart")
    
    submit_btn.click(
        fn=track_exercise_weights,
        inputs=[file_input, exercise_input],
        outputs=[plot_output, stats_output]
    )
    
    gr.Markdown("""
    ## CSV Format Requirements
    Your CSV file should have:
    - A 'Date' column in a format like 'YYYY-MM-DD'
    - An 'Exercise' column with the name of each exercise
    - A 'Weight' column with the weight values in lbs
    
    Example:
    """)

def prediction_tab():
    with gr.TabItem("🔮 Prediction"):
            gr.Markdown("# Exercise Weight Predictor")
            gr.Markdown("Upload a CSV file with exercise data and select an exercise to track progress and predict where you'll be.")
            prediction_app()
