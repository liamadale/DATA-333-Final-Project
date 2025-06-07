import gradio as gr
from recorder_tab import recorder_tab
from routines_tab import routines_tab
from regression_tab import regression_tab

with gr.Blocks() as demo:
    with gr.Tabs():
        recorder_tab()
        routines_tab()
        regression_tab()

demo.launch()

