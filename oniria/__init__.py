import os
from dotenv import load_dotenv, dotenv_values

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(os.path.abspath(dotenv_path))
