# Capstone Generative AI

## Introduction
Overall this was fun. While I enjoy deeplearning a lot more I can see how using LLMs like this can add complementary features. Although this time I didn't see any reason to use `@tool`, I can see the value in providing the addition context to an LLM. Especially something like the result of a model prediction. Many options. Lots of potential.

## How to run this
To run this you are going to need to run `Ollama` locally. I am going to assume that you already have it install. While I used this forked project, I didn't run Ollama in the dev container. I just ran it locally on my machine because I wanted my machine to have Ollama locally. As long as Ollama is running locally or in the container, the instructions should still be fine

### Make sure Ollama is running locally
```bash
ollama serve
```

### Pull the model in the project - glm-5:cloud
```bash
ollama pull glm-5:cloud
```

### Run the app
```
python capstone_gen_ai/main.py
```

### Go to localhost
```
http://127.0.0.1:7860
```

## Model Choice
I chose to use `glm-5:cloud` based on the [LLM Arena Leaderboard](https://arena.ai/leaderboard/text?license=open-source). In the test arena, I shorted by open source and that was the top open source option for text.