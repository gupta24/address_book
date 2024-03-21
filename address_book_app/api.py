from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from address_book_app.core.sqlite_db_connection import engine
from address_book_app.db_models import models
from address_book_app.endpoints_v1.address_apis import routes as address_book_route


models.Base.metadata.create_all(bind=engine)

# intialized the fastapi app
app = FastAPI(
    title="AddressBookApp",
    description="Get latitude and longitute co-ordinates of given address",
    version="0.0.1"
)

# add the middleware for handle api request from all clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# add app api routes
app.include_router(address_book_route)
