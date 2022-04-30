FROM python
WORKDIR /chatroom
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 3000
CMD python3 app.py