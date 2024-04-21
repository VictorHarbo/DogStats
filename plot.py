import matplotlib.pyplot as plt
import datetime

from matplotlib.ticker import MaxNLocator
from plotting.functions import seven_days_of_steps, runs_per_week, plank_minuts_pr_week

# Color for a fourth plot, which fits the scheme: #FDFFAB (https://colorhunt.co/palette/d9edbfffb996ffcf81fdffab)

def define_plot(plot_index, xvalues, yvalues, hex_color, title, xlabel, ylabel):
    axs[plot_index].bar(xvalues, yvalues, color=hex_color)
    axs[plot_index].set_title(title)
    axs[plot_index].set_xlabel(xlabel)
    axs[plot_index].set_ylabel(ylabel)

# Create a figure and subplots
fig, axs = plt.subplots(1, 3, figsize=(20, 5))  # 1 row, 3 columns

# Create first plot
dictionary_of_steps = seven_days_of_steps()

define_plot(0, dictionary_of_steps.keys(), dictionary_of_steps.values(), '#D9EDBF',
            'Skridt de sidste 7 dage', 'Dato', 'Skridt')
axs[0].tick_params(axis='x', rotation=45)
axs[0].set_xticklabels([s[5:] for s in  dictionary_of_steps.keys()])

# Add the mean  of values from the first plot to the plot as a text entry.
sum_values = sum(dictionary_of_steps.values())
average = int(sum_values / len(dictionary_of_steps))
axs[0].text(5 , 14000, f'Gennemsnit: {average:.0f}', ha='center', va='bottom', fontsize=12, color='black')

# Create second plot
runs_df = runs_per_week()

define_plot(1, runs_df["week"], runs_df["count"], '#FFB996', 
            'Løbeturer pr. uge', 'Uge', 'Antal løbeture')
axs[1].yaxis.set_major_locator(MaxNLocator(integer=True))
axs[1].xaxis.set_major_locator(MaxNLocator(integer=True))
axs[1].set_xlim(14, datetime.date.today().isocalendar()[1])

# Create third plot
planks = plank_minuts_pr_week()
dates = list(planks.keys())
durations = [value.total_seconds() / 60 for value in planks.values()]

define_plot(2, dates, durations, '#FFCF81', 'Minutters planke pr. uge', 
            'Uge', 'Minutters planke')
axs[2].xaxis.set_major_locator(MaxNLocator(integer=True))
axs[2].set_xlim(14, datetime.date.today().isocalendar()[1])

# Adjust layout and display plot
plt.tight_layout()
plt.subplots_adjust(wspace=0.25)

# Get current date
current_date = datetime.datetime.now()
# Format the date as "YYYYMMDD"
formatted_date = current_date.strftime("%Y%m%d")

plt.savefig('/Users/vhol/DogStats/grafs/' + formatted_date + '_graf.jpg')  # Save as JPG
plt.show()