import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=int(PORT), reload=True)