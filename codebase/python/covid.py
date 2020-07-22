#!/usr/bin/python3
# ---

import csv
import numpy as np
import matplotlib.pyplot as plt
import argparse
from multiprocessing import Process, Manager
import time
def close_windows(list_of_windows):
    while True:
        time.sleep(2)
        print("hej")        
        plt.close('all')

def read_data():
    """Function to read the data from a file. This could be more sophisticated and get data from the webb, etc."""
    first_row = True
    with open('database/covid.csv','r') as csvfile:
        csv_read = csv.reader(csvfile, delimiter=',')
        for row in csv_read:
            if first_row:
                first_row = False
            else:
                #print(row)
                pass

    # Or use the numpy version. Unknown values are set to NaN
    A = np.genfromtxt('database/covid.csv',delimiter=',',skip_header=True)

    return A

def main(options):
    p = Process(target=close_windows, args=([],))
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
    plt.plot(deaths_per_day,linewidth=3)
    plt.plot(deaths_avg_wk[:-(avg_length-1)],
             'r--', linewidth=3)
    plt.grid(True)

    plt.xlabel("Dagar sedan forsta sjukdomsfallet")
    plt.ylabel('Antal doda per dag')
    plt.title('Antal doda over tid')

    plt.legend(['Inrapporterade dodsfall per dag', f'Medelvardesbildat over {avg_length} dagar'])
    plt.savefig('number_of_deaths_sweden_per_day.png')
    

    plt.figure(2)

    dead_per_day = 2
    deaths_fake = dead_per_day*np.ones(int(np.amax(deaths_total)/dead_per_day))
    deaths_fake_total = np.arange(1,int(np.amax(deaths_total)),int(np.amax(deaths_total)/deaths_total.size))# np.cumsum(deaths_fake)
    deaths_fake = np.ones(deaths_fake_total.size)*int(np.amax(deaths_total)/deaths_total.size)    
    deaths_fake_avg_wk = np.convolve(deaths_fake, np.ones(avg_length))/avg_length

    plt.plot(deaths_total,
             avg_length*deaths_avg_wk[:-(avg_length-1)],
             '-',
             linewidth=3)

    plt.plot(deaths_fake_total, avg_length*deaths_fake_avg_wk[:-(avg_length-1)],'--')

    
    deaths_fake = np.power(3,0.06545*np.arange(1+deaths_total.size))
    deaths_fake_total = np.cumsum(deaths_fake)
    deaths_fake_avg_wk = np.convolve(deaths_fake, np.ones(avg_length))/avg_length
    
    print(deaths_fake_total.size)
    print(deaths_fake_avg_wk.size)
    plt.plot(deaths_fake_total, avg_length*deaths_fake_avg_wk[:-(avg_length-1)],'--')
    
    #plt.grid(True)
    plt.xlabel('Lopande totalt antal avlidna')
    plt.ylabel(f'Antal doda de senaste {avg_length} dagarna')
    plt.title('Antal doda over lang tid jamfort med kort tid')
    plt.savefig('number_of_deaths_cannon_sweden_per_day_lin.png')
    print(np.amax(deaths_total))
    print(deaths_total)
    plt.xlim(left=1, right=1.1*np.amax(deaths_total)) # min([np.amax(deaths_total), np.amax(deaths_fake_total)]))
    plt.ylim(bottom=1, top = 1.1*np.amax(avg_length*deaths_avg_wk))
    plt.legend(['Verkligt avlidna','Antaget konstant per dag', 'Exponentiellt tilltagande'])
    #plt.yscale('log')
    #plt.xscale('log')
    plt.savefig('number_of_deaths_cannon_sweden_per_day_log.png')
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
    plt.plot(times, S_one/1e6)
    
    times = np.arange(16)
    R_covid = 1.8
    S_covid =  np.power(1 + R_covid, times)
    plt.plot(times, S_covid/1e6)

    R_two = 2
    R_three = 3

    S_two = np.power(1 + R_two, times)
    plt.plot(times, S_two/1e6)
    
    times = np.arange(12)
    S_three = np.power(1 + R_three, times)
    plt.plot(times, S_three/1e6)
   
    R_measel = 13
    times = np.arange(7)
    S_measels =  np.power(1 + R_measel, times)
    plt.plot(times, S_measels/1e6)

    plt.xlabel('Antal smittningar')
    plt.ylabel('Totala antalet miljoner smittade')
    plt.title('Exponentiellt okande antalet smittade')
    plt.legend(['1','Covid','2','3','Masslingen'])    
    plt.ylim(bottom=0, top=1)
    plt.xticks(np.arange(21))
    plt.savefig('exponential_1.png')
    plt.ylim(bottom=1e-6, top=1)
    plt.yscale('log')
    plt.savefig('exponential_2.png')
    plt.xscale('log')
    plt.savefig('exponential_3.png')
    
    plt.show()


