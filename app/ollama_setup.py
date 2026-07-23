from ollama  import AsyncClient
from app.env import settings

async def ensure_models_exists():
    
    models_required = [
        settings.embedding_model,
        settings.llm_model
    ]

    client = AsyncClient(host = settings.ollama_url)
    
    response = await client.list()
    
    installed_models = [m.model for m in response.models] 

    for model in models_required:

        model_exists = any(installed.startswith(model) for installed in installed_models)
        
        if not model_exists:
            print(f"Model '{model}' not found. Downloading...")
            await client.pull(model = model)
        else:
            print(f"Model'{model}' already exists.")
    