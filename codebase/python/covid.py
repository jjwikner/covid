#!/usr/bin/python3
# ---

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import argparse
import time

def close_windows(list_of_windows):
    while True:
        time.sleep(2)
        print("hej")        
        plt.close('all')

def read_data():
    """Function to read the data from a file. This could be more sophisticated and get data from the webb, etc."""
    first_row = True
    with open(f'..{os.sep}..{os.sep}database{os.sep}covid.csv','r') as csvfile:
        csv_read = csv.reader(csvfile, delimiter=',')
        for row in csv_read:
            if first_row:
                first_row = False
            else:
                #print(row)
                pass

    # Or use the numpy version. Unknown values are set to NaN
    A = np.genfromtxt(f'..{os.sep}..{os.sep}database/covid.csv',delimiter=',',skip_header=True)

    return A

def main(options):
    # p = Process(target=close_windows, args=([],))
    # p.start()
    # p.join()
    
    covid_stats = read_data()
    death_row = 6
    deaths_per_day = covid_stats[:,death_row]
    deaths_total = covid_stats[:,death_row-1]
    avg_length = 7
    deaths_avg_wk = np.convolve(deaths_per_day, np.ones(avg_length))/avg_length
    deaths_avg_biwk = np.convolve(deaths_per_day, np.ones(14))/14

    plt.figure(1)
    plt.plot(deaths_per_day,'k-.',linewidth=1)
    plt.plot(deaths_avg_wk[:-(avg_length-1)],
             'k-', linewidth=3)

    noise = np.std( deaths_per_day-deaths_avg_wk[:-(avg_length-1)] )
    power = np.sqrt((1/deaths_per_day.shape[0])*np.sum(deaths_avg_wk[:-(avg_length-1)]**2))
    print(f"Signal power: {power:2.1f} deaths,rms. \nNoise power: {noise:2.1f} deaths,rms.")
    print(f"SNR: {power/noise:2.1f}x or {20*np.log10(power/noise):2.1f} dB.")
    
    #plt.plot(225+np.arange(len(deaths_avg_wk[:-(avg_length-1)])), deaths_avg_wk[:-(avg_length-1)],
    #         'g--', linewidth=3)
    plt.grid(True)
    plt.xlim(left=0, right=30+len(deaths_avg_wk[:-(avg_length-1)]))

    plt.xlabel("Dagar sedan första sjukdomsfallet")
    plt.ylabel('Antal döda per dag')
    plt.title('Antal döda över tid')

    plt.legend(['Inrapporterade dödsfall per dag', 
                f'Medelvärdesbildat över {avg_length} dagar', 
                'Första vågen på andra vågen'])
    plt.savefig('D:\\Users\\jjwikner\\google\\bok\\elektronism\\figs\\number_of_deaths_sweden_per_day.png',dpi=300)
    

    plt.figure(2)

    dead_per_day = 21
    deaths_fake = dead_per_day*np.ones(int(np.amax(deaths_total)/dead_per_day))
    deaths_fake_total = np.arange(1,int(np.amax(deaths_total)),int(np.amax(deaths_total)/deaths_total.size))# np.cumsum(deaths_fake)
    deaths_fake = np.ones(deaths_fake_total.size)*int(np.amax(deaths_total)/deaths_total.size)    
    deaths_fake_avg_wk = np.convolve(deaths_fake, np.ones(avg_length))/avg_length

    plt.plot(deaths_total,
             avg_length*deaths_avg_wk[:-(avg_length-1)],
             'k-',
             linewidth=3)

    plt.plot(deaths_fake_total, avg_length*deaths_fake_avg_wk[:-(avg_length-1)],'k-.')

    
    deaths_fake = np.power(3,0.06545*np.arange(1+deaths_total.size))
    deaths_fake_total = np.cumsum(deaths_fake)
    deaths_fake_avg_wk = np.convolve(deaths_fake, np.ones(avg_length))/avg_length
    
    #print(deaths_fake_total.size)
    #print(deaths_fake_avg_wk.size)
    plt.plot(deaths_fake_total, avg_length*deaths_fake_avg_wk[:-(avg_length-1)],'k--')
    
    #plt.grid(True)
    plt.xlabel('Löpande totalt antal avlidna')
    plt.ylabel(f'Antal döda de senaste {avg_length} dagarna')
    plt.title('Antal döda över lång tid jämfört med kort tid')
    plt.savefig('number_of_deaths_cannon_sweden_per_day_lin.png',dpi=300)
    print(np.amax(deaths_total))
    print(deaths_total)
    plt.xlim(left=1, right=1.1*np.amax(deaths_total)) # min([np.amax(deaths_total), np.amax(deaths_fake_total)]))
    plt.ylim(bottom=1, top = 1.1*np.amax(avg_length*deaths_avg_wk))
    plt.legend(['Verkligt avlidna','Antaget konstant per dag', 'Exponentiellt tilltagande'])
    #plt.yscale('log')
    #plt.xscale('log')
    plt.savefig('D:\\Users\\jjwikner\\google\\bok\\elektronism\\figs\\number_of_deaths_cannon_sweden_per_day_log.png',dpi=300)
    plt.yscale('linear')
    plt.xscale('linear')
    
    if options.plot:
        plt.show()
    
    # p.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot some covid stuff.')
    parser.add_argument('--plot',
                        help='Plot the windows',
                        action='store_true', default=False)
    args = parser.parse_args()
    main(args)
    # try:
    # except KeyboardInterrupt:
    #     plt.close('all')


    plt.figure()
    times = np.arange(21)
    R_one = 1
    S_one = np.power(1 + R_one, times)
    plt.plot(times, S_one/1e6,'k--')
    
    times = np.arange(16)
    R_covid = 1.8
    S_covid =  np.power(1 + R_covid, times)
    plt.plot(times, S_covid/1e6,'k-')

    R_two = 2
    R_three = 3

    S_two = np.power(1 + R_two, times)
    plt.plot(times, S_two/1e6,'k--')
    
    times = np.arange(12)
    S_three = np.power(1 + R_three, times)
    plt.plot(times, S_three/1e6,'k-.')
   
    R_measel = 13
    times = np.arange(7)
    S_measels =  np.power(1 + R_measel, times)
    plt.plot(times, S_measels/1e6,'k:')

    plt.xlabel('Antalet i smittningsledet')
    plt.ylabel('Totala antalet miljoner smittade')
    plt.title('Exponentiellt ökande antalet smittade')
    plt.legend(['R=1','Covid','R=2','R=3','Mässlingen'])    
    plt.ylim(bottom=0, top=1)
    plt.xticks(np.arange(21))
    plt.savefig('D:\\Users\\jjwikner\\google\\bok\\elektronism\\figs\\tillvaxt_lin.png',dpi=300)
    plt.ylim(bottom=1e-6, top=1)
    plt.yscale('log')
    plt.savefig('tillvaxt.png',dpi=300)
    plt.xscale('log')
    plt.savefig('D:\\Users\\jjwikner\\google\\bok\\elektronism\\figs\\tillvaxt_log.png',dpi=300)
    
    plt.show()


