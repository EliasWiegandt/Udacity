function draw(data) {

    /*
      D3.js setup code
    */
    "use strict";
    var margin = 0,
        width = 540 - margin,
        height = 350 - margin;

    var svg = d3.select(".chart1")
        .append("svg")
        .attr('class', 'svg_element')
        .attr("width", width + margin)
        .attr("height", height + margin)
        .append('g')
        .attr('class', 'chart');

    var myChart = new dimple.chart(svg, data);

    // X-AXIS
    var x = myChart.addMeasureAxis("x", "Mean household wealth");
    x.title = "Mean Household Wealth, relative scale";

    // Y-AXIS
    var y = myChart.addMeasureAxis("y", 'Mean math test score');
    y.overrideMin = 350;
    y.title = "Mean Math Score";
    y.ticks = 6;

    myChart.addSeries(["Country", ""], dimple.plot.scatter);
    myChart.setBounds(50, 20, width - margin - 100, height - margin - 100)
    myChart.draw(1500);
};

d3.csv("Pisa2012_country_mean_scaled.csv", function(data) {
    data.forEach(function(d) {
        d['Mean math test score'] = +d['Mean math test score'];
        d["Extra math classes"] = +d["Extra math classes"];
        d["Mean household wealth"] = +d["Mean household wealth"];
    });
    draw(data);
});
