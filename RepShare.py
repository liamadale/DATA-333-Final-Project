import gradio as gr
from routines_tab import routine_builder

# Standalone demo that reuses the routine builder
with gr.Blocks() as demo:
    routine_builder()

demo.launch()
