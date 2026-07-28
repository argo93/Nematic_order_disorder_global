function [S_field, theta_field, avg_nematic_order, global_nematic_order, U, V] = analyze_nematic_order(filename, sigma, box_size, Fancy, Filter)
    % ANALYZE_NEMATIC_ORDER Analyzes orientational order and director fields from image texture.
    %
    % This function calculates local and global nematic order parameters using 
    % the Structure Tensor (or gradient-based coherence tensor) computed from the image.
    %
    % INPUTS:
    %   filename             - Path to the image file (e.g. PNG/JPG)
    %   sigma                - Standard deviation of the Gaussian blur kernel (reduces pixel noise)
    %   box_size             - Width of square grid boxes for local spatial averaging (pixels)
    %   Fancy                - Visualization flag (1 for styled thicker arrows, 0 for simple quiver)
    %   Filter               - Optional input (not active in current implementation)
    %
    % OUTPUTS:
    %   S_field              - 2D grid of interpolated local nematic order (scalar, 0 to 1)
    %   theta_field          - 2D grid of interpolated local director angles (scaled by /pi)
    %   avg_nematic_order    - Average nematic order across all grid boxes
    %   global_nematic_order - Nematic order computed across the entire image at once
    %   U, V                 - X and Y components of the local nematic director (unit vectors)

    % ---------------------------------------------------------------------
    % 1. Image Pre-processing
    % ---------------------------------------------------------------------
    % Read the image from disk
    img = imread(filename);
    
    % Convert to grayscale if it is an RGB color image (3 channels)
    if size(img, 3) == 3
        img = rgb2gray(img);
    end
    
    % Convert image representation to double precision in the range [0, 1]
    img = im2double(img);

    % ---------------------------------------------------------------------
    % 2. Image Smoothing
    % ---------------------------------------------------------------------
    % Apply a Gaussian low-pass filter to smooth the image. This suppresses
    % high-frequency noise (e.g., sensor noise, pixel-level fluctuations) 
    % and helps focus the gradient computation on relevant texture features.
    blurred_img = imgaussfilt(img, sigma);

    % ---------------------------------------------------------------------
    % 3. Gradient Computation
    % ---------------------------------------------------------------------
    % Calculate local gradients (partial derivatives along x and y) using
    % central differences. Gradients point in the direction of greatest
    % intensity change (perpendicular to texture lines/strips).
    [Ix, Iy] = gradient(blurred_img);

    % Get the size of the smoothed image
    [height, width] = size(blurred_img);

    % ---------------------------------------------------------------------
    % 4. Box-wise Structure Tensor Calculations
    % ---------------------------------------------------------------------
    % Divide the image into a grid of square boxes of size `box_size x box_size`.
    % We compute local texture properties in each grid cell.
    num_boxes_x = floor(width / box_size);
    num_boxes_y = floor(height / box_size);
    
    % Pre-allocate arrays for the nematic tensor components:
    % In 2D, the nematic order tensor Q is represented as:
    % Q = S * [cos(2*theta), sin(2*theta); sin(2*theta), -cos(2*theta)]
    % Let:
    %   c2 = S * cos(2*theta)
    %   s2 = S * sin(2*theta)
    % These elements capture the orientational features of the local structure.
    c2_all = zeros(num_boxes_y, num_boxes_x);
    s2_all = zeros(num_boxes_y, num_boxes_x);

    % Loop through each grid box
    for i = 1:num_boxes_y
        for j = 1:num_boxes_x
            % Define the boundary coordinates of the current box
            row_start = (i-1)*box_size + 1;
            row_end = i*box_size;
            col_start = (j-1)*box_size + 1;
            col_end = j*box_size;
            
            % Extract the gradients (Ix, Iy) for the pixels inside the current box
            Ix_box = Ix(row_start:row_end, col_start:col_end);
            Iy_box = Iy(row_start:row_end, col_start:col_end);
            
            % Compute the elements of the Local Structure Tensor (J):
            % J = [ J11, J12; 
            %       J12, J22 ]
            % where:
            %   J11 = <Ix^2>
            %   J12 = <Ix * Iy>
            %   J22 = <Iy^2>
            % and <.> denotes spatial averaging over the box.
            J11 = mean2(Ix_box.^2);
            J12 = mean2(Ix_box .* Iy_box);
            J22 = mean2(Iy_box.^2);
            
            % Trace of the structure tensor represents the total gradient energy
            traceJ = J11 + J22;
            
            % Handle homogeneous regions where gradients are negligible (e.g., flat background)
            if traceJ < 1e-10
                c2 = 0;
                s2 = 0;
            else
                % Normalize structure tensor elements to extract pure orientation.
                % The primary orientation of the texture gradient is related to the
                % difference in eigenvalues.
                % c2 = cos(2*phi_grad) and s2 = sin(2*phi_grad)
                c2 = (J11 - J22) / traceJ;
                s2 = (2 * J12) / traceJ;
            end
            
            % Store the computed nematic components for the current box
            c2_all(i, j) = c2;
            s2_all(i, j) = s2;
        end
    end

    % ---------------------------------------------------------------------
    % 5. Scalar Nematic Order Parameter
    % ---------------------------------------------------------------------
    % Calculate the average nematic components over all grid boxes
    c2_avg = mean(c2_all(:));
    s2_avg = mean(s2_all(:));
    
    % avg_nematic_order (S_average): Quantifies how aligned the local directors
    % are with each other across the entire sample. Ranges from 0 (disordered,
    % isotropic) to 1 (perfectly aligned, single uniform direction).
    avg_nematic_order = sqrt(c2_avg^2 + s2_avg^2);
    
    % ---------------------------------------------------------------------
    % 6. Global Nematic Order Parameter (Entire Image)
    % ---------------------------------------------------------------------
    % Instead of analyzing box-wise, compute a single structure tensor for
    % the entire image gradients.
    J11_global = mean2(Ix.^2);
    J12_global = mean2(Ix .* Iy);
    J22_global = mean2(Iy.^2);
    traceJ_global = J11_global + J22_global;
    
    if traceJ_global < 1e-10
        global_nematic_order = 0;
    else
        c2_global = (J11_global - J22_global) / traceJ_global;
        s2_global = (2 * J12_global) / traceJ_global;
        global_nematic_order = sqrt(c2_global^2 + s2_global^2);
    end
    
    % Display numerical results in the command window
    fprintf('Average Nematic Order (box-wise): %.4f\n', avg_nematic_order);
    fprintf('Global Nematic Order: %.4f\n', global_nematic_order);
    
    % ---------------------------------------------------------------------
    % 7. Field Interpolation & Visualization
    % ---------------------------------------------------------------------
    % S_box: The local scalar order parameter (anisotropy) in each box.
    % It quantifies the degree of local alignment inside the box.
    S_box = sqrt(c2_all.^2 + s2_all.^2);
    
    % theta_box: The local orientation of the gradient. 
    % We multiply by 0.5 because nematic symmetry has a period of 180 degrees (pi).
    theta_box = 0.5 * atan2(s2_all, c2_all);
    
    % Interpolate the fields to create a higher-resolution visual representation.
    % interp2(..., 4) refines the grid 4 times using bilinear interpolation.
    S_field = interp2(S_box, 4);
    theta_field = interp2((theta_box)/pi, 4);

    % Plot the local orientation angle map (sin(2*theta_field))
    % The sine function projects the angle into a smooth, periodic representation.
    figure;
    imagesc(sin(theta_field*2)); 
    colormap(twilight); % Cyclic colormap (useful for wrapping angles)
    colorbar;
    title('Angle of the Nematic Director (sin(2\theta))');
    axis image;
    
    % ---------------------------------------------------------------------
    % 8. Director Overlay (Quiver Plot)
    % ---------------------------------------------------------------------
    % Compute coordinates for the center of each box
    [X, Y] = meshgrid(1:num_boxes_x, 1:num_boxes_y);
    
    % The gradients are perpendicular to the texture lines (director).
    % To obtain the director field (tangent to the skin lines/fibers), we add pi/2 (90 degrees).
    U = cos(theta_box + pi/2);
    V = sin(theta_box + pi/2);
    
    % Plot 1: Image overlaid with Director Field
    figure;
    subplot(1,2,1);
    imagesc(img);
    colormap gray;
    hold on;
    
    % Draw lines (directors) using quiver without arrowheads
    if Fancy == 1
        % Heavy, highly-visible line style
        quiver(X * box_size - box_size/2, Y * box_size - box_size/2, U, V, 0.7, ...
               'Alignment', 'center', 'ShowArrowHead', 'off', 'Marker', 'o', ...
               'LineWidth', 2, 'Color', [1 1 0], 'AutoScaleFactor', 0.7);
    else
        % Standard yellow line style
        quiver(X * box_size - box_size/2, Y * box_size - box_size/2, U, V, 0.7, ...
               'y', 'Alignment', 'center', 'ShowArrowHead', 'off', 'LineWidth', 1.2);
    end
    title('Director Field Overlay');
    axis image;
    hold off;
    
    % Plot 2: Nematic angle map beside it (in grayscale for comparison)
    subplot(1,2,2);
    imagesc(sin(theta_field*2)); 
    colormap gray;
    title('Angle of the Nematic Director');
    axis image;
end
