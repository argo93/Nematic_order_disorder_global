import os
import numpy as np
import matplotlib.pyplot as plt
from analyze_nematic_order import analyze_nematic_order

# =========================================================================
# PARAMETER DEFINITIONS
# =========================================================================

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define path to the input image. We look for 'image2.PNG' in the 'images' subdirectory.
filename = os.path.abspath(os.path.join(script_dir, "..", "images", "image2.PNG"))

# Fallback to lower case if file not found (useful for cross-platform compatibility)
if not os.path.exists(filename):
    filename = os.path.abspath(os.path.join(script_dir, "..", "images", "image2.png"))

# parameters
sigma = 3.0       # Standard deviation of the Gaussian blur kernel (pixels)
box_size = 64     # Dimension of square grid boxes for local averaging (pixels)

# =========================================================================
# RUN ANALYSIS
# =========================================================================
print(f"Loading image from: {filename}")
print(f"Running analysis with sigma = {sigma}, box_size = {box_size}...")

try:
    S_field, theta_field, avg_S, global_S, U, V = analyze_nematic_order(
        filename=filename, 
        sigma=sigma, 
        box_size=box_size, 
        fancy=0
    )
except Exception as e:
    print(f"Error during analysis: {e}")
    # Try direct absolute path as a fallback
    fallback_path = "/Users/mukherjee/Documents/MATLAB/Nematic Skin/valeria/images/image2.PNG"
    print(f"Retrying with fallback absolute path: {fallback_path}")
    S_field, theta_field, avg_S, global_S, U, V = analyze_nematic_order(
        filename=fallback_path, 
        sigma=sigma, 
        box_size=box_size, 
        fancy=0
    )

# =========================================================================
# OPTIONAL POST-PROCESSING & PROFILE EXTRACTION
# =========================================================================
# Below is a Python equivalent of the commented MATLAB post-processing section.
# It extracts a 1D profile of S along the x-direction, averaged over a vertical band.
"""
# Define the vertical (y) bounds of the band of interest (in pixel/field coordinates)
y1 = 300
y2 = 450

# Ensure y-indices are within field bounds
if y2 < S_field.shape[0]:
    # Calculate the mean of S along the x-direction (axis 1) within the y1-y2 band
    Qy = np.mean(S_field[y1:y2, :], axis=0)

    # Plot the 1D profile
    plt.figure(figsize=(8, 4))
    plt.plot(Qy, linewidth=1.5, color='blue')
    plt.grid(True)
    plt.xlabel('x position')
    plt.ylabel('S nematic order')
    plt.title('Average Nematic Order Profile (S) along X-axis')
    plt.show()
else:
    print(f"Vertical bounds {y1}-{y2} exceed S_field height {S_field.shape[0]}.")
"""
