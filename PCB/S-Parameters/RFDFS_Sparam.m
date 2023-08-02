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
xlabel('Frequency (MHz)')