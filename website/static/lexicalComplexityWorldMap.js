document.addEventListener("DOMContentLoaded", function() {
  var svg = d3.select("#worldMap")
    .attr("width", window.innerWidth)
    .attr("height", window.innerHeight);

  var projection = d3.geoAitoff()
    .scale((window.innerWidth - 50) / (2 * Math.PI))
    .translate([window.innerWidth / 2, window.innerHeight / 2]);

  var path = d3.geoPath().projection(projection);

  var tooltip = d3.select("#tooltip");

  var colorScale = d3.scaleSequential(d3.interpolateRdYlBu)
    .domain([0.65, 0.8]);

  var geoData;

  function fetchData(year) {
    fetch(`/data4?year=${year}`)
      .then(response => response.json())
      .then(data => {
        console.log("Data fetched from server:", data);
        updateMap(data);
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  }

  function updateMap(sentimentData) {
    if (!geoData) {
      console.error("Geo data is not loaded.");
      return;
    }

    var countries = svg.selectAll("path")
      .data(geoData.features, function(d) { return d.properties.A3; });

    countries.enter().append("path")
      .attr("class", "country")
      .merge(countries)
      .attr("d", path)
      .attr("fill", function(d) {
        const countryCode = d.properties.A3;
        const sentiment = sentimentData[countryCode];
        console.log(`Country Code: ${countryCode}, Sentiment: ${sentiment}`);
        return sentiment !== undefined ? colorScale(sentiment) : "grey";
      });

    countries.exit().remove();
  }

  d3.json("/static/world_with_country_names.geojson").then(function(data) {
    geoData = data;
    fetchData(1946);

    window.addEventListener("resize", function() {
      svg.attr("width", window.innerWidth)
         .attr("height", window.innerHeight);

      projection
        .scale((window.innerWidth - 50) / (2 * Math.PI))
        .translate([window.innerWidth / 2, window.innerHeight / 2]);

      svg.selectAll("path").attr("d", path);
    });

    var slider = document.getElementById("yearSlider");
    slider.addEventListener("input", function() {
      var year = slider.value;
      document.getElementById("yearLabel").textContent = year; // Update the year label
      fetchData(year);
    });

    createSliderTicks();
  }).catch(function(error) {
    console.error("Error loading geo data:", error);
  });

  function createSliderTicks() {
    var slider = document.getElementById("yearSlider");
    var sliderTicks = document.getElementById("sliderTicks");
    var min = parseInt(slider.min);
    var max = parseInt(slider.max);
    var step = 1; // Every year

    for (var year = min; year <= max; year += step) {
      var tick = document.createElement("div");
      tick.className = "tick";
      var position = ((year - min) / (max - min)) * 100;
      tick.style.left = position + "%";
      sliderTicks.appendChild(tick);

      var tickLabel = document.createElement("div");
      tickLabel.className = "tick-label";
      tickLabel.style.left = position + "%";
      tickLabel.style.transform = "translateX(-50%)";

      var yearStr = year.toString();
      yearStr.split("").forEach(function(char) {
        var charDiv = document.createElement("div");
        charDiv.textContent = char;
        tickLabel.appendChild(charDiv);
      });

      sliderTicks.appendChild(tickLabel);
    }
  }
});
