var w = 800,
    h = 500,
    fill = d3.scale.category20();

var vis = d3.select("#chart")
  .append("svg:svg")
    .attr("width", w)
    .attr("height", h);

d3.json("force.json", function(json) {
  //console.log(json);
  var force = d3.layout.force()
      .charge(-120)
      .linkDistance(100)
      .nodes(json.nodes)
      .links(json.links)
      .size([w, h])
      .start();

  var link = vis.selectAll("line.link")
      .data(json.links)
    .enter().append("svg:line")
      .attr("class", "link")
      .style("stroke-width", function(d) { return Math.sqrt(d.value); })
      .attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

  var node = vis.selectAll(".node")
    .data(json.nodes)
    .enter().append("g")
    .attr("class", "node")
    .call(force.drag);

  node.append("circle")
    .attr("r", 5)
    .style("fill", function (d) { return fill(d.group); })
    .attr("cx", function(d) { return d.x; })
    .attr("cy", function(d) { return d.y; });

  node.append("text")
    .attr("dx", 10)
    .attr("dy", ".35em")
    .text(function(d) { return d.id });

  vis.style("opacity", 1e-6)
    .transition()
      .duration(1000)
      .style("opacity", 1);

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    d3.selectAll("circle").attr("cx", function (d) {
        return d.x;
    })
        .attr("cy", function (d) {
        return d.y;
    });

    d3.selectAll("text").attr("x", function (d) {
        return d.x;
    })
        .attr("y", function (d) {
        return d.y;
    });
    
  });
});