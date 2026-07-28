
# Nematic Orientational Order and Texture Analysis

This repository contains tools for calculating **nematic orientational order** and **average texture disorder** directly from images. It uses a gradient-based **Structure Tensor** approach to identify alignment, draw director fields, and analyze angular fluctuations.

Originally written in MATLAB, this repository now includes both commented MATLAB scripts and a complete Python translation, along with batch-processing scripts for both environments.

---

## 📖 Theoretical Background

### What is Nematic Order?
In physics, **nematic liquid crystals** are states of matter where molecules have no long-range positional order, but possess a common orientational order along a specific direction, called the **director**. 
When analyzing image textures (such as fibers, biological tissues, or skin wrinkles):
- **Alignment (Order)**: The texture features (lines/wrinkles) run parallel to each other.
- **Disorder (Isotropy)**: The texture features are oriented randomly in all directions.

### The Structure Tensor (Gradient-based)
To quantify local orientation, we compute the local image gradients (how pixel brightness changes):
1. **Gradients ($I_x, I_y$)**: Represent the direction of maximum intensity change. The gradient vector is **perpendicular** to the texture edge/fiber.
2. **Structure Tensor ($J$)**: Inside a local region (grid box), we compute the average of outer products of the gradients:
   $$J = \begin{bmatrix} \langle I_x^2 \rangle & \langle I_x I_y \rangle \\ \langle I_x I_y \rangle & \langle I_y^2 \rangle \end{bmatrix} = \begin{bmatrix} J_{11} & J_{12} \\ J_{12} & J_{22} \end{bmatrix}$$
   where $\langle \cdot \rangle$ denotes the spatial average over all pixels in the box.

### Nematic Order Parameters
From the structure tensor, we extract:
- **Nematic Director Angle ($\theta$)**: The local orientation of the texture. Since gradients are perpendicular to the texture lines, we shift the gradient orientation by $90^\circ$ ($\pi/2$ radians):
  $$\theta_{\text{gradient}} = \frac{1}{2} \text{atan2}(2J_{12}, J_{11} - J_{22})$$
  $$\theta_{\text{texture}} = \theta_{\text{gradient}} + \frac{\pi}{2}$$
- **Scalar Order Parameter ($S$)**: A value between $0$ (completely disordered/isotropic) and $1$ (perfectly aligned). In 2D, this is calculated as:
  $$S = \sqrt{c_2^2 + s_2^2}$$
  where:
  $$c_2 = \frac{J_{11} - J_{22}}{J_{11} + J_{22}}, \quad s_2 = \frac{2J_{12}}{J_{11} + J_{22}}$$

---

## 🛠️ Key Parameters

When running the analysis, you configure two critical parameters:
1. **Gaussian Smoothing Scale ($\sigma$)**:
   - Reduces pixel-level noise (e.g. sensor noise).
   - Higher values smooth out fine details, focusing on larger-scale structures.
   - Typical values: `1` to `5`.
2. **Grid Box Size (`box_size`)**:
   - The size (in pixels) of the square boxes used for local averaging.
   - A smaller box size gives high-resolution local director fields, but is more sensitive to local noise.
   - A larger box size averages out fluctuations, giving a smoother global representation.
   - Typical values: `32`, `64`, or `128` pixels.

---

## 💻 MATLAB Code Guide

The folder contains four MATLAB scripts:

1. **`analyze_nematic_order.m`**:
   - *Purpose*: The core analysis function.
   - *What it does*: Loads the image, converts to grayscale, applies a Gaussian blur, computes gradients, runs the box-wise structure tensor calculations, interpolates the field for smooth visualization, and plots the director overlay.
   - *Usage*: `[S_field, theta_field, avg_S, global_S, U, V] = analyze_nematic_order(filename, sigma, box_size, Fancy)`

2. **`nematicRun.m`**:
   - *Purpose*: Main execution wrapper script.
   - *What it does*: Sets parameters (`sigma`, `box_size`), defines the input file path, and executes `analyze_nematic_order`. Also includes commented templates for extracting 1D profiles.

3. **`statistics.m`**:
   - *Purpose*: Statistical analysis of orientation fluctuations.
   - *What it does*: Takes orientation angles from different runs (`theta1`, `theta2`), calculates their variance (which measures the degree of angular disorder), and plots a comparative probability distribution histogram.

4. **`nematicBatchRun.m`**:
   - *Purpose*: Automate analysis over multiple images.
   - *What it does*: Scans the folder for all `.png`/`.PNG` images (e.g., `image1.PNG` and `image2.PNG`), processes each image to save its director overlays, angle maps, and individual fluctuation histograms. It then aggregates their results, saves a comparative overlay plot, and writes a CSV report (`nematic_summary.csv`) under a new `batch_results/` folder.

---

## 🐍 Python Code Guide

A translated Python version is available in the `python/` subfolder.

### Setup and Requirements
Make sure you have Python 3.8+ installed. Navigate to the `python` directory and set up a virtual environment:

```bash
# Navigate to the python subfolder
cd python

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

# Install required packages
pip install -r requirements.txt
```

### Running the Python Scripts
1. **Run the Nematic Analysis**:
   ```bash
   python nematic_run.py
   ```
   This script loads the image (`image2.PNG`), computes the nematic order fields, prints the average & global order parameter values, and displays the director overlay plots.

2. **Run the Statistical Comparison**:
   ```bash
   python statistics.py
   ```
   This script executes a comparison between different orientation profiles (from `image1.PNG` and `image2.PNG`), calculates their angular variance, and plots their comparative probability histograms.

3. **Run Batch Processing**:
   ```bash
   python nematic_batch_run.py
   ```
   This script processes all images in the parent directory, saving director overlays, angle maps, histograms, a comparative stairs histogram plot, and a `nematic_summary.csv` file under a new `batch_results_python/` folder. It runs in headless mode, making it fast and robust.

---

## 📊 Interpreting Visualizations

- **Director Field Overlay**: Shows the input image overlaid with yellow lines representing the local orientation of the texture. If lines are aligned together, the texture has high nematic order.
- **Angle of the Nematic Director ($\sin(2\theta)$)**: Displays a spatial heat map of the orientation. The $\sin(2\theta)$ projection ensures that angles wrapping around (e.g. $-90^\circ$ and $+90^\circ$) represent the same value, matching the nematic symmetry.
- **Angle Fluctuation Histograms**: A narrower peak centered at $0^\circ$ signifies highly aligned texture. A wider, flatter histogram signifies high angular disorder (large variance).



## GNU General Public License v3.0 (GNU GPLv3)
Copyright (c) 2026
This program is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
