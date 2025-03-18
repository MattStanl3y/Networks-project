import pyshark
import pandas as pd
from datetime import datetime
import os

def analyze_capture(capture_file, output_csv=None):
    """
    Analyze a packet capture file and extract key information.
    
    Args:
        capture_file (str): Path to the capture file
        output_csv (str, optional): Path to save CSV results
    
    Returns:
        pandas.DataFrame: DataFrame containing packet information
    """
    if not os.path.exists(capture_file):
        print(f"Error: Capture file {capture_file} not found")
        return None
    
    print(f"Analyzing capture file: {capture_file}")
    
    # Initialize empty lists to store packet info
    timestamps = []
    protocols = []
    src_ips = []
    dst_ips = []
    src_ports = []
    dst_ports = []
    packet_lengths = []
    
    try:
        # Open the capture file
        cap = pyshark.FileCapture(capture_file)
        
        # Process each packet
        for packet in cap:
            # Get timestamp
            timestamps.append(packet.sniff_time)
            
            # Get packet length
            packet_lengths.append(int(packet.length))
            
            # Get IP info if available
            if hasattr(packet, 'ip'):
                src_ips.append(packet.ip.src)
                dst_ips.append(packet.ip.dst)
            else:
                src_ips.append(None)
                dst_ips.append(None)
            
            # Get protocol and port info
            if hasattr(packet, 'tcp'):
                protocols.append('TCP')
                src_ports.append(packet.tcp.srcport)
                dst_ports.append(packet.tcp.dstport)
            elif hasattr(packet, 'udp'):
                protocols.append('UDP')
                src_ports.append(packet.udp.srcport)
                dst_ports.append(packet.udp.dstport)
            else:
                # Use highest layer protocol name
                protocols.append(packet.highest_layer)
                src_ports.append(None)
                dst_ports.append(None)
        
        # Create DataFrame
        df = pd.DataFrame({
            'timestamp': timestamps,
            'protocol': protocols,
            'src_ip': src_ips,
            'dst_ip': dst_ips,
            'src_port': src_ports,
            'dst_port': dst_ports,
            'length': packet_lengths
        })
        
        # Calculate some basic statistics
        total_packets = len(df)
        total_bytes = df['length'].sum()
        duration = (df['timestamp'].max() - df['timestamp'].min()).total_seconds()
        avg_packet_size = df['length'].mean()
        protocol_counts = df['protocol'].value_counts()
        
        # Print summary
        print(f"\nCapture Summary:")
        print(f"Total packets: {total_packets}")
        print(f"Total bytes: {total_bytes}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Average packet size: {avg_packet_size:.2f} bytes")
        print(f"\nProtocol Distribution:")
        for protocol, count in protocol_counts.items():
            print(f"  {protocol}: {count} packets ({count/total_packets*100:.1f}%)")
        
        # Save to CSV if requested
        if output_csv:
            df.to_csv(output_csv, index=False)
            print(f"\nData saved to {output_csv}")
        
        return df
    
    except Exception as e:
        print(f"Error processing capture file: {e}")
        return None

if __name__ == "__main__":
    # Get input from user
    capture_file = input("Enter the capture file to analyze: ")
    output_csv = input("Enter CSV filename to save results [leave blank to skip]: ")
    
    output_csv = output_csv if output_csv.strip() else None
    analyze_capture(capture_file, output_csv)