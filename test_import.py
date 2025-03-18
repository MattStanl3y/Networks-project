import pyshark
import os

def verify_capture(capture_file):
    """
    Verify that we can open and read a capture file by printing summary information.
    
    Args:
        capture_file (str): Path to the capture file
    """
    if not os.path.exists(capture_file):
        print(f"Error: Capture file {capture_file} not found")
        return
    
    print(f"Opening capture file: {capture_file}")
    
    try:
        # Open the capture file
        cap = pyshark.FileCapture(capture_file)
        
        # Count the first 10 packets (if available)
        packet_count = 0
        for packet in cap:
            packet_count += 1
            print(f"Packet {packet_count}: {packet.length} bytes, Layer names: {packet.layers}")
            
            # Print more details about the first packet
            if packet_count == 1:
                print("\nFirst packet details:")
                print(f"  Timestamp: {packet.sniff_time}")
                print(f"  Length: {packet.length} bytes")
                if hasattr(packet, 'ip'):
                    print(f"  Source IP: {packet.ip.src}")
                    print(f"  Destination IP: {packet.ip.dst}")
                if hasattr(packet, 'tcp'):
                    print(f"  Protocol: TCP")
                    print(f"  Source Port: {packet.tcp.srcport}")
                    print(f"  Destination Port: {packet.tcp.dstport}")
                elif hasattr(packet, 'udp'):
                    print(f"  Protocol: UDP")
                    print(f"  Source Port: {packet.udp.srcport}")
                    print(f"  Destination Port: {packet.udp.dstport}")
            
            # Limit to 10 packets for test
            if packet_count >= 10:
                break
        
        print(f"\nSuccessfully read {packet_count} packets")
        
    except Exception as e:
        print(f"Error processing capture file: {e}")

if __name__ == "__main__":
    # Test with the file created by capture.py
    verify_capture("test_capture.pcapng")