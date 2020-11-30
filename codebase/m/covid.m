% covid.m
% import covid data from csv

A  =  dlmread('..\..\database\covid2.csv',',',1,0);
x = A(:,1);
y = A(:,7);
p = polyfit(x,y,28);
x_n = 1:max(x);
f = polyval(p,x_n);
plot(x,y,'o',x_n,f,'-')
legend('data','linear fit')