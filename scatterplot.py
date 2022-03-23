from turtle import left
from bokeh.plotting import figure, ColumnDataSource
from bokeh.io import output_file, show
from bokeh.models import HoverTool, BoxAnnotation, Label, LabelSet

#import rankings CSV and create dataframe for Bokeh to read from
datapath = r"C:\...\qbranks2021.csv"
data = pandas.read_csv(datapath)
df = pandas.DataFrame(data)

#Create ColumnDataSource from dataframe
source = ColumnDataSource(df)

#Create figure
p = figure(title='2021 - QB Avg vs. IQR', tooltips= "Player: @PlayerName", x_axis_label="Avg Score", y_axis_label="Interquartile Range")
p.title.align = 'center'
p.title.text_font_size = '25px'

#Labels
labels = LabelSet(x='Average', y='IQR', text='PlayerName', x_offset=1, y_offset=1, source=source, render_mode='canvas', text_font_size='10px')
p.add_layout(labels)

#Adding Box Annotations
tier1 = BoxAnnotation(left=25, top=15, fill_alpha=0.2, fill_color='green')
tier2 = BoxAnnotation(left=25, bottom=15, fill_alpha=0.2, fill_color='yellow')
tier3 = BoxAnnotation(right=25, left=20, fill_alpha=0.2, fill_color='orange')
tier4 = BoxAnnotation(right=20, fill_alpha=0.2, fill_color='red')

p.add_layout(tier1)
p.add_layout(tier2)
p.add_layout(tier3)
p.add_layout(tier4)


#Add circle glyphs to figure
p.circle('Average', 'IQR', source = source)

show(p)
