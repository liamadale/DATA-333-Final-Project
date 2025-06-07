import gradio as gr
from recorder_tab import recorder_tab
from routines_tab import routines_tab
from prediction_tab import prediction_tab
from saved_search_tab import search_tab

with gr.Blocks() as demo:
    gr.Markdown("# 🏋️‍♂️ RepShare - Workout Toolkit")
    with gr.Tabs():
        recorder_tab()
        routines_tab()
        prediction_tab()
        search_tab()


demo.launch()

