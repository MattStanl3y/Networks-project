import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

def visualize_traffic(csv_file="result.csv"):
    try:
        # Load the CSV data
        df = pd.read_csv(csv_file)
        
        # Convert timestamp string to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Calculate time since start for each packet
        start_time = df['timestamp'].min()
        df['time_seconds'] = (df['timestamp'] - start_time).dt.total_seconds()
        df['time_bucket'] = df['time_seconds'].apply(lambda x: int(x))
        
        # Create a figure with multiple subplots
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        
        # 1. Packet size distribution
        axs[0, 0].hist(df['length'], bins=20, color='skyblue', edgecolor='black')
        axs[0, 0].set_title('Packet Size Distribution')
        axs[0, 0].set_xlabel('Packet Size (bytes)')
        axs[0, 0].set_ylabel('Number of Packets')
        
        # 2. Protocol distribution
        protocol_counts = df['protocol'].value_counts()
        axs[0, 1].bar(protocol_counts.index, protocol_counts.values, color='lightgreen')
        axs[0, 1].set_title('Protocol Distribution')
        axs[0, 1].set_ylabel('Number of Packets')
        axs[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Traffic over time (packet count)
        packets_per_second = df.groupby('time_bucket').size()
        axs[1, 0].plot(packets_per_second.index, packets_per_second.values, 'b-')
        axs[1, 0].set_title('Packets per Second')
        axs[1, 0].set_xlabel('Time (seconds)')
        axs[1, 0].set_ylabel('Packet Count')
        
        # 4. Bandwidth over time
        bandwidth = df.groupby('time_bucket')['length'].sum() / 1024  # Convert to KB
        axs[1, 1].plot(bandwidth.index, bandwidth.values, 'r-')
        axs[1, 1].set_title('Bandwidth Usage')
        axs[1, 1].set_xlabel('Time (seconds)')
        axs[1, 1].set_ylabel('KB per Second')
        
        plt.tight_layout()
        
        # Save the figure
        output_file = "result_analysis.png"
        plt.savefig(output_file)
        print(f"Visualization saved to {output_file}")
        
        # Show the plot
        plt.show()
            
    except Exception as e:
        print(f"Error creating visualizations: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        visualize_traffic(csv_file)
    else:
        visualize_traffic()