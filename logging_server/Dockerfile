FROM tiangolo/uvicorn-gunicorn:python3.8-slim
LABEL maintainer='Andreas Stephan'

RUN mkdir -p /app/
COPY requirements.txt /app/

# install requirements before code is models in order to
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000
#CMD ["python", "api.py"]
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"]