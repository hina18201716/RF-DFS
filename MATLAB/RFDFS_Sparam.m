% RF-DFS S-Parameters
clear
clc
close all

% Importing data
RevA_6G = sparameters('RF-DFS-RevA-6G.s2p');
RevC_6G = sparameters('RF-DFS-RevC-6G.s2p');
RevC_12G = sparameters('RF-DFS-RevC-12G.s2p');
PMA6G_MC_WEB = sparameters('PMA2-63LN+_5.00V_42mA_Plus25DegC_Unit1.s2p');


% Graphing S-Parameters
figure(1)
rfplot(RevA_6G)
grid on
title('RF-DFS Rev A with PMA2-63LN+')
xlabel('Frequency (GHz)')

figure(2)
rfplot(PMA6G_MC_WEB)
grid on
title('PMA2-63LN+ Evaluation Test Board')
xlabel('Frequency (GHz)')

figure(3)
rfplot(RevC_6G)
grid on
title('RF-DFS Rev C with PMA2-63LN+')
xlabel('Frequency (GHz)')

figure(4)
rfplot(RevC_12G)
grid on
title('RF-DFS Rev C with PMA2-123LN+')
xlabel('Frequency (GHz)')

% Output csv
writematrix([RevC_6G.Frequencies/10^6, mag2db(abs(rfparam(RevC_6G, 2, 1))), mag2db(abs(rfparam(RevC_6G, 1, 1)))], 'RevC-6G.txt', 'Delimiter', 'tab');
writematrix([RevC_12G.Frequencies/10^6, mag2db(abs(rfparam(RevC_12G, 2, 1))), mag2db(abs(rfparam(RevC_12G, 1, 1)))], 'RevC-12G.txt', 'Delimiter', 'tab');