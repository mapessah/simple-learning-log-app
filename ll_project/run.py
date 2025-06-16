import subprocess
import time
import webbrowser

# Start Django server
print('Starting server...')
server = subprocess.Popen(["python3", "manage.py", "runserver"])

# Wait a bit before opening the browser
time.sleep(3)

# Open default browser to server URL
webbrowser.open("http://127.0.0.1:8000")

# Show exit prompt
print("\n✅ Server is running at http://127.0.0.1:8000")
print("Type 'q' or 'exit' to stop the server.\n")

# Wait for user to quit
while True:
    cmd = input(">> ").strip().lower()
    if cmd in ['q', 'exit']:
        print("🛑 Shutting down server...")
        server.terminate()
        break
