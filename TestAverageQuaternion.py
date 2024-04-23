import numpy as np

# Function to normalize a quaternion
def normalize_quaternion(q):
    norm = np.linalg.norm(q)
    return q / norm

# Function to average quaternions
def average_quaternions(quaternions):
    # Normalize all quaternions
    normalized_quaternions = [normalize_quaternion(q) for q in quaternions]
    
    # Calculate the sum of quaternions
    sum_quaternion = np.sum(normalized_quaternions, axis=0)
    
    # Normalize the sum to get the average quaternion
    average_quaternion = normalize_quaternion(sum_quaternion)
    
    return average_quaternion

# Example quaternions (replace with your quaternions)
quaternions = [
    np.array([0.707, 0.0, 0.707, 0.0]),
    np.array([0.0, 0.707, 0.0, 0.707]),
    np.array([0.5, 0.5, 0.5, 0.5])
]

# Calculate the average quaternion
average_q = average_quaternions(quaternions)
print("Average Quaternion:", average_q)
