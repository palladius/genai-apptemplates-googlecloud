import google.cloud.logging

import vertexai
from vertexai.language_models import TextGenerationModel

import gradio as gr

PROJECT_ID = "$PROJECT_ID" #Your Google Cloud Project ID
LOCATION_NAME="us-central1" #us-central1

client = google.cloud.logging.Client(project=PROJECT_ID)
client.setup_logging()

log_name = "genai-vertex-text-log"
logger = client.logger(log_name)

vertexai.init(project=PROJECT_ID, location=LOCATION_NAME)

model = TextGenerationModel.from_pretrained("text-bison@001")

def predict(prompt, max_output_tokens, temperature, top_p, top_k):
    logger.log_text(prompt)
    answer = model.predict(
        prompt,
        max_output_tokens=max_output_tokens, # default 128
        temperature=temperature, # default 0
        top_p=top_p, # default 1
        top_k=top_k) # default 40
    return answer

examples = [
    ["What are some generative AI services on Google Cloud in Public Preview?"],
    ["How many zipcodes are there in Mumbai"],
    ["What is the Zipcode for Kandivali East in Mumbai"],
]

demo = gr.Interface(
    predict,
    [ gr.Textbox(label="Enter prompt:", value="What are some generative AI services on Google Cloud in Public Preview?"),
      gr.Slider(32, 1024, value=512, step = 32, label = "max_output_tokens"),
      gr.Slider(0, 1, value=0.2, step = 0.1, label = "temperature"),
      gr.Slider(0, 1, value=0.8, step = 0.1, label = "top_p"),
      gr.Slider(1, 40, value=38, step = 1, label = "top_k"),
    ],
    "text",
    examples=examples
    )

demo.launch(server_name="0.0.0.0", server_port=8080)
