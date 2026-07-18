import os
import redis
from dotenv import load_dotenv

load_dotenv()

redis_poll = redis.Redis(
    host             = os.getenv("REDIS_HOST"),
    port             = os.getenv("REDIS_PORT"),
    password         = os.getenv("REDIS_PASSWORD"),
    decode_responses = True 
)

if __name__ == "__main__":

    print("Trying connect to Redis...")

    try:

        if redis_poll.ping():
            print("Successfully connected to Redis!")

    except redis.exceptions.AuthenticationError:
        print("Authentication Error: Check the password in your .env file.")

    except redis.exceptions.ConnectionError:
        print("Connection Error: Could not reach the Redis server.")

    except Exception as e:
        print(f"An unexpected error occurred.: {e}")
