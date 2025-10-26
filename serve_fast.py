#!/usr/bin/env python3
import http.server
import socketserver
import socket
import webbrowser
import os
import gzip
import io
from urllib.parse import urlparse

# Get the local IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# Fast handler with compression
class FastHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def end_headers(self):
        # Add performance headers
        self.send_header('Cache-Control', 'public, max-age=300')  # 5 minutes cache
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    
    def do_GET(self):
        # Check if client accepts gzip
        if 'gzip' in self.headers.get('Accept-Encoding', ''):
            self.send_response(200)
            
            # Get file content
            path = self.translate_path(self.path)
            if os.path.isfile(path):
                with open(path, 'rb') as f:
                    content = f.read()
                
                # Compress content
                compressed_content = gzip.compress(content)
                
                # Send headers
                self.send_header('Content-Type', self.guess_type(path))
                self.send_header('Content-Length', str(len(compressed_content)))
                self.send_header('Content-Encoding', 'gzip')
                self.send_header('Cache-Control', 'public, max-age=300')
                self.end_headers()
                
                # Send compressed content
                self.wfile.write(compressed_content)
                return
        
        # Fallback to normal serving
        super().do_GET()

# Set the port
PORT = 8000

# Change to the directory containing the HTML file
os.chdir(r"C:\Users\davis\Desktop\Almaza")

# Create fast server
class FastTCPServer(socketserver.TCPServer):
    allow_reuse_address = True
    request_queue_size = 200
    
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        super().server_bind()

# Start the fast server
with FastTCPServer(("0.0.0.0", PORT), FastHTTPRequestHandler) as httpd:
    local_ip = get_local_ip()
    print(f"⚡ FAST Server running at:")
    print(f"Local: http://localhost:{PORT}")
    print(f"Network: http://{local_ip}:{PORT}")
    print(f"\n📱 Open this URL on your phone: http://{local_ip}:{PORT}/almaza-perfect-layout.html")
    print("\n🚀 Speed optimizations:")
    print("   - Gzip compression enabled")
    print("   - Smart caching (5 minutes)")
    print("   - Optimized socket settings")
    print("   - Larger request queue")
    print("\nPress Ctrl+C to stop the server")
    
    # Open in browser automatically
    webbrowser.open(f"http://localhost:{PORT}/almaza-perfect-layout.html")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


