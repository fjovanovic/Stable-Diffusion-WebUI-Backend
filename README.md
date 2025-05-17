# Stable Diffusion WebUI Backend
This project is a backend written using [FastAPI](https://fastapi.tiangolo.com/) specifically made for [AI Image Generator](https://github.com/fjovanovic/AI-Image-Generator-WebUI) 
project, web-based AI image generator powered by [Stable Diffusion](https://github.com/Stability-AI/stablediffusion) and [Gradio](https://www.gradio.app/). 

It provides an intuitive interface accessible through a web browser, allowing users to generate images using both text-to-image and image-to-image models. 
With its user-friendly design, the WebUI makes AI-powered image creation simple and efficient.  
Even if you don't have powerful hardware, you can run backend using Google Colab (check below)

## Prerequisites 
- ![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg) 
- `venv`
  
  > Before installing dependencies it is highly recommended to work in [virtual environment](https://docs.python.org/3/library/venv.html).
  > If you want to create virtual environment `.venv`, use following command:
  > ```bash
  >  python -m venv .venv
  >  ```
  > Make sure it is activated after installation

## Install dependencies 
To install pytorch use their [website](https://pytorch.org/get-started/locally/) and select required fields 
```bash
pip install -r requirements.txt
```

## Usage 
- To run the app use [uvicorn](https://www.uvicorn.org/) tool
  
  ```bash
  uvicorn main:app
  ```
- To check docs for the backend use following URL  
  `http://localhost:8000/docs` (if app is run on localhost and on port 8000)

## Problem with hardware 
If you don't have enough hardware capacity you can run it on Google Colab and use ngrok for tunneling to localhost (Colab)
- Install `pyngrok, nest_asyncio, uvicorn`
- Add `NGROK_TOKEN` to you secrets in Google Colab
  
  ```python
  from pyngrok import ngrok
  import uvicorn
  import nest_asyncio
  from google.colab import userdata

  NGROK_TOKEN = userdata.get('NGROK_TOKEN')
  ngrok.set_auth_token(NGROK_TOKEN)

  # Backend code ...
  
  nest_asyncio.apply()

  public_url = ngrok.connect(8000)
  print(f'Public URL: {public_url}')
  
  uvicorn.run(app, host='0.0.0.0', port=8000)
  ```
