import socket
import json
import os
import base64

def send_blender_command(cmd_type: str, params: dict = None, host="127.0.0.1", port=9876, timeout=15.0):
    """Send command to live Blender MCP server on port 9876."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((host, port))
    payload = {"type": cmd_type}
    if params:
        payload["params"] = params
    s.sendall(json.dumps(payload).encode("utf-8"))
    
    # Read full response
    buffer = b""
    while True:
        chunk = s.recv(16384)
        if not chunk:
            break
        buffer += chunk
        try:
            # Check if valid JSON received
            data = json.loads(buffer.decode("utf-8"))
            s.close()
            return data
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
    s.close()
    return json.loads(buffer.decode("utf-8")) if buffer else {}

def execute_bpy(code_str: str):
    """Execute arbitrary python/bpy script inside Blender."""
    return send_blender_command("execute_code", {"code": code_str})

def capture_screenshot(output_path: str, max_size=1920, format="png"):
    """Capture Blender viewport screenshot and save to disk."""
    res = send_blender_command("get_viewport_screenshot", {"filepath": output_path, "max_size": max_size, "format": format})
    if os.path.exists(output_path):
        return output_path
    return res

if __name__ == "__main__":
    status = send_blender_command("ping")
    print("Ping:", status)
