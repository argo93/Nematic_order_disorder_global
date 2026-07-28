% Nematic Run script
% This script sets parameters, loads the input image, runs the nematic order analysis,
% and can be used to extract local profiles of the nematic order parameter.

clearvars;
close all;
clc;

% =========================================================================
% PARAMETER DEFINITIONS
% =========================================================================

% Define the full path to the input image file
filename = fullfile('/Users/mukherjee/Documents/MATLAB/Nematic Skin/valeria/images/', 'image2.PNG'); 

% sigma: Width of the Gaussian smoothing kernel (in pixels).
% This filters out high-frequency pixel noise before computing gradients.
% For example, sigma = 3 corresponds to a kernel size that smoothes features smaller than ~3 pixels.
sigma = 3; 

% box_size: The dimension (in pixels) of the square grid boxes used for local averaging.
% The structure tensor and nematic order parameters are calculated inside each box_size x box_size region.
box_size = 64; 

% =========================================================================
% NEMATIC ORDER ANALYSIS
% =========================================================================
% S_field: Interpolated local scalar nematic order parameter field (0 = disordered, 1 = perfectly ordered)
% theta_field: Interpolated local nematic director angle field (in radians, scaled /pi)
% avg_nematic_order: Average scalar nematic order parameter over all grid boxes
% global_nematic_order: Global scalar nematic order parameter calculated across the entire image at once
% U, V: X and Y components of the local director field vectors (unit vectors)
%
% Arguments: (filename, sigma, box_size, Fancy_Visualization_Flag)
% Setting Fancy = 0 uses standard yellow quiver arrows for the director field.
[S_field, theta_field, avg_nematic_order, global_nematic_order, U, V] = analyze_nematic_order(filename, sigma, box_size, 0);

% =========================================================================
% OPTIONAL POST-PROCESSING & PROFILE EXTRACTION
% =========================================================================
% Un-comment the code below to extract and plot a 1D profile of the nematic order S
% along the x-direction, averaged across a specific horizontal band (y-region).
%
% % Plot the local interpolated nematic order parameter map
% figure;
% imagesc(S_field);
% title('Scalar Nematic Order (Interpolated)');
% colorbar;
%
% % Define the vertical (y) bounds of the band of interest (in grid box coordinates)
% y1 = 300; 
% y2 = 450;
%
% % Calculate the mean of S along the x-direction within the y1-y2 band
% Qy = mean(S_field(y1:y2, :), 1); 
%
% % Plot the 1D profile
% figure;
% plot(Qy, 'LineWidth', 1.2);
% grid on;
% xlabel('x position');
% ylabel('S (Nematic Order)');
% title('Average Nematic Order Profile');
