import legscrape
import numpy as np
import matplotlib.pyplot as plt

def chart_axis(bill):
    axis = []

    for key in sorted(bill.additions):
        axis.append(key)
    return axis

def ChartAdditions(bill):
    adds = []

    for add in sorted(bill.additions):
        adds.append(bill.additions[add])

    return adds

def AmendmentAdditions(bill):
    change = 0
    num = 0
    for add in sorted(bill.additions):
        change += bill.additions[add]
        num += 1

    return change/num

def AmendmentRemovals(bill):
    change = 0
    num = 0

    for remove in sorted(bill.removals):
        change += bill.removals[remove]
        num += 1

    return change/num

def ChartRemovals(bill):
    removes = []
    for add in sorted(bill.removals):
        removes.append(bill.removals[add])

    return removes

def draw_chart(bill, chart_pos, fig, ax):

    adds = ChartAdditions(bill)
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
    plt.setp(xtickNames, rotation=45, fontsize=10)

def ManageCharts(bill):
    num = 0
    amends = 0

    for x in bill.amendments:
        for z in x:
            amends += 1

    f, axarr = plt.subplots(amends, sharey=True)

    for x in bill.amendments:
        for z in x:
            draw_chart(z, num, f, axarr[num])
            num += 1

    plt.show()

def CalculateScore(bill):
    adds = 0
    amends = 0

    for x in bill.amendments:
        for z in x:
            amends += 1

    for x in bill.amendments:
        for z in x:
            adds += AmendmentAdditions(z)
            adds += AmendmentRemovals(z)

    score = adds/amends
    print(score)

def main():
    bill_link = raw_input("Enter leginfo link to bill: ")
    bill = legscrape.process_bill(bill_link)
    #ManageCharts(bill)
    CalculateScore(bill)

if __name__ == '__main__':
    main()
