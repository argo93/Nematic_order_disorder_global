import os
import numpy as np
import matplotlib.pyplot as plt
from analyze_nematic_order import analyze_nematic_order

# =========================================================================
# STATISTICAL ANALYSIS OF DIRECTOR FLUCTUATIONS
# =========================================================================
# This script compares the fluctuations of director angles from two different 
# images (image1.PNG and image2.PNG) to analyze order vs. disorder.

# 1. Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
file1 = os.path.abspath(os.path.join(script_dir, "..", "images", "image1.PNG"))
file2 = os.path.abspath(os.path.join(script_dir, "..", "images", "image2.PNG"))

# Fallbacks for lowercase extensions
if not os.path.exists(file1):
    file1 = os.path.abspath(os.path.join(script_dir, "..", "images", "image1.png"))
if not os.path.exists(file2):
    file2 = os.path.abspath(os.path.join(script_dir, "..", "images", "image2.png"))

print("Running nematic analysis for image 1 (image1.PNG)...")
try:
    _, theta1_scaled, _, _, _, _ = analyze_nematic_order(file1, sigma=3.0, box_size=64, fancy=0)
except Exception as e:
    print(f"Failed to analyze image 1: {e}")
    # Fallback to absolute paths
    file1 = "/Users/mukherjee/Documents/MATLAB/Nematic Skin/valeria/images/image1.PNG"
    _, theta1_scaled, _, _, _, _ = analyze_nematic_order(file1, sigma=3.0, box_size=64, fancy=0)

print("\nRunning nematic analysis for image 2 (image2.PNG)...")
try:
    _, theta2_scaled, _, _, _, _ = analyze_nematic_order(file2, sigma=3.0, box_size=64, fancy=0)
except Exception as e:
    print(f"Failed to analyze image 2: {e}")
    # Fallback to absolute paths
    file2 = "/Users/mukherjee/Documents/MATLAB/Nematic Skin/valeria/images/image2.PNG"
    _, theta2_scaled, _, _, _, _ = analyze_nematic_order(file2, sigma=3.0, box_size=64, fancy=0)

# The outputs from analyze_nematic_order are theta_field, which are scaled as (theta / pi).
# We convert them back to radians:
theta1 = theta1_scaled * np.pi
theta2 = theta2_scaled * np.pi

# 2. Calculate angular fluctuations (deviations from the mean) in degrees
dTheta1 = (theta1 - np.mean(theta1)) * 180.0 / np.pi
dTheta2 = (theta2 - np.mean(theta2)) * 180.0 / np.pi

# Flatten the arrays to compute statistical metrics over all grid points
dTheta1_flat = dTheta1.flatten()
dTheta2_flat = dTheta2.flatten()

# 3. Calculate variances
varTheta1 = np.var(dTheta1_flat)
varTheta2 = np.var(dTheta2_flat)

print("\n=========================================================================")
print(f"Variance of Theta 1 (image1.PNG)  : {varTheta1:.4f} deg^2")
print(f"Variance of Theta 2 (image2.PNG) : {varTheta2:.4f} deg^2")
print("=========================================================================")

# 4. Plot comparative histograms
plt.figure(figsize=(8, 6))

# Define common bins for a fair comparison
min_val = min(np.min(dTheta1_flat), np.min(dTheta2_flat))
max_val = max(np.max(dTheta1_flat), np.max(dTheta2_flat))
bins = np.linspace(min_val, max_val, 30)

# MATLAB's 'Normalization' = 'probability' makes the sum of bar heights equal to 1.
# We achieve this in matplotlib by passing weights = 1/N.
weights1 = np.ones_like(dTheta1_flat) / len(dTheta1_flat)
weights2 = np.ones_like(dTheta2_flat) / len(dTheta2_flat)

plt.hist(dTheta2_flat, bins=bins, weights=weights2, alpha=0.6, label='image2.PNG (Dataset 2)', color='red', edgecolor='black')
plt.hist(dTheta1_flat, bins=bins, weights=weights1, alpha=0.6, label='image1.PNG (Dataset 1)', color='blue', edgecolor='black')

# Formatting plot matching statistics MATLAB style
plt.xlabel(r'Relative orientation $\Delta\theta$ in $^{\circ}$', fontsize=14)
plt.ylabel('Probability', fontsize=14)
plt.title('Comparison of Director Orientation Fluctuations', fontsize=16)

# Setup Y-ticks to match MATLAB custom levels if desired
plt.ylim(0, 0.1)
plt.yticks(np.arange(0, 0.1, 0.02))

# Premium styling
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_facecolor('none')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(frameon=False, fontsize=12)

plt.tight_layout()
plt.show()
