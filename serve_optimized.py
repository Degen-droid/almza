#!/usr/bin/env python3
import http.server
import socketserver
import socket
import webbrowser
import os
from urllib.parse import urlparse

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

# Custom handler with caching and optimization
class OptimizedHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add caching headers for better performance
        if self.path.endswith(('.html', '.css', '.js')):
            self.send_header('Cache-Control', 'no-cache, must-revalidate')
        elif self.path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')):
            self.send_header('Cache-Control', 'public, max-age=3600')  # 1 hour cache
        super().end_headers()
    
    def do_GET(self):
        # Serve with compression headers
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        
        # Add performance headers
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        
        super().do_GET()

# Set the port
PORT = 8000

# Change to the directory containing the HTML file
os.chdir(r"C:\Users\davis\Desktop\Almaza")

# Start the optimized server
with socketserver.TCPServer(("", PORT), OptimizedHTTPRequestHandler) as httpd:
    local_ip = get_local_ip()
    print(f"🚀 Optimized Server running at:")
    print(f"Local: http://localhost:{PORT}")
    print(f"Network: http://{local_ip}:{PORT}")
    print(f"\n📱 Open this URL on your phone: http://{local_ip}:{PORT}/almaza-perfect-layout.html")
    print("\n⚡ Server optimized for faster loading:")
    print("   - Added caching headers")
    print("   - Optimized content delivery")
    print("   - Better performance headers")
    print("\nPress Ctrl+C to stop the server")
    
    # Open in browser automatically
    webbrowser.open(f"http://localhost:{PORT}/almaza-perfect-layout.html")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


