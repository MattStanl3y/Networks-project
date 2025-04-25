import os
from capture import capture_traffic, get_user_input
from process import analyze_capture
from visualize import visualize_traffic

def main():
    # Create results directory if it doesn't exist
    if not os.path.exists('results'):
        os.makedirs('results')
        print("Created results directory")
    
    # Get user input
    interface, duration, my_ip, game_port, game_name = get_user_input()
    
    # Capture traffic
    capture_file = capture_traffic(
        duration=duration,
        output_file="results/result.pcapng",
        interface=interface,
        my_ip=my_ip,
        game_port=game_port,
        game_name=game_name
    )
    
    print(f"Created capture file: {os.path.abspath(capture_file)}")
    
    # Process the capture
    analyze_capture(capture_file, "results/result.csv")
    
    # Visualize the data
    visualize_traffic("results/result.csv")

if __name__ == "__main__":
    main()