FROM orgoro/dlib-opencv-python

WORKDIR /app

COPY . .


# RUN pip3 install cmake
RUN pip3 install flask
RUN pip install fastapi
RUN pip install uvicorn
RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD uvicorn --host=0.0.0.0 --port 8000 main:app



