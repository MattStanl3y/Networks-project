import pyshark
import pandas as pd
import os

def analyze_capture(capture_file, output_csv):
    # Verify input paths
    if not os.path.exists(capture_file):
        print(f"Error: Capture file {capture_file} not found")
        return None
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    
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
        packet_count = 0
        
        for packet in cap:
            # Add a progress indicator for large files
            packet_count += 1
            if packet_count % 1000 == 0:
                print(f"Processed {packet_count} packets...")
            
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
                # Check for HTTP/HTTPS
                if hasattr(packet, 'http'):
                    protocols.append('HTTP')
                elif hasattr(packet, 'tls'):
                    protocols.append('HTTPS')
                else:
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
        duration = (df['timestamp'].max() - df['timestamp'].min()).total_seconds() if len(df) > 1 else 0
        avg_packet_size = df['length'].mean() if len(df) > 0 else 0
        protocol_counts = df['protocol'].value_counts()
        
        # Print summary
        print(f"Capture Summary:")
        print(f"Total packets: {total_packets}")
        print(f"Total bytes: {total_bytes}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Average packet size: {avg_packet_size:.2f} bytes")
        print(f"Protocol Distribution:")
        for protocol, count in protocol_counts.items():
            print(f"  {protocol}: {count} packets ({count/total_packets*100:.1f}%)")
        
        # Save to CSV
        df.to_csv(output_csv, index=False)
        print(f"Data saved to {output_csv}")
        
        return df
    
    except Exception as e:
        print(f"Error processing capture file: {e}")
        return None

if __name__ == "__main__":
    # Create results directory if it doesn't exist
    if not os.path.exists('results'):
        os.makedirs('results')
        print("Created results directory")
    
    analyze_capture("results/result.pcapng", "results/result.csv")