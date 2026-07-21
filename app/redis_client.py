import redis

from app.env import settings

redis_client = redis.Redis(
    host             = settings.redis_host,
    port             = settings.redis_port,
    decode_responses = True 
)

# uv run python -m app.redis_client

if __name__ == "__main__":

    print("Trying connect to Redis...")

    try:

        if redis_client.ping():
            print("Successfully connected to Redis!")

    except redis.exceptions.ConnectionError:
        print("Connection Error: Could not reach the Redis server.")

    except Exception as e:
        print(f"An unexpected error occurred.: {e}")
