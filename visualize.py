import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
from scipy.ndimage import gaussian_filter1d

def visualize_traffic(csv_file):
    try:
        # Check if file exists
        if not os.path.exists(csv_file):
            print(f"Error: CSV file not found: {csv_file}")
            return
        
        # Load the CSV data
        df = pd.read_csv(csv_file)
        
        # Convert timestamp string to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Calculate time since start for each packet
        start_time = df['timestamp'].min()
        df['time_seconds'] = (df['timestamp'] - start_time).dt.total_seconds()
        df['time_bucket'] = df['time_seconds'].apply(lambda x: round(x, 1))  # 0.1 second buckets
        
        # Create a figure with multiple subplots
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        
        # Packet size distribution
        axs[0, 0].hist(df['length'], bins=20, color='skyblue', edgecolor='black')
        axs[0, 0].set_title('Packet Size Distribution')
        axs[0, 0].set_xlabel('Packet Size (bytes)')
        axs[0, 0].set_ylabel('Number of Packets')
        
        # Traffic Direction (Incoming vs Outgoing)
        outgoing = df[df['src_ip'] == df['src_ip'].iloc[0]].shape[0]
        incoming = df[df['dst_ip'] == df['src_ip'].iloc[0]].shape[0]
        
        axs[0, 1].bar(['Outgoing', 'Incoming'], [outgoing, incoming], color=['orange', 'green'])
        axs[0, 1].set_title('Traffic Direction')
        axs[0, 1].set_ylabel('Number of Packets')
        
        # Packets per second over time - SMOOTHED
        packets_per_time = df.groupby('time_bucket').size()
        
        # Create a complete time range with all points
        full_time_range = np.arange(0, df['time_seconds'].max() + 0.1, 0.1)
        
        # Create a full series with all time points
        full_packets = pd.Series(index=full_time_range, data=0)
        
        # Fill in the data we have
        for time_point, count in packets_per_time.items():
            if time_point in full_packets.index:
                full_packets[time_point] = count
        
        #  Gaussian for smoother curve
        smooth_packets = gaussian_filter1d(full_packets.values, sigma=2)
        
        # Plot the smoothed data
        axs[1, 0].plot(full_packets.index, smooth_packets, 'b-', linewidth=2)
        axs[1, 0].set_title('Packets per Second (Smoothed)')
        axs[1, 0].set_xlabel('Time (seconds)')
        axs[1, 0].set_ylabel('Packet Count')
        
        # Make sure the x-axis shows the full duration
        max_time = df['time_seconds'].max()
        axs[1, 0].set_xlim(0, max_time)
        
        # Bandwidth over time - SMOOTHED
        bandwidth = df.groupby('time_bucket')['length'].sum() / 1024  # Convert to KB
        
        # Create a full series for bandwidth with all time points
        full_bandwidth = pd.Series(index=full_time_range, data=0)
        
        # Fill in the data we have
        for time_point, bw in bandwidth.items():
            if time_point in full_bandwidth.index:
                full_bandwidth[time_point] = bw
        
        # Gaussian for a smoother curve
        smooth_bandwidth = gaussian_filter1d(full_bandwidth.values, sigma=2)
        
        # Plot the smoothed data
        axs[1, 1].plot(full_bandwidth.index, smooth_bandwidth, 'r-', linewidth=2)
        axs[1, 1].set_title('Bandwidth Usage (Smoothed)')
        axs[1, 1].set_xlabel('Time (seconds)')
        axs[1, 1].set_ylabel('KB per Second')
        
        # Make sure the x-axis shows the full duration
        axs[1, 1].set_xlim(0, max_time)
        
        plt.tight_layout()
        
        # Save the figure
        output_file = "results/result_analysis.png"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        plt.savefig(output_file)
        print(f"Visualization saved to {output_file}")
        
        # Show the plot
        plt.show()
        
    except Exception as e:
        print(f"Error creating visualizations: {e}")

if __name__ == "__main__":
    # Create results directory if it doesn't exist
    if not os.path.exists('results'):
        os.makedirs('results')
        print("Created results directory")
    
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        visualize_traffic(csv_file)
    else:
        visualize_traffic("results/result.csv")