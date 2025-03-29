import sys
import socket
import threading

def receive_messages(client_socket):
  """
  接收服务器发送的消息
  """
  while True:
    try:
      message = client_socket.recv(1024).decode('utf-8')
      if message:
        print(message)
    except:
      print("You have been disconnected from the server.")
      client_socket.close()
      break

def send_messages(client_socket):
  """
  发送消息到服务器
  """
  while True:
    message = input()
    if message.lower() == '/exit':
      client_socket.close()
      break
    client_socket.send(message.encode('utf-8'))

def start_client():
  """
  启动客户端
  """
  SERVER_ADDRESS = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
  SERVER_PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 12345

  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect((SERVER_ADDRESS, SERVER_PORT))
  print("Connected to the server. Type your messages below (type '/exit' to quit):")

  receive_thread = threading.Thread(target=receive_messages, args=(client,))
  send_thread = threading.Thread(target=send_messages, args=(client,))

  receive_thread.start()
  send_thread.start()

  receive_thread.join()
  send_thread.join()

if __name__ == "__main__":
    start_client()