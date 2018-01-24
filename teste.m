close all;
clear all;

sam_constants;
sam_parameters;

T=1000;
disp(['Utilizando F calculado por Riccati com T=',num2str(T),' iteracoes:']);
disp('Raios espectrais:');
Fs_riccati=riccati(T,N,As,Bs,Cs,Ds,P);
stabilizes(Fs_riccati,As,Bs,P,N);
