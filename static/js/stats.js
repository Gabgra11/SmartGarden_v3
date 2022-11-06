// Dummy placeholder data:
var temps_7day = [70.4, 71.0, 70.9, 69.9, 70.2, 71.0, 71.2];
var humid_7day = [29.9, 30.1, 30.2, 29.8, 29.8, 30.1, 30.0];
var moist_7day = [85.2, 66.4, 45.2, 88.8, 67.9, 51.3, 44.2];
var water_7day = [true, false, false, true, false, false, false];
var day_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
var bar_colors = ['#42aaff', '#42aaff', '#42aaff', '#42aaff', '#42aaff', '#42aaff', '#42aaff'];

$(document).ready(function() {
  fillTempChart();
  fillHumidChart();
  fillMoistChart();
});



function fillTempChart() {
  var temps_chart = document.getElementById("tempBarChart").getContext('2d');

  var myBarChart = new Chart(temps_chart, {
      type: 'bar',
      data: {
        labels: day_labels,
        datasets: [{
          label: 'Temperature (F)',
          data: temps_7day,
          backgroundColor: bar_colors
        }]
      },
      options: {
        legend: {display: false},
        title: {
          display: true,
          text: "7-Day Temperature History"
        }
      }
    });
}

function fillMoistChart() {
  var moist_chart = document.getElementById("moistBarChart").getContext('2d');

  var myBarChart = new Chart(moist_chart, {
      type: 'bar',
      data: {
        labels: day_labels,
        datasets: [{
          label: 'Moisture (%)',
          data: moist_7day,
          backgroundColor: bar_colors
        }]
      },
      options: {
        legend: {display: false},
        title: {
          display: true,
          text: "7-Day Soil Moisture History"
        }
      }
    });
}

function fillHumidChart() {
  var humid_chart = document.getElementById("humidBarChart").getContext('2d');

  var myBarChart = new Chart(humid_chart, {
      type: 'bar',
      data: {
        labels: day_labels,
        datasets: [{
          label: 'Humidity (%)',
          data: humid_7day,
          backgroundColor: bar_colors
        }]
      },
      options: {
        legend: {display: false},
        title: {
          display: true,
          text: "7-Day Ambient Humidity History"
        }
      }
    });
}