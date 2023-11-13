import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date")

# Clean data
df = df[(df.value >= df.value.quantile(0.025)) &
        (df.value <= df.value.quantile(0.975))]
df.index = pd.to_datetime(df.index)

def draw_line_plot():
   # Draw line plot
   fig, ax = plt.subplots(figsize=(30, 12))
   ax.plot(df.index, df.value, color="r")
   ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
   ax.set_xlabel("Date")
   ax.set_ylabel("Page Views")

   # Save image and return fig (don't change this part)
   fig.savefig('Graphics/line_plot.png')
   return fig

def draw_bar_plot():
   # Copy and modify data for monthly bar plot
   df_bar = df.copy()

   # Draw bar plot
   df_bar = df_bar.resample("M").sum() / df_bar.resample("M").count()
   df_bar = df_bar.reset_index()
   df_bar = df_bar.groupby([
      df_bar.date.dt.month.rename("m"),
      df_bar.date.dt.month_name().rename("month"),
      df_bar.date.dt.year.rename("year")
   ]).value.sum()
   df_bar = df_bar.reset_index()[["month", "year", "value"]]

   # Plot form 1
   years = list(range(
      df_bar.year.min(),
      df_bar.year.max() + 1,
   ))
   labels = df_bar.month.unique().tolist()
   width = 1/20

   fig, ax = plt.subplots(figsize=(25, 15))

   for i, month in enumerate(labels):
      offset = width*i
      x = [i + offset for i in years]
      y = []
      for year in years:
         r = df_bar[(df_bar.month == month) &
                    (df_bar.year == year)]
         value = 0 if r.shape[0] == 0 else r.value.tolist()[0]
         y.append(value)
      rects = ax.bar(x, y, width, label=month)

   ax.set_xlabel("Years")
   ax.set_ylabel("Average Page Views")
   ax.set_xticks(
      [width*3 + i for i in years],
      years,
      rotation=90
   )
   ax.legend(title="Months")

   # Plot form 2
   # graphic = sns.catplot(
   #    data=df_bar,
   #    x="year", y="value", hue="month",
   #    kind="bar",
   # )
   # graphic.set(xlabel="Years", ylabel="Average Page Views")
   # graphic.legend.set_title("Months")

   # Save image and return fig (don't change this part)
   fig.savefig('Graphics/bar_plot.png')
   return fig

def draw_box_plot():
   # Prepare data for box plots (this part is done!)
   df_box = df.copy()
   df_box.reset_index(inplace=True)
   df_box['year'] = [d.year for d in df_box.date]
   df_box['month'] = [d.strftime('%b') for d in df_box.date]
   df_box['month_ix'] = [d.month for d in df_box.date]

   # Draw box plots (using Seaborn)
   fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(25, 15))

   g1 = sns.boxplot(
      data=df_box,
      x="year", y="value", hue="year",
      palette="tab10",
      legend=False,
      ax=ax1
   )
   g1.set(xlabel="Year", ylabel="Page Views")
   g1.set_title("Year-wise Box Plot (Trend)")
   g2 = sns.boxplot(
      data=df_box,
      x="month", y="value", hue="month",
      order=df_box.sort_values("month_ix").month.unique(),
      palette="bright",
      legend=False,
      ax=ax2
   )
   g2.set(xlabel="Month", ylabel="Page Views")
   g2.set_title("Month-wise Box Plot (Seasonality)")

   # Save image and return fig (don't change this part)
   fig.savefig('Graphics/box_plot.png')
   return fig
