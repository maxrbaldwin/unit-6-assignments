import gradio as gr

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

model = 'glm-5:cloud'
temperature = 0.9
client = ChatOllama(model=model, temperature=temperature)

history = []

def make_prompt(radioType, radioTireSize, radioColor, radioDiscount, radioMarketingThemes):
    prompt = f"""
        My company is called BikeEase and I would like to create a marketing campaign for a new bike model.
        Please come up with a catchy slogan, a name for the bike and a brief description of the features and benefits for the bike.
        Some information to include is that the bike is a {radioType} bike with {radioTireSize} tires, it comes in {radioColor} color and there is a discount of {radioDiscount}.
        The marketing theme should be {radioMarketingThemes}.
    """
    return prompt

def handle_initial_prompt(radioType, radioTireSize, radioColor, radioDiscount, radioMarketingThemes):
    prompt = make_prompt(radioType, radioTireSize, radioColor, radioDiscount, radioMarketingThemes)
    response = client.invoke(prompt)
    history.append(prompt)
    history.append(response)
    return response.content

with gr.Blocks() as capstone_gen_ai:
    gr.Markdown(f'# BikeEase Marketing Maestro - {model}')
    with gr.Row():
        with gr.Column():
            radioType = gr.Radio(['Mountain', 'Road', 'Hybrid'], label="What type of bike is it?")
            radioTireSize = gr.Radio(['26"', '27.5"', '29"'], label="What size tires does the bike have?")
            radioColor = gr.Radio(['Red', 'Blue', 'Green', 'Black'], label="What color is the bike?")
            radioDiscount = gr.Radio(['10%', '20%', '30%', '50%'], label="Is there a discount on the bike?")
            radioMarketingThemes = gr.Radio(['Adventure', 'Speed', 'Comfort', 'Style'], label="What marketing theme should be emphasized?")
            submit_button = gr.Button('Submit')
        with gr.Column():
            # output_text = gr.Textbox(label='Output', placeholder='Model response will appear here...', lines=10, interactive=True)
            output_md = gr.Markdown("Model response will appear here...")

    
    submit_button.click(fn=handle_initial_prompt, inputs=[radioType, radioTireSize, radioColor, radioDiscount, radioMarketingThemes], outputs=[output_md])
    
if __name__ == "__main__":
    capstone_gen_ai.launch()