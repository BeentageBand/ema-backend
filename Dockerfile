FROM library/python:3.8
WORKDIR /app
COPY ./requirements.txt .

# Avoid that python write into the image
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN python3 -m pip install --upgrade pip \
      && python3 -m pip install -r requirements.txt

# Copy all to 1 layer
FROM scratch
WORKDIR /app
COPY --from=0 / /

# Run on 0.0.0.0 so docker can publish the port
CMD [ "python3", "manage.py", "runserver" , "0.0.0.0:8000"]