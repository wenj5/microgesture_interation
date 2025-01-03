import numpy as np
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime 


class LandmarkTracker:
    def __init__(self, output_file = None):
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_file = f'landmark_trajectory_{timestamp}.csv'
        else: 
            self.output_file = output_file

        with open(self.output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['frame', 
                 'raw_x', 'raw_y', 'raw_z',
                 'filtered_x', 'filtered_y', 'filtered_z'])
        
        self.frame_count = 0

        self.fig = plt.figure(figsize= (10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.raw_trajectory = {'x':[], 'y':[], 'z':[]}
        self.filtered_trajectoty = {'x':[], 'y':[], 'z':[]}

    def update(self, raw_landmark, filtered_landmark):
        with open(self.output_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([self.frame_count,
                           raw_landmark[0], raw_landmark[1], raw_landmark[2],
                           filtered_landmark[0], filtered_landmark[1], filtered_landmark[2]])
        
        for i, coord in enumerate(['x', 'y', 'z']):
            self.raw_trajectory[coord].append(raw_landmark[i])
            self.filtered_trajectory[coord].append(filtered_landmark[i])
        
        self.frame_count += 1
        
    def visualize(self, show_plot=True):
        """
        Update the 3D visualization
        """
        self.ax.clear()
        
        # Plot raw trajectory in blue
        self.ax.plot3D(self.raw_trajectory['x'], 
                      self.raw_trajectory['y'], 
                      self.raw_trajectory['z'], 
                      'b-', label='Raw', alpha=0.5)
        
        # Plot filtered trajectory in red
        self.ax.plot3D(self.filtered_trajectory['x'], 
                      self.filtered_trajectory['y'], 
                      self.filtered_trajectory['z'], 
                      'r-', label='Filtered')
        
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Landmark Trajectory Comparison')
        self.ax.legend()
        
        if show_plot:
            plt.draw()
            plt.pause(0.001)  # Small pause to update the plot
            
    def save_plot(self, filename=None):
        """
        Save the current plot to a file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'trajectory_plot_{timestamp}.png'
            
        plt.savefig(filename)
        print(f"Plot saved to {filename}")