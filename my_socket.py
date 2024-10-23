import socket
import time
import json
from datetime import datetime

class MySocket:
    def __init__(self, window_length : int, sliding_interval : int ) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.window_length = window_length
        self.sliding_interval = sliding_interval
        self.buffer = b''
        self.temp_buffer = b''

    def connect(self, host : str, port : int) -> None:
        self.sock.connect((host, port))
    
    def process(self) -> None:
        output = {"startTime": "", "endTime": "", "answer_counts":  {}}
        s_time = self.receive()
        start_time = datetime.strptime(s_time, "%Y-%m-%dT%H:%M:%S.%f")

        while True:
            time.sleep(0.1)
            e_time = self.receive()
            end_time = datetime.strptime(e_time, "%Y-%m-%dT%H:%M:%S.%f")
            elapsed_time = round((end_time - start_time).total_seconds(), 1)

            if elapsed_time >= self.window_length:
                answer_counts = self.__calculate()

                output['startTime'] = start_time.strftime("%Y-%m-%dT%H:%M:%S") + 'Z'
                output['endTime'] = end_time.strftime("%Y-%m-%dT%H:%M:%S") + 'Z'
                output['answer_counts'] = answer_counts

                start_time = self.__get_creation_date()

                print(output)

    def receive(self) -> str:
        local_buffer = b''
        while b'\n' not in local_buffer:
            chunk = self.sock.recv(1024)
            if not chunk:
                raise RuntimeError("socket connection broken")
            self.buffer += chunk
            local_buffer += self.temp_buffer + chunk

        message, self.temp_buffer = local_buffer.split(b'\n', 1)
        
        json_message = json.loads(message.decode())
        
        return json_message['creationdate']

    def __get_creation_date(self) -> datetime:
        json_message = self.buffer.split(b'\n')[0]
        decoded_json_message = json.loads(json_message.decode())
        creation_date = datetime.strptime(decoded_json_message['creationdate'], "%Y-%m-%dT%H:%M:%S.%f")
        return creation_date
    
    def __calculate(self) -> dict:
        answer_counts = {"cooking" : 0, "datascience": 0, "stackoverflow": 0}
        index = 0
        elapsed_time = 0
        for i in range(len(self.buffer.split(b'\n'))):
            if i == 0:
                first_creation_date = self.__get_creation_date()
            else:
                if elapsed_time <= self.sliding_interval:
                    message, self.buffer = self.buffer.split(b'\n', 1)
                else:
                    message = self.buffer.split(b'\n')[index]
                    index += 1
                json_message = json.loads(message.decode())
                creation_date = datetime.strptime(json_message['creationdate'], "%Y-%m-%dT%H:%M:%S.%f")
                elapsed_time = round((creation_date - first_creation_date).total_seconds(), 1)
                answer_counts[json_message['site']] += 1
        return answer_counts
