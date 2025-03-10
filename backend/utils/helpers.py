import socket

def get_local_ip():
    """Get the local IP address of the current machine"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # Fallback method
        return socket.gethostbyname(socket.gethostname())