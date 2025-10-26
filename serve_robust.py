#!/usr/bin/env python3
import http.server
import socketserver
import socket
import webbrowser
import os
import threading
import time

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

# Custom handler with better error handling
class RobustHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def log_message(self, format, *args):
        # Custom logging to avoid connection errors in logs
        print(f"[{time.strftime('%H:%M:%S')}] {format % args}")
    
    def handle_one_request(self):
        try:
            super().handle_one_request()
        except (ConnectionResetError, BrokenPipeError, OSError) as e:
            # Silently handle connection errors that are common with mobile browsers
            pass
    
    def end_headers(self):
        # Add CORS headers for better compatibility
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

# Set the port
PORT = 8000

# Change to the directory containing the HTML file
os.chdir(r"C:\Users\davis\Desktop\Almaza")

# Create server with better socket options
class RobustTCPServer(socketserver.TCPServer):
    allow_reuse_address = True
    request_queue_size = 100
    
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()

# Start the robust server
with RobustTCPServer(("0.0.0.0", PORT), RobustHTTPRequestHandler) as httpd:
    local_ip = get_local_ip()
    print(f"🚀 Robust Server running at:")
    print(f"Local: http://localhost:{PORT}")
    print(f"Network: http://{local_ip}:{PORT}")
    print(f"\n📱 Open this URL on your phone: http://{local_ip}:{PORT}/almaza-perfect-layout.html")
    print("\n🔧 Server improvements:")
    print("   - Better connection handling")
    print("   - CORS headers for cross-origin requests")
    print("   - Error-resistant request processing")
    print("   - Optimized socket settings")
    print("\nPress Ctrl+C to stop the server")
    
    # Open in browser automatically
    webbrowser.open(f"http://localhost:{PORT}/almaza-perfect-layout.html")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


