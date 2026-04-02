import os
import torch
import gradio as gr
from diffusers import StableDiffusionPipeline
from huggingface_hub import InferenceClient
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

model_map = {
    'stabilityai/stable-diffusion-xl-base-1.0': {
        'model': 'stabilityai/stable-diffusion-xl-base-1.0',
        'use_remote': True,
        'quality': 'high',
        'tokens_maximum': 'high',
    },
    'sd-legacy/stable-diffusion-v1-5': {
        'model': 'sd-legacy/stable-diffusion-v1-5',
        'quality': 'low',
        'tokens_maximum': 'low',
    },
    'ByteDance/sd2.1-base-zsnr-laionaes6': {
        'model': 'ByteDance/sd2.1-base-zsnr-laionaes6',
        'quality': 'low',
        'tokens_maximum': 'medium',
    }
}

model = list(model_map.values())[0]['model']

def get_pipe():
    torch.cuda.empty_cache()
    pipe = StableDiffusionPipeline.from_pretrained(model_map[model]['model']).to("cuda")
    return pipe

def make_movie_poster_prompt(title_input, genre_input, quality_input, art_style_input, release_date_input):
    return f"""
    Create a movie poster for a {genre_input} movie titled "{title_input}". The movie title should be included in the poster design. The poster should visually represent the genre of the movie and be eye-catching to potential viewers.
    The poster should be in {quality_input} quality and have an art style that is {art_style_input}.
    The movie is set to be released on {release_date_input} and this release date should be included in the image.
    """

def generate_movie_poster(title_input, genre_input, quality_input, art_style_input, release_date_input):
    prompt = make_movie_poster_prompt(title_input, genre_input, quality_input, art_style_input, release_date_input)
    movie_poster = generate_poster(prompt)
    return movie_poster

def generate_poster(prompt):
    selected_model = model_map[model]
    
    if selected_model.get('use_remote'):
        print('**** Using remote inference for model:', selected_model['model'], os.getenv("HUGGING_FACE_TOKEN"))
        client = InferenceClient(
            model=selected_model['model'],
            api_key=HUGGING_FACE_TOKEN
        )
        response = client.text_to_image(prompt, num_inference_steps=40, guidance_scale=8.0)
        image = response
        return image
    else:
        print('**** Using local inference for model:', selected_model['model'])
        image = get_pipe()(prompt, num_inference_steps=50).images[0]
        return image

def make_netflix_prompt(movie_name):
    return f"""
    Please describe the plot, genre, main characters, and visual style
    of the Netflix movie "{movie_name}".
    """

def make_neflix_poster_prompt(movie_description):
    return f"""
    Create a movie poster based on the following description of a Netflix movie:
    {movie_description}
    The poster should visually represent the plot, genre, main characters, and visual style of the movie. The poster should be eye-catching and appealing to potential viewers.
    The poster must include the title of the movie.
    The post must include the Netflix logo to indicate that it is a Netflix movie.
    """

def generate_netflix_poster(movie_name):
    model = 'glm-5:cloud'
    temperature = 0.9
    client = ChatOllama(model=model, temperature=temperature)
    netflix_prompt = make_netflix_prompt(movie_name)
    response = client.invoke(netflix_prompt)
    poster_prompt = make_neflix_poster_prompt(response)
    netflix_poster = generate_poster(poster_prompt)
    return netflix_poster

def handle_model_selection(model_label):
    global model
    
    for value in model_map.values():
        label = make_label(value['model'], value['quality'], value['tokens_maximum'])
        if label == model_label:
             model = value['model']
             break
    
    model_name = model_map[model]['model']
    
    return f"### Model - {model_name}"

def make_label(model_name, quality, tokens_maximum):
    return f"{model_name} - Quality: {quality}, Tokens: {tokens_maximum}"

def get_model_selection_dropdown():
    labels = []
    
    for key in model_map.values():
        label = make_label(key['model'], key['quality'], key['tokens_maximum'])
        labels.append(label)
    return labels

with gr.Blocks() as studio:
    gr.Markdown(f'# Movie Poster Generator')
    model_output = gr.Markdown(f'### Model - {model}')
    
    with gr.Tabs() as tabs:
        with gr.Tab("Movie Poster Generator", id="movie_poster_generator"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("This tab will be for generating movie posters based the selections you make below")
                    title_input = gr.Textbox(label='Movie Title', placeholder='Enter the title of the movie here...', lines=1)
                    genre_input = gr.Radio(['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi'], label="Select the genre of the movie")
                    quality_input = gr.Radio(['720p', '1080p', '4K'], label="Select the quality of the movie poster")
                    art_style_input = gr.Radio(['Realistic', 'Cartoon', 'Abstract'], label="Select the art style of the movie poster")
                    release_date_input = gr.Textbox(label='Release Date', placeholder='Enter the release date of the movie here...', lines=1)
                    submit_button = gr.Button('Generate Poster')
                with gr.Column():
                    gr.Markdown("The generated movie poster will appear here after you click the 'Generate Poster' button.")
                    output_image = gr.Image(label='Generated Movie Poster')

        with gr.Tab("Netflix Movie Generator", id="netflix_movie_generator"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("This tab will be for generating movie posters based on Netflix movies. You can enter the name of a Netflix movie and the model will generate a poster for it.")
                    netflix_movie_input = gr.Textbox(label='Netflix Movie Name', placeholder='Enter the name of a Netflix movie here...', lines=1)
                    netflix_submit_button = gr.Button('Generate Poster')
                with gr.Column():
                    gr.Markdown("The generated Netflix movie poster will appear here after you click the 'Generate Poster' button.")
                    netflix_output_image = gr.Image(label='Generated Netflix Movie Poster')

            netflix_submit_button.click(fn=generate_netflix_poster, inputs=[netflix_movie_input], outputs=[netflix_output_image])

        with gr.Tab("Free Style", id="free_style"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("This tab is for generating movie posters based on a free form text prompt. You can enter any description of a movie and the model will generate a poster for it.")
                    free_style_input = gr.Textbox(label='Free Style Movie Description', placeholder='Enter a description of a movie here...', lines=5)
                    free_style_submit_button = gr.Button('Generate Poster')
                with gr.Column():
                    gr.Markdown("The generated movie poster will appear here after you click the 'Generate Poster' button.")
                    free_style_output_image = gr.Image(label='Generated Free Style Movie Poster')
            
        
        with gr.Tab("Model Select", id="model_select"):
            gr.Markdown("This tab will be for selecting different models to use for generating movie posters. You can select from a list of available models and the model you select will be used for generating movie posters in the other tabs.")
            model_selection = gr.Dropdown(get_model_selection_dropdown(), label="Select a model to use for generating movie posters")
        
    submit_button.click(fn=generate_movie_poster, inputs=[title_input, genre_input, quality_input, art_style_input, release_date_input], outputs=[output_image])
    model_selection.change(fn=handle_model_selection, inputs=[model_selection], outputs=[model_output])
    free_style_submit_button.click(fn=generate_poster, inputs=[free_style_input], outputs=[free_style_output_image])

if __name__ == "__main__":
    studio.launch()