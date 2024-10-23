FROM python

ADD main.py .
ADD my_socket.py .
ADD test.py .

CMD ["python", "./main.py"]