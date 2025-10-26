#!/usr/bin/env python3
import http.server
import socketserver
import socket
import webbrowser
import os

# Get the local IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to a remote server to get local IP
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# Set the port
PORT = 8000

# Change to the directory containing the HTML file
os.chdir(r"C:\Users\davis\Desktop\Almaza")

# Create a simple HTTP server
Handler = http.server.SimpleHTTPRequestHandler

# Start the server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    local_ip = get_local_ip()
    print(f"Server running at:")
    print(f"Local: http://localhost:{PORT}")
    print(f"Network: http://{local_ip}:{PORT}")
    print(f"\nOpen this URL on your phone: http://{local_ip}:{PORT}/almaza-perfect-layout.html")
    print("\nPress Ctrl+C to stop the server")
    
    # Open in browser automatically
    webbrowser.open(f"http://localhost:{PORT}/almaza-perfect-layout.html")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


























