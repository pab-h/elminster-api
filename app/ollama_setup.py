from ollama  import Client
from app.env import settings

def ensure_models_exists():
    
    models_required = [
        settings.embedding_model,
        settings.llm_model
    ]

    client = Client(host = settings.ollama_url)
    
    response = client.list()
    
    installed_models = [m.model for m in response.models] 

    for model in models_required:

        model_exists = any(installed.startswith(model) for installed in installed_models)
        
        if not model_exists:
            print(f"Model '{model}' not found. Downloading...")
            client.pull(model = model)
        else:
            print(f"Model'{model}' already exists.")
    