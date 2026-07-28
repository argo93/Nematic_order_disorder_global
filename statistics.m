% Statistics - Statistical Analysis of Director Orientations
% This script computes the fluctuations of director angles (theta1, theta2)
% around their respective mean angles, calculates their variances, 
% and plots their probability distributions (histograms) for comparison.
%
% Note: This script assumes that 'theta1' and 'theta2' variables are already
% loaded in the workspace (for example, from analyzing two different images 
% or two different regions/parameters).

% 1. Calculate the deviation (fluctuation) of each angle from the global mean,
% and convert the resulting values from radians to degrees (* 180 / pi).
dTheta1 = (theta1 - mean(theta1, "all")) * 180 / pi;
dTheta2 = (theta2 - mean(theta2, "all")) * 180 / pi;

% 2. Calculate the variance of these angular fluctuations across all grid points.
% A larger variance indicates a higher degree of local disorder or misalignment.
varTheta1 = var(dTheta1, [], 'all');
varTheta2 = var(dTheta2, [], 'all');

% Print the calculated variances to the command window
fprintf('Variance of Theta 1 (deg^2): %.4f\n', varTheta1);
fprintf('Variance of Theta 2 (deg^2): %.4f\n', varTheta2);

% 3. Create a comparison histogram showing the probability distributions of
% the relative orientations.
figure;

% Plot distribution for Dataset 2 (typically representing a more disordered skin state)
histogram(dTheta2, 'Normalization', 'probability'); 
hold on;

% Plot distribution for Dataset 1 (typically representing a more aligned skin state)
histogram(dTheta1, 'Normalization', 'probability');

% Format the axes and labels using LaTeX formatting for high-quality figures
xlabel('Relative orientation $\Delta\theta$ in $^{\circ}$', 'Interpreter', 'latex');
ylabel('Probability', 'Interpreter', 'latex');

% Set custom ticks on the Y-axis for clarity
yticks(0:0.02:0.08);

% Apply premium styling: Arial font, larger text, thick lines, box off, transparent background
set(gca, 'FontName', 'Arial', 'FontSize', 18, 'LineWidth', 1.5, 'Box', 'off', 'Color', 'none');

% Add legend
legend({'Dataset 2', 'Dataset 1'}, 'Box', 'off', 'Location', 'northeast');
hold off;
