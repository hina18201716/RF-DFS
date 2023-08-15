% RF-DFS S-Parameters

% Importing data
PMA6G = sparameters('RF-DFS_6GHz.s2p');


% Graphing S-Parameters
figure(1)
tiledlayout('flow')
nexttile
rfplot(PMA6G)
grid on
title('RF-DFS Board with PMA2-63LN+')
xlabel('Frequency (GHz)')

% Output csv
writematrix([PMA6G.Frequencies/10^6, mag2db(abs(rfparam(PMA6G, 2, 1)))], 'rfdfs-6g-sparam.txt', 'Delimiter', 'tab');