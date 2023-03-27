import uvicorn
from configuration import API_HOST, API_PORT


if __name__ == "__main__":
    uvicorn.run("address_book_app.api:app", host=API_HOST, port=API_PORT, reload=True)
