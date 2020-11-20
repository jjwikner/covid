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

def read_data(database='../../database/befolkning.csv'):
    """Function to read the data from a file. This could be more sophisticated and get data from the webb, etc."""
    first_row = True
    with open(database,'r') as csvfile:
        csv_read = csv.reader(csvfile, delimiter=';')
        for row in csv_read:
            if first_row:
                first_row = False
            else:
                #print(row)
                pass

    # Or use the numpy version. Unknown values are set to NaN
    A = np.genfromtxt(database,delimiter=';',skip_header=True)

    return A

def main(options):

    folk_stats = read_data()
    year = folk_stats[:,0]
    plt.figure(1)
    plt.plot(year, folk_stats[:,1:],'-x')
    plt.grid(True)
    plt.xlabel('År')
    plt.ylabel('Antal människor på jorden')
    plt.title('Befolkningsutveckling')

    #plt.plot(year, 
    plt.yscale('log')
    plt.xscale('linear')
    #plt.savefig('befolkning.png')
    
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
