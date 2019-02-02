FROM arm32v7/python:3

WORKDIR /opt/sense_temperature

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY sense_temperature.py ./

CMD [ "python", "./sense_temperature.py" ]
