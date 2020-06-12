% covid.m
% import covid data from csv

deaths_day = covid_x(:,end);
deaths_week = filter(ones(1,7)/7,1,deaths_day);
deaths_total = covid_x(:,end-1);


fh = figure(1); clf; ah = axes; hold on; zoom on; grid on; set(gca,'Fontsize',14)
ph(1) = plot(deaths_week)
ph(2) = plot(deaths_day)
sum(deaths_day)
sum(deaths_week)

set(ph,'LineWidth',2)
xlabel('Dagar sedan man tyckte det var värt att börja räkna');
ylabel('Dödelidöda per dag');
title('Antal döda över tid');
