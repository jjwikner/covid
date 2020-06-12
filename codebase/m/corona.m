x = 2020
y = [50]
err = y
figure(1); clf; ah = axes; hold on; zoom on; grid on; 
ph = plot(x,y,'x');
set(ph,'Linewidth',12);
eh = errorbar(x,y,err);
set(eh,'linewidth',3);
xlabel('Year');
ylabel('Percentage of population who died')
title('Covid19-inflicted deaths as function of time');
set(gca,'Xtick',[2019 2020 2021]);
xlim([2018.5 2021.5])
ylim([-5 105])
set(gca,'Ytick',0:25:100)
set(gca,'FontSize',12);
print('covid19.png','-dpng');