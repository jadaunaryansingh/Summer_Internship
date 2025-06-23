import gradio as gr
import google.generativeai as genai
genai.configure(api_key="AIzaSyCbo3EaicL9Un8WJV3y_R5fMA1DdteWtFs")
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def recommend_clothes(body_shape, height, gender, size):
    prompt = (
        f"I am a {gender} with a body shape of {body_shape}, height {height}, "
        f"and clothing size {size}. Suggest outfit recommendations that suit me. "
        f"Include clothing types, ideal fits, and color/style tips."
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

with gr.Blocks() as demo:
    gr.Markdown("# 👗 StyleMe AI – Clothing Recommendation App")
    with gr.Row():
        gender = gr.Dropdown(["Male", "Female", "Non-binary"], label="Gender")
        body_shape = gr.Dropdown(
            ["Hourglass", "Pear", "Rectangle", "Apple", "Inverted Triangle", "Athletic", "Round"],
            label="Body Shape"
        )
    with gr.Row():
        height = gr.Textbox(label="Height (in cm or feet)")
        size = gr.Dropdown(["XS", "S", "M", "L", "XL", "XXL"], label="Clothing Size")
    submit_btn = gr.Button("Recommend Clothes")
    output = gr.Textbox(label="Recommendations", lines=10)
    submit_btn.click(recommend_clothes, inputs=[body_shape, height, gender, size], outputs=output)
demo.launch()