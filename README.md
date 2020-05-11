# Film Festival Visualization
An interactive map that shows the recipients of best actor/actress, director, and film in the Berlin, Cannes, and Venice film festivals over the past ~90 years.

## Python Dependencies
- Geopandas
- Json
- Bokeh
- Pandas
- Numpy

## How to Use
- Once you have installed the proper dependencies, run the command

      bokeh serve --show gui.py
- Use the slider to see the heatmap change over the years
- Hover over countries on the map to see how many and which awards were given to that country for the year selected.
      
      - Awards that were given to countries that no longer exist are mapped to their modern day geographic counterparts.

## Resources
- https://towardsdatascience.com/a-complete-guide-to-an-interactive-geographical-map-using-python-f4c5197e23e0
