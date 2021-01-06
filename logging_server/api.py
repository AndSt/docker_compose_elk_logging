import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.origins import get_allowed_origins
from src.logging import setup_basic_logging


from pydantic.main import BaseModel


class LoggingRequest(BaseModel):
    level: str
    context: str


setup_basic_logging()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.put('/log')
def log(req: LoggingRequest):
    if req.level == "error":
        logging.error(req.context)
    elif req.level == "info":
        logging.info(req.context)
    elif req.level == "debug":
        logging.debug(req.context)
    else:
        logging.debug(req.context)


if __name__ == "__main__":
    logging.info('Start App.')
    uvicorn.run("api:app", host="0.0.0.0", port=54300, log_level="debug", reload=True)
