import os
from dotenv import load_dotenv

_ = load_dotenv()

api_token = os.getenv("EXAMPLE_KEY")

if __name__ == "__main__":
    print("Hello World!")