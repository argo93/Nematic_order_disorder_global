import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
from PIL import Image
import os

def analyze_nematic_order(filename, sigma, box_size, fancy=0):
    """
    Analyzes orientational order and director fields from image texture.
    
    Parameters:
    -----------
    filename : str
        Path to the image file.
    sigma : float
        Standard deviation of the Gaussian blur kernel (in pixels).
    box_size : int
        Size of square grid boxes for local spatial averaging (in pixels).
    fancy : int (0 or 1)
        If 1, uses a styled thick representation for the director lines.
        
    Returns:
    --------
    S_field : ndarray
        Interpolated local scalar nematic order parameter field (2D).
    theta_field : ndarray
        Interpolated local director angle field in radians, scaled by 1/pi (2D).
    avg_nematic_order : float
        Average scalar nematic order parameter over all boxes.
    global_nematic_order : float
        Global scalar nematic order parameter across the entire image.
    U : ndarray
        X components of local director field vectors.
    V : ndarray
        Y components of local director field vectors.
    """
    # -------------------------------------------------------------------------
    # 1. Image Pre-processing
    # -------------------------------------------------------------------------
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Image file not found: {filename}")
        
    img_pil = Image.open(filename)
    # Convert to grayscale if RGB
    if img_pil.mode in ("RGB", "RGBA"):
        img_pil = img_pil.convert("L")
    img = np.array(img_pil, dtype=float)
    
    # Scale image intensities to [0, 1] to match MATLAB's im2double
    img = img / 255.0
    
    # -------------------------------------------------------------------------
    # 2. Image Smoothing
    # -------------------------------------------------------------------------
    # Apply 2D Gaussian blur. Mode 'nearest' behaves closely to MATLAB's padding.
    blurred_img = ndimage.gaussian_filter(img, sigma, mode='nearest')
    
    # -------------------------------------------------------------------------
    # 3. Gradient Computation
    # -------------------------------------------------------------------------
    # NumPy gradient along axis 0 (y) and axis 1 (x)
    # Note: np.gradient returns (grad_y, grad_x) for a 2D array.
    Iy, Ix = np.gradient(blurred_img)
    
    height, width = blurred_img.shape
    
    # -------------------------------------------------------------------------
    # 4. Box-wise Structure Tensor Calculations
    # -------------------------------------------------------------------------
    num_boxes_x = width // box_size
    num_boxes_y = height // box_size
    
    c2_all = np.zeros((num_boxes_y, num_boxes_x))
    s2_all = np.zeros((num_boxes_y, num_boxes_x))
    
    for i in range(num_boxes_y):
        for j in range(num_boxes_x):
            # Define box boundaries (0-indexed, exclusive upper bounds)
            row_start = i * box_size
            row_end = (i + 1) * box_size
            col_start = j * box_size
            col_end = (j + 1) * box_size
            
            # Extract gradients for the current box
            Ix_box = Ix[row_start:row_end, col_start:col_end]
            Iy_box = Iy[row_start:row_end, col_start:col_end]
            
            # Compute local structure tensor components
            J11 = np.mean(Ix_box**2)
            J12 = np.mean(Ix_box * Iy_box)
            J22 = np.mean(Iy_box**2)
            traceJ = J11 + J22
            
            if traceJ < 1e-10:
                c2 = 0.0
                s2 = 0.0
            else:
                # Normalize and compute nematic components
                c2 = (J11 - J22) / traceJ
                s2 = (2.0 * J12) / traceJ
                
            c2_all[i, j] = c2
            s2_all[i, j] = s2
            
    # -------------------------------------------------------------------------
    # 5. Scalar Nematic Order Parameter
    # -------------------------------------------------------------------------
    c2_avg = np.mean(c2_all)
    s2_avg = np.mean(s2_all)
    avg_nematic_order = np.sqrt(c2_avg**2 + s2_avg**2)
    
    # -------------------------------------------------------------------------
    # 6. Global Nematic Order Parameter (Entire Image)
    # -------------------------------------------------------------------------
    J11_global = np.mean(Ix**2)
    J12_global = np.mean(Ix * Iy)
    J22_global = np.mean(Iy**2)
    traceJ_global = J11_global + J22_global
    
    if traceJ_global < 1e-10:
        global_nematic_order = 0.0
    else:
        c2_global = (J11_global - J22_global) / traceJ_global
        s2_global = (2.0 * J12_global) / traceJ_global
        global_nematic_order = np.sqrt(c2_global**2 + s2_global**2)
        
    print(f"Average Nematic Order (box-wise): {avg_nematic_order:.4f}")
    print(f"Global Nematic Order: {global_nematic_order:.4f}")
    
    # -------------------------------------------------------------------------
    # 7. Field Interpolation & Visualization
    # -------------------------------------------------------------------------
    S_box = np.sqrt(c2_all**2 + s2_all**2)
    theta_box = 0.5 * np.arctan2(s2_all, c2_all)
    
    # Refine grid by factor of 16 (zoom = 2^4 = 16) to match MATLAB's interp2(..., 4)
    # order=1 specifies bilinear interpolation
    S_field = ndimage.zoom(S_box, 16, order=1)
    theta_field = ndimage.zoom(theta_box / np.pi, 16, order=1)
    
    # Plot 1: Angle of the Nematic Director (sin(2*theta))
    plt.figure(figsize=(6, 5))
    plt.imshow(np.sin(theta_field * 2.0 * np.pi), cmap='twilight', aspect='equal')
    plt.colorbar(label=r'$\sin(2\theta)$')
    plt.title('Angle of the Nematic Director')
    plt.axis('image')
    plt.tight_layout()
    plt.show(block=False)
    
    # -------------------------------------------------------------------------
    # 8. Director Overlay (Quiver Plot)
    # -------------------------------------------------------------------------
    # Create coordinate meshgrid for box centers
    x = (np.arange(num_boxes_x) + 0.5) * box_size
    y = (np.arange(num_boxes_y) + 0.5) * box_size
    X, Y = np.meshgrid(x, y)
    
    # Directors are perpendicular to gradients (texture orientation = gradient angle + pi/2)
    U = np.cos(theta_box + np.pi / 2.0)
    V = np.sin(theta_box + np.pi / 2.0)
    
    # Plot 2: Subplots showing Director Overlay and Grayscale Angle Field
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    # Left subplot: Grayscale image with director overlay
    axes[0].imshow(img, cmap='gray', aspect='equal')
    
    # Set styling based on fancy parameter
    if fancy == 1:
        # Styled representation with dot markers and thicker lines
        # Matplotlib quiver uses cartesian angles by default. We specify angles='xy', scale_units='xy'
        # scale=0.03 fits the length visually
        axes[0].quiver(X, Y, U, V, angles='xy', scale_units='xy', scale=0.03,
                       color='yellow', width=0.005, headwidth=0, headlength=0, 
                       headaxislength=0, pivot='middle')
        axes[0].scatter(X, Y, color='yellow', s=10, zorder=3)
    else:
        # Standard yellow lines
        axes[0].quiver(X, Y, U, V, angles='xy', scale_units='xy', scale=0.02,
                       color='yellow', width=0.003, headwidth=0, headlength=0, 
                       headaxislength=0, pivot='middle')
                       
    axes[0].set_title('Director Field Overlay')
    axes[0].axis('image')
    
    # Right subplot: Grayscale representation of the angle field
    im2 = axes[1].imshow(np.sin(theta_field * 2.0 * np.pi), cmap='gray', aspect='equal')
    axes[1].set_title('Angle of the Nematic Director')
    axes[1].axis('image')
    
    plt.tight_layout()
    plt.show()
    
    return S_field, theta_field, avg_nematic_order, global_nematic_order, U, V
