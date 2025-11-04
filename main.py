from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def main():
    print("Hello from langchain-course!")
    print("OpenAI API Key:", os.getenv("OPENAI_API_KEY"))
    print("Google API Key:", os.getenv("GOOGLE_API_KEY"))


if __name__ == "__main__":
    main()
