import socket
import struct

def convert_ip_to_int(ip_address):
    return struct.unpack("!I", socket.inet_aton(ip_address))[0]

def convert_int_to_ip(integer_address):
    return socket.inet_ntoa(struct.pack("!I", integer_address))

LOCAL_IP_ADDRESS = socket.gethostbyname(socket.gethostname())
LOCAL_IP_INT_VALUE = convert_ip_to_int(LOCAL_IP_ADDRESS)

PORT_PRIMARY = 10025
PORT_SECONDARY = 10125

socket_primary = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_secondary = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

socket_primary.bind(("", PORT_PRIMARY))
socket_secondary.bind(("", PORT_SECONDARY))

message_handlers = {
    1: lambda data, sender: process_type_1(data, sender),
    2: lambda data, sender: process_type_2(data, sender),
    3: lambda data, sender: process_type_3(data, sender),
    4: lambda data, sender: process_type_4(data, sender),
    5: lambda data, sender: process_type_5(data, sender),
    101: lambda data, sender: process_type_101(data, sender),
    102: lambda data, sender: process_type_102(data, sender),
    103: lambda data, sender: process_type_103(data, sender),
}

def process_message(received_data, sender):
    message_type, external_port, external_ip, local_ip = struct.unpack("!IIII", received_data)
    handler_function = message_handlers.get(message_type)

    if handler_function:
        handler_function((message_type, external_port, external_ip, local_ip), sender)
    else:
        raise ValueError(f"Unknown message type: {message_type}")

def process_type_1(*args): pass
def process_type_2(*args): pass
def process_type_3(*args): pass
def process_type_4(*args): pass
def process_type_5(*args): pass

def process_type_101(message_data, sender):
    message_type, ext_port, ext_addr, local_addr = message_data
    response = struct.pack("!IIII", message_type, sender[1], convert_ip_to_int(sender[0]), LOCAL_IP_INT_VALUE)
    socket_primary.sendto(response, sender)

def process_type_102(message_data, sender):
    message_type, ext_port, ext_addr, local_addr = message_data
    response = struct.pack("!IIII", message_type, sender[1], convert_ip_to_int(sender[0]), LOCAL_IP_INT_VALUE)
    socket_secondary.sendto(response, sender)

def process_type_103(message_data, sender):
    message_type, ext_port, ext_addr, local_addr = message_data
    response = struct.pack("!IIII", message_type, sender[1], convert_ip_to_int(sender[0]), LOCAL_IP_INT_VALUE)
    socket_primary.sendto(response, sender)

while True:
    data_received, sender_address = socket_primary.recvfrom(16)
    process_message(data_received, sender_address)