# PyChat

A basic chat room application built in Python to facilitate real-time communication between clients through a central server.

## Features

- Concurrent Client Communication: Supports multiple clients communicating with each other via the server.

- Server-Client Architecture: A centralized server manages all client messages.

- Encryption (Coming Soon): Traffic between clients and the server will be encrypted for secure communication.

## How It Works

1. Server:

  - Listens for incoming client connections.

  - Broadcasts messages received from one client to all connected clients.

2. Client:

  - Connects to the server and sends messages.

  - Receives messages from other clients through the server.

## Setup Instructions

### Prerequisites

- Python 3.x installed on your system.

### Installation

1. Clone the repository:

  ```
  git clone https://github.com/JosephDePalo/pychat
  cd pychat
  ```

2. Run the server:

  ```
  python server.py <PORT>
  ```

3. Run the client:

  ```
  python client.py <PORT>
  ```

Connect multiple clients by running client.py on different terminals or machines.

## Planned Features

Traffic Encryption: Secure communication using protocols like RSA or AES.

Naming Feature: Ability for clients to nickname themselves.

Authentication: User login and registration system.

Persistent Chat History: Store messages for future retrieval.
