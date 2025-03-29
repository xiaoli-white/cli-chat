import sys
import signal
import socket
import threading
import select

server = None

clients = []

running = True

def broadcast_message(message, sender, address):
  """
  广播消息给所有客户端，除了发送者
  """

  msg = f"{address}: {message}"
  for client in clients:
    if client != sender:
      try:
        client.send(msg.encode('utf-8'))
      except:
        print(f"Error sending message to {address}")
        clients.remove(client)
        client.close()

def handle_client(client_socket, address):
  """
  处理单个客户端的线程函数
  """
  print(f"Accepted connection from {address}")
  while running:
    try:
      message = client_socket.recv(1024).decode('utf-8')
      if message:
        print(f"Received message from {address}: {message}")
        broadcast_message(message, client_socket, address)
      else:
        break
    except:
      break

  print(f"Connection with {address} closed")
  clients.remove(client_socket)
  client_socket.close()

def start_server():
  """
  启动服务器
  """
  SERVER_ADDRESS = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
  SERVER_PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 12345

  global server
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind((SERVER_ADDRESS, SERVER_PORT))
  server.listen()
  print(f"Server started on {SERVER_ADDRESS}:{SERVER_PORT}, waiting for connections...")

  while running:
    readable, _, _ = select.select([server], [], [], 1)
    if readable:
      client_socket, address = server.accept()
      clients.append(client_socket)
      client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
      client_thread.start()

def signal_handler(signal, frame):
  """
  信号处理函数，用于捕获 Ctrl+C
  """
  global running
  running = False
  print("Server is shutting down...")
  for client in clients:
    client.close()
  server.close()
  print("Server has been shut down.")

if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal_handler)
  start_server()