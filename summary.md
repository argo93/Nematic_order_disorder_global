# Nematic Texture Analysis: Executive Summary

This document summarizes the results obtained from running the orientational order and disorder analysis on the skin texture images.

---

## 📂 Project Directory Structure

```text
valeria/
├── images/                        # Raw input images
│   ├── image1.PNG                 # Highly aligned skin texture
│   └── image2.PNG                 # Disordered skin texture
├── python/                        # Translated Python environment
│   ├── analyze_nematic_order.py   # Core analysis module
│   ├── nematic_run.py             # Single-image runner (image2.PNG)
│   ├── statistics.py              # Stats comparison script
│   ├── nematic_batch_run.py       # Batch processing script
│   └── requirements.txt           # Python library dependencies
├── batch_results/                 # Outputs from MATLAB batch run
│   ├── nematic_summary.csv        # MATLAB statistics report
│   ├── comparative_histograms.png # Comparative fluctuation histogram plot
│   └── [image]_overlay.png etc.   # Visualization plots
├── batch_results_python/          # Outputs from Python batch run
│   ├── nematic_summary.csv        # Python statistics report
│   ├── comparative_histograms.png # Comparative fluctuation histogram plot
│   └── [image]_overlay.png etc.   # Visualization plots
├── analyze_nematic_order.m        # Core MATLAB analysis function
├── nematicRun.m                   # Single-image MATLAB runner
├── statistics.m                   # Stats MATLAB script
├── nematicBatchRun.m              # Batch MATLAB script
├── README.md                      # Detailed beginners guide
└── summary.md                     # This summary file
```

---

## 📈 Quantitative Results

The analysis was performed with parameters: Standard deviation of blur ($\sigma = 3$) and local averaging box size ($box\_size = 64$ pixels).

| Metric | Image 1: `image1.PNG` (Aligned) | Image 2: `image2.PNG` (Disordered) | Explanation |
| :--- | :---: | :---: | :--- |
| **Average Local Order ($S$)** | **`0.7356`** | **`0.2567`** | Local alignment inside grid boxes (0 = random, 1 = uniform). |
| **Global Order ($S_{\text{global}}$)** | **`0.8774`** | **`0.2127`** | Overall alignment across the entire image. |
| **Orientation Variance ($\text{Var}(\Delta\theta}$)** | **`93.9997 deg²`** | **`784.3698 deg²`** | Fluctuations of local directors. Lower variance = higher alignment. |

*Note: The values above are from the Python execution. MATLAB values match these within a tiny numerical tolerance ($< 0.2\%$) due to minor differences in grayscale weighting and Gaussian blur truncation.*

---

## 🔍 Key Findings

1. **Quantifying Order**:
   - `image1.PNG` shows high local and global order ($S \approx 0.74$, $S_{\text{global}} \approx 0.88$). The textures are mostly parallel.
   - `image2.PNG` shows very low order ($S \approx 0.26$, $S_{\text{global}} \approx 0.21$). The textures are random and isotropic.
2. **Quantifying Disorder**:
   - The angular fluctuations (deviations of local director angles from the mean) are highly concentrated near $0^\circ$ for `image1.PNG` (variance $\approx 94\text{ deg}^2$).
   - For `image2.PNG`, the fluctuations are very wide and spread out (variance $\approx 784\text{ deg}^2$), reflecting high structural disorder.

---

## 🛠️ Discovered and Corrected Bugs
- **MATLAB Fluctuation Variance Bug**: The original `valeria.m` (now `statistics.m`) script divided local angles by $\pi$ twice before calculating variance, causing the printed variance to be off by a factor of $\pi^2 \approx 9.87$. The corrected variance is implemented in both [nematicBatchRun.m](file:///Users/mukherjee/Documents/MATLAB/Nematic%20Skin/valeria/nematicBatchRun.m) and [python/statistics.py](file:///Users/mukherjee/Documents/MATLAB/Nematic%20Skin/valeria/python/statistics.py).
