import subprocess
import time
import os
import platform
import socket

def list_interfaces():
    # Check if we're on Windows or macOS and use appropriate tshark path
    if platform.system() == "Windows":
        cmd = ["tshark", "-D"]
    else:  # macOS or other
        cmd = ["/Applications/Wireshark.app/Contents/MacOS/tshark", "-D"]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("Available interfaces:")
    print(result.stdout)

def get_my_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Could not automatically detect IP: {e}")
        return None

def get_user_input():
    # Get and confirm IP address
    detected_ip = get_my_ip()
    if detected_ip:
        print(f"Detected your IP address as: {detected_ip}")
        ip_confirm = input(f"Is this your correct IP address? [Y/n]: ").strip().lower()
        if ip_confirm == "" or ip_confirm.startswith("y"):
            my_ip = detected_ip
        else:
            my_ip = input("Enter your correct IP address: ").strip()
    else:
        my_ip = input("Could not detect IP automatically. Enter your IP address: ").strip()
    
    # Game port selection
    print("\nCommon game UDP ports:")
    print("1. Call of Duty: 3074")
    print("2. Fortnite: 9000")
    print("3. Apex Legends: 37015")
    print("4. Valorant: 7081")
    print("5. Custom port")
    
    port_choice = input("\nSelect game (1-5): ").strip()
    if port_choice == "1":
        game_port = 3074
        game_name = "Call of Duty"
    elif port_choice == "2":
        game_port = 9000
        game_name = "Fortnite"
    elif port_choice == "3":
        game_port = 37015
        game_name = "Apex Legends"
    elif port_choice == "4":
        game_port = 7081
        game_name = "Valorant"
    elif port_choice == "5":
        game_port = int(input("Enter custom UDP port number: "))
        game_name = "Custom"
    else:
        game_port = 3074  # Default to Call of Duty
        game_name = "Call of Duty"
    
    # Capture duration
    duration_str = input("\nEnter capture duration in seconds [60]: ")
    duration = int(duration_str) if duration_str.strip() else 60
    
    # Interface selection (optional)
    print("\nAvailable network interfaces:")
    list_interfaces()
    interface = input("\nSelect interface (leave blank for auto): ").strip()
    
    # Final confirmation to start
    print(f"\nReady to capture {game_name} traffic on port {game_port}")
    print(f"IP Address: {my_ip}")
    print(f"Duration: {duration} seconds")
    print(f"Interface: {'Auto' if not interface else interface}")
    
    start = input("\nType 'start' to begin capture: ").strip().lower()
    if start != "start":
        print("Capture cancelled.")
        exit()
    
    return interface, duration, my_ip, game_port, game_name

def capture_traffic(duration=60, output_file="results/result.pcapng", interface=None, my_ip="127.0.0.1", game_port=3074, game_name="Unknown"):
    # Update filter for selected game
    game_filter = f"host {my_ip} and udp port {game_port}"
    
    # Build the tshark command for Windows
    cmd = ["C:\\Program Files\\Wireshark\\tshark.exe", "-w", output_file]
    
    # Add interface if specified
    if interface:
        cmd.extend(["-i", interface])
    
    # Add filter to command
    cmd.extend(["-f", game_filter])
    
    # Start capture
    print(f"Starting capture for {game_name} on port {game_port}...")
    print(f"Capturing for {duration} seconds...")
    print(f"Using filter: {game_filter}")
    
    process = subprocess.Popen(cmd)
    time.sleep(duration)
    process.terminate()
    print(f"Capture complete. File saved to {output_file}")
    
    return output_file

if __name__ == "__main__":
    # Get user input
    interface, duration, my_ip, game_port, game_name = get_user_input()
    
    # Capture traffic with standardized output filename
    capture_file = capture_traffic(
        duration=duration,
        output_file="results/result.pcapng",
        interface=interface,
        my_ip=my_ip,
        game_port=game_port,
        game_name=game_name
    )
    
    print(f"Created capture file: {os.path.abspath(capture_file)}")