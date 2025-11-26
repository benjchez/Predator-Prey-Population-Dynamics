data = load("data\example1.dat");

range_to = 5000;

% plot(data(:, 1), data(:, 2), 'DisplayName', 'Prey');
% hold on;
% plot(data(:, 1), data(:, 3), 'DisplayName', 'Predators');

plot(data(1: range_to, 1), data(1: range_to, 2), 'DisplayName', 'Prey');
hold on;
plot(data(1: range_to, 1), data(1: range_to, 3), 'DisplayName', 'Predators');

legend show
xlabel('Turn number');
ylabel('Population count');
hold off;