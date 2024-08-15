document.addEventListener("DOMContentLoaded", function() {
  var svg = d3.select("#worldMap")
    .attr("width", window.innerWidth)
    .attr("height", window.innerHeight);

  var projection = d3.geoAitoff()
    .scale((window.innerWidth - 50) / (2 * Math.PI))
    .translate([window.innerWidth / 2, window.innerHeight / 2]);

  var path = d3.geoPath().projection(projection);

  var colorScale = d3.scaleSequential(d3.interpolateViridis)
    .domain([0, 10000]);  // Adjust based on expected word count range

  function fetchData(year) {
    fetch(`/data?year=${year}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log("Data fetched from server:", data);

        var wordCounts = {};
        data.forEach(d => {
          wordCounts[d.country_code] = d.word_count;
        });

        d3.json("/static/world_with_country_names.geojson").then(function(geoData) {
          var countries = svg.selectAll("path")
            .data(geoData.features);

          // Apply the color scale immediately to all countries
          function getFillColor(d) {
            const countryCode = d.properties.A3;
            const wordCount = wordCounts[countryCode];
            console.log(`Country Code: ${countryCode}, Word Count: ${wordCount}`);  // Log for debugging
            return wordCount ? colorScale(wordCount) : "grey";
          }

          countries.enter().append("path")
            .attr("class", "country")
            .merge(countries)
            .attr("d", path)
            .attr("fill", getFillColor);

          countries.exit().remove();

          // Update the fill color for all countries immediately after the data is fetched
          svg.selectAll("path").attr("fill", getFillColor);
        });
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  }

  function updateSliderTicks() {
    var slider = document.getElementById("yearSlider");
    var ticksContainer = document.getElementById("sliderTicks");
    var minYear = parseInt(slider.min, 10);
    var maxYear = parseInt(slider.max, 10);
    var step = 1;
    var width = slider.offsetWidth;

    // Remove existing ticks
    ticksContainer.innerHTML = '';

    for (var year = minYear; year <= maxYear; year += step) {
      var tick = document.createElement('div');
      tick.className = 'tick';
      var tickLabel = document.createElement('div');
      tickLabel.className = 'tick-label';
      tickLabel.textContent = year;

      var position = ((year - minYear) / (maxYear - minYear)) * width;
      tick.style.left = position + 'px';
      tickLabel.style.left = position + 'px';

      ticksContainer.appendChild(tick);
      ticksContainer.appendChild(tickLabel);
    }
  }

  var yearSlider = document.getElementById("yearSlider");
  var yearLabel = document.getElementById("yearLabel");

  yearSlider.addEventListener("input", function() {
    var year = yearSlider.value;
    yearLabel.textContent = year;
    fetchData(year);
  });

  window.addEventListener("resize", function() {
    svg.attr("width", window.innerWidth)
       .attr("height", window.innerHeight);

    projection
      .scale((window.innerWidth - 50) / (2 * Math.PI))
      .translate([window.innerWidth / 2, window.innerHeight / 2]);

    svg.selectAll("path").attr("d", path);
  });

  // Initial data load
  fetchData(yearSlider.value);

  // Initialize slider ticks
  updateSliderTicks();
});
