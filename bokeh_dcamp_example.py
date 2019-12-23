# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 15:19:22 2019

@author: Moji
"""

# Perform necessary imports

from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, Select, Slider, CategoricalColorMapper
from bokeh.layouts import row, widgetbox
from bokeh.palettes import Spectral6
import pandas as pd
### read data from github csv file
url = 'https://raw.githubusercontent.com/johnashu/datacamp/master/gapminder1.csv'
data = pd.read_csv(url, error_bad_lines=False, index_col ='Year')

# Make a unique list of regions 
regions_list = data.region.unique().tolist()
# create a color maper for different regions in plot
color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)
# Make the ColumnDataSource: source

source = ColumnDataSource(data={
    'x'       : data.loc[1970].fertility,
    'y'       : data.loc[1970].life,
    'country' : data.loc[1970].Country,
    'pop'     : (data.loc[1970].population / 20000000) + 2,
    'region'  : data.loc[1970].region,
})
def update_plot(attr, old, new):
    # Read the current value off the slider and 2 dropdowns: yr, x, y
    yr = slider.value
    x = x_select.value
    y = y_select.value
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    # Set new_data
    new_data = {
        'x'       : data.loc[yr][x],
        'y'       : data.loc[yr][y],
        'country' : data.loc[yr].Country,
        'pop'     : (data.loc[yr].population / 20000000) + 2,
        'region'  : data.loc[yr].region,
    }
    # Assign new_data to source.data
    source.data = new_data

    # Set the range of all axes
    plot.x_range.start = min(data[x])
    plot.x_range.end = max(data[x])
    plot.y_range.start = min(data[y])
    plot.y_range.end = max(data[y])

    # Add title to plot
    plot.title.text = 'Gapminder data for %d' % yr


# Create the figure: p
plot = figure(title='Gapminder data for 1970', x_axis_label='Fertility (children per woman)', y_axis_label='Life Expectancy (years)',
           plot_height=400, plot_width=700,
           tools=[HoverTool(tooltips='@country'), 'pan','box_zoom', 'box_select'])

# Add a circle glyph to the figure p
plot.circle(x='x', y='y', source=source,color=dict(field='region', transform=color_mapper), legend='region')
plot.legend.location ='bottom_left'
slider = Slider(start=1970, end=2010, step=1, value=1970, title='Year')

# Attach the callback to the 'value' property of slider
slider.on_change('value', update_plot)

# Create a dropdown Select widget for the x data: x_select
x_select = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='fertility',
    title='x-axis data'
)

# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', update_plot)

# Create a dropdown Select widget for the y data: y_select
y_select = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='life',
    title='y-axis data'
)
y_select.on_change('value', update_plot)

layout = row(widgetbox(slider, x_select, y_select), plot)
curdoc().add_root(layout)
curdoc().title = 'Gapminder'
