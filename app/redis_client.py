import redis

from dotenv  import load_dotenv
from app.env import settings

load_dotenv()

redis_client = redis.Redis(
    host             = settings.redis_host,
    port             = settings.redis_port,
    password         = settings.redis_password,
    decode_responses = True 
)

# uv run python -m app.redis_client

if __name__ == "__main__":

    print("Trying connect to Redis...")

    try:

        if redis_client.ping():
            print("Successfully connected to Redis!")

    except redis.exceptions.AuthenticationError:
        print("Authentication Error: Check the password in your .env file.")

    except redis.exceptions.ConnectionError:
        print("Connection Error: Could not reach the Redis server.")

    except Exception as e:
        print(f"An unexpected error occurred.: {e}")
