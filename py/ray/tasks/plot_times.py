import matplotlib.pyplot as plt 
import pandas as pd

S_TIMES = [(10, 5.71), (20, 12.86), (30, 19.94), (40, 28.64), (50, 37.89), (60, 43.91), (70, 52.8), (80, 62.12), (90, 70.86), (100, 79.23)]
D_TIMES = [(10, 2.76), (20, 4.07), (30, 5.5), (40, 9.44), (50, 10.32), (60, 11.25), (70, 13.36), (80, 16.35), (90, 20.61), (100, 21.2)]
BATCHES = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

def extract_times(lst):
    s_times = [t[1] for t in lst]
    return s_times

if __name__ == "__main__":
    s_times = extract_times(S_TIMES)
    d_times = extract_times(D_TIMES)
    data = {'batches': BATCHES,
            'serial' : s_times,
            'distributed': d_times}
    df = pd.DataFrame(data)
    df.plot(x="batches", y=["serial", "distributed"], kind="bar")
    plt.ylabel('Times in sec', fontsize=12)
    plt.xlabel('Number of Batches of Images', fontsize=12)
    plt.grid(False)
    plt.show()