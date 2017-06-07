# Data Visualization Project
Elias Laura Wiegandt

## Summary
The visualization is a scatter plot, that describes the relationship between average household wealth (x-axis), average score in the PISA math test (y-axis) and the percentage of students who take extra math lessons (color of points), for each country who took part in the PISA programme.
The data covers 68 countries and around 510,000 students.

## Design
The data wrangling was carried out in an iPyhton Jupyter Notebook. This notebook is included in the uploaded zipped folder. A code cookbook is included as a pdf.

The two main variables to be investigated were average household wealth and average math score. As the goal was to describe the relation between these two variables, a scatter plot was chosen.
Including all 510,000 data points in the visualization would have resulted in a too data-heavy plot. To remedy this, the average scores and household wealth for each country was computed. This resulted in a hump-like distribution of the data points, with the highest math scores seen for countries with average household wealth around the average of the countries' average household wealth.
To better show this distribution, the y-axis was scaled, to start at a high value and thus "zoom in" on the relationship between the x and y variables. This runs the risk of overstating the relationship, but also makes it easier for the reader to see the relationship graphically.
The x-axis was scaled to be in the interval [0;1]. The data was already in a scale without any intuitive interpretation. As the transformation does not alter the order or relative intervals between the observation for each country, no information was lost.

The average number of pupils who take more than two extra hours of math lessons, outside required school, was used to create a color scale for the points. Using this variable to color the chart shows that a lot of the countries with average household wealth, but high average math scores, also had high rates of extra math tuition. It also appears that a lot of the countries with high household wealth but average math scores were characterized by low extra tuition.
Using color shows the clusters in the data, and adds information on possible reasons behind the hump-like distribution. Nuances of blue and green colors were used, to not draw the eye to any specific observations and not cause trouble for any color blind viewers.

The project rubric states that an animation was to be included. I believe the default mouseover tooltip on the scatterplot is perfect for this chart, as it shows the reader what country each point in the plot represents.
A simple animation of the drawing of the chart was included. This animation was chosen because it gives the viewer a "sneak peak" of all the data. If there had been any outliers left out of the chart, they would be visible in this animation.

## Feedback
My sister Yaffah pointed out that the Dimple tool-tips was very important for finding out which points were which countries. We discussed if there could be other ways of encoding this information. We worked out a bar chart with country name on the x-axis, see "index_v02.html". This was useful for comparing the performance of subsets of countries (more than eight countries seem confusing to the viewer), but really only worked if only one variable was compared. Hence, a bar chart is not optimal, as the goal is to show the relation between average household wealth and average math test score.
Yaffah also presented the idea of using color to explain information that might relate to the hump-like distribution. In "index_v01.html", the chart before the implementation of this suggestion can be seen.
This led to the search for a variable that could do this, which resulted in the inclusion of the variable describing extra math tuition.

My friend Christian advised me on whether to change from a scatter plot to a bubble plot. This would provide the possibility of including a fourth variable in the plot.
We tested this, and the result can be seen in "index_v03.html".
But with a size-axis implemented the information in the chart seemed to blur more than it became clear. Thus, using a scatterplot was chosen as the model that best communicated the information in the data.

My friend Marie advised me on the interpretability. She especially wanted me to include a legend on the color scale. This is not possible in the current Dimple setup. Doing it in D3 is possible, but difficult. As the color grading of the points might not be of interest, simply excluding this variable seems like the better option.
Marie and I discussed extensively whether the animation of the drawing was "tacky". We ended up deciding to keep it, but made it faster (from 3 to 1.5 seconds).

The reviewer of the first submission required several changes. These were, most notably: better description on the webpage itself and a legend for the color codings, if they were to be included.
The html of the webpage was updated, so the header became more telling, a description of the data and links to different sources were added.
Including a colorlegend was attempted, but not successfully implemented in a satisfactory manner. Use Github log for intermediate results.
It was possible to include a color legend, consisting of a colorbar on the html page using "colorbar.js" (see references below for link to the Github repo it was copied from). But the interplay between the Dimple code in plot.js and the code in colorbar.js turned out to be erratic. Oftentimes, the colorbar would not be shown. No systematic pattern behind this could be discerned, it might have to do with whether the js code is asynchronous or synchronous.
Further, linking the colorbar to the data in the plot proved very difficult.
A manual approach was tried, with the colorbar fit "by hand" to the series. The was mediocre.
The color encoded the percentage of the student sample in each country who took more than two hours of extra math lessons outside school. As this was of secondary importance to the main finding, the relation between wealth and math score, it was decided to remove the color encodings from the chart.

## Resources
The information from the Dimple wiki was used extensively:
https://github.com/PMSI-AlignAlytics/dimple/wiki

All googles leads to stackexchange. No code is directly copied from here, but it was widely used for inspiration in solving small problems.
http://stackexchange.com/

Finally, the classroom examples from Udacity was used to build the visualization.
https://www.udacity.com/

Experiments with a colorbar were tried:
https://github.com/bmschmidt/colorbar/blob/master/index.html
