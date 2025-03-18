import pyshark
import pandas as pd
import os

def analyze_capture(capture_file="result.pcapng", output_csv="result.csv"):
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
        # Process each packet
        cap = pyshark.FileCapture(capture_file)
        for packet in cap:
            timestamps.append(packet.sniff_time)
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
        
        # Calculate basic statistics
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
        
        # Save to CSV
        df.to_csv(output_csv, index=False)
        print(f"\nData saved to {output_csv}")
        
        return df
    
    except Exception as e:
        print(f"Error processing capture file: {e}")
        return None

if __name__ == "__main__":
    analyze_capture()