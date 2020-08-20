import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

def calendar_heatmap(pd_series, seq_color=None, ax=None, **kwargs):
    
    days_of_week   = ['Sun.', 'Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.']
    months_of_year = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 
                      'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.']
    
    # Assign the beginning and ending dates
    beg = pd_series.index.min()
    end = pd_series.index.max()
    end += np.timedelta64(1, 'D')

    # Pandas and numpy day-of-week conventions are Monday=0 and Sunday=6.
    beg_sun = beg - np.timedelta64((beg.dayofweek + 1) % 7, 'D')
    end_sun = end + np.timedelta64(7 - end.dayofweek - 1, 'D')

    # Create the heatmap and track ticks.
    weeks = (end_sun - beg_sun).days // 7
    heatmap = np.zeros((7, weeks))
    ticks = {} 
    for week in range(weeks):
        for day in range(7):
            date = beg_sun + np.timedelta64(7 * week + day, 'D')
            if date.day == 1:
                ticks[week] = months_of_year[date.month - 1]
            if date.dayofyear == 1:
                ticks[week] += f'\n{date.year}'
            if beg <= date < end:
                heatmap[day, week] = pd_series.get(date, 0)

    # Get the coordinates, offset by 0.5 to align the ticks.
    y = np.arange(8) - 0.5
    x = np.arange(weeks + 1) - 0.5

    # Plot the heatmap. 
    plt.gcf().set_size_inches(18, 3)
    ax = ax or plt.gca()
    mesh = ax.pcolormesh(x, y, heatmap, cmap=plt.get_cmap(seq_color), **kwargs)
    ax.invert_yaxis()
    
    # Set the ticks.
    ax.set_xticks(list(ticks.keys()))
    ax.set_xticklabels(list(ticks.values()))
    ax.set_yticks(np.arange(7))
    ax.set_yticklabels(days_of_week)

    # Set the current image and axes in the pyplot API.
    plt.sca(ax)
    plt.sci(mesh)

    return ax