import legscrape
import numpy as np
import matplotlib.pyplot as plt

def chart_axis(bill):
    axis = []

    for key in bill.additions:
        axis.append(key)
    return axis

def ChartAdditions(bill):
    adds = []

    for add in bill.additions:
        adds.append(bill.additions[add])

    return adds

def ChartRemovals(bill):
    removes = []
    for add in bill.removals:
        removes.append(bill.removals[add])

    return removes

def draw_chart(bill, chart_pos, fig):
    ax = fig.add_subplot(chart_pos,chart_pos,1)
    adds = ChartAdditions(bill)
    ## the data
    N = 35
    menMeans = ChartAdditions(bill)
    N = len(menMeans)
    womenMeans = ChartRemovals(bill)

    ## necessary variables
    ind = np.arange(N)                # the x locations for the groups
    width = 0.35                      # the width of the bars

    ## the bars
    rects1 = ax.bar(ind, menMeans, width,
                    color='blue',
                    error_kw=dict(elinewidth=2,ecolor='red'))

    rects2 = ax.bar(ind+width, womenMeans, width,
                        color='red',
                        error_kw=dict(elinewidth=2,ecolor='blue'))

    # axes and labels
    ax.set_xlim(-width,len(ind)+width)
    ax.set_ylim(0,1.0)
    ax.set_ylabel('Percent of Change')
    ax.set_title(bill.title)
    xTickMarks = chart_axis(bill)
    ax.set_xticks(ind+width)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=20)

    ## add a legend
    ax.legend( (rects1[0], rects2[0]), ('Additions', 'Removals') )

def ManageCharts(bill):
    num = 1
    fig = plt.figure()

    for x in bill.amendments:
        for z in x:
            draw_chart(z, num, fig)
            num += 1

    plt.show()

def main():
    bill_link = raw_input("Enter leginfo link to bill: ")
    bill = legscrape.process_bill(bill_link)
    ManageCharts(bill)

if __name__ == '__main__':
    main()
