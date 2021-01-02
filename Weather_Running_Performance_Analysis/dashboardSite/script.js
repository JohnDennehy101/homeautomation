// Firebase configuration
const firebaseConfig = {
  apiKey: config.firebaseApiKey,
  authDomain: config.firebaseAuthDomain,
  databaseURL: config.firebaseDatabaseURL,
  projectId: config.firebaseProjectId,
  storageBucket: config.firebaseStorageBucket,
  messagingSenderId: config.firebaseMessagingSenderId,
  appId: config.firebaseAppId,
};

firebase.initializeApp(firebaseConfig);

// Get a reference to the database service
const database = firebase.database();

// Create weather database reference
const weatherDataRef = database.ref("weatherData");

// Create run database reference
const runDataRef = database.ref("runningData");

//On addition of a new run activity to Firebase, the dashboard is updated (dynamically rendering HTML5 elements)
runDataRef.on("value", function (snapshot) {
  let runDataArr = [];
  let runCadenceArr = [];
  let runAverageSpeedArr = [];
  let runAverageHeartRateArr = [];
  let runDistanceArr = [];
  let runDateArr = [];
  let runElevationGainArr = [];
  //Each run activity in Firebase is pushed to the runDataArr
  snapshot.forEach((child) => {
    runDataArr.push(child.val());
  });
  //Loops through runDataArr to populate different arrays with distinct metrics from each run (cadence, speed, distance, elevation, average heart rate, run date)
  for (let i = 0; i < runDataArr.length; i++) {
    runCadenceArr.push(runDataArr[i]["average_cadence"]);
    runAverageSpeedArr.push(runDataArr[i]["average_speed"]);
    runDistanceArr.push(runDataArr[i]["distance"]);
    runElevationGainArr.push(runDataArr[i]["total_elevation_gain"]);
    runAverageHeartRateArr.push(runDataArr[i]["average_heartrate"]);
    runDateArr.push(runDataArr[i]["run_date"]);
  }

  //Obtaining latest run info
  let latestRun = runDataArr[runDataArr.length - 1];
  console.log(latestRun);
  //Dynamically creating elements for dashboard
  let runContainerElem = document.createElement("div");
  let mapElem = document.createElement("div");
  mapElem.id = "map";
  let runInfoContainerElem = document.createElement("div");
  //Elements for average run cadence
  let averageRunCadence = document.createElement("div");
  averageRunCadence.classList.add("runMetric");
  averageRunCadence.style.width = "50%";
  averageRunCadence.innerHTML =
    '<p>Average Cadence</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["average_cadence"] +
    "</p>";

  //Elements for average run heart rate
  let averageRunHeartRate = document.createElement("div");
  averageRunHeartRate.classList.add("runMetric");
  averageRunHeartRate.style.width = "50%";
  averageRunHeartRate.innerHTML =
    '<p>Average Heart Rate</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["average_heartrate"] +
    "</p>";

  //Elements for average run speed
  let averageRunSpeed = document.createElement("div");
  averageRunSpeed.classList.add("runMetric");
  averageRunSpeed.style.width = "50%";
  averageRunSpeed.innerHTML =
    '<p>Average Speed</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["average_speed"] +
    "</p>";

  //Latitude and Longitude positions for Google Maps Markers (obtained from latestRun object)
  let startLatitudeLongitude = latestRun["start_latlng"];
  let endLatitudeLongitude = latestRun["end_latlng"];

  //Elements for run max heart rate
  let maxHeartRate = document.createElement("div");
  maxHeartRate.classList.add("runMetric");
  maxHeartRate.innerHTML =
    '<p>Max Heart Rate</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["max_heartrate"] +
    "</p>";
  maxHeartRate.style.width = "50%";

  //Elements for run max speed
  let maxRunSpeed = document.createElement("div");
  maxRunSpeed.classList.add("runMetric");
  maxRunSpeed.style.width = "50%";
  maxRunSpeed.innerHTML =
    '<p>Max Speed</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["max_speed"] +
    "</p>";

  //Elements for run moving time
  let movingTime = document.createElement("div");
  movingTime.classList.add("runMetric");
  movingTime.style.width = "50%";
  movingTime.innerHTML =
    '<p>Moving Time (seconds)</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["moving_time"] +
    "</p>";

  //Elements for run date
  let runDate = document.createElement("div");

  runDate.style.width = "50%";
  runDate.classList.add("runMetric");
  runDate.innerHTML =
    '<p>Run Date</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["run_date"] +
    "</p>";

  //Elements for run start time
  let runStartTime = document.createElement("div");
  runStartTime.classList.add("runMetric");
  runStartTime.style.width = "50%";
  runStartTime.innerHTML =
    '<p>Run Start Time</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["start_time"] +
    "</p>";

  //Elements for run end time
  let runEndTime = document.createElement("div");
  runEndTime.classList.add("runMetric");
  runEndTime.style.width = "50%";
  runEndTime.innerHTML =
    '<p>Run End Time</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["end_time"] +
    "</p>";


  //Elements for activity type
  let activityType = document.createElement("div");
  activityType.classList.add("runMetric");
  activityType.innerHTML =
    '<p>Activity Type</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["type"] +
    "</p>";
  activityType.style.width = "50%";

  //Polyline for Google Maps Display
  let summaryPolyline = latestRun["summary_polyline"];

  //Elements for run title
  let runTitle = document.createElement("div");
  runTitle.classList.add("runMetric");

  runTitle.innerHTML =
    '<p>Activity Title</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["title"] +
    "</p>";
  runTitle.style.width = "50%";
  let runElevationGain = document.createElement("div");
  runElevationGain.classList.add("runMetric");
  runElevationGain.style.width = "50%";
  runElevationGain.innerHTML =
    '<p>Elevation Gain</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["total_elevation_gain"] +
    "</p>";

  //Appending dashboard items to runInfoContainerElem (parent div element on dashboard for latest run activity info)
  runInfoContainerElem.appendChild(runTitle);
  runInfoContainerElem.appendChild(runDate);

  runInfoContainerElem.appendChild(averageRunCadence);

  runInfoContainerElem.appendChild(averageRunHeartRate);
  runInfoContainerElem.appendChild(maxHeartRate);

  runInfoContainerElem.appendChild(averageRunSpeed);
  runInfoContainerElem.appendChild(maxRunSpeed);

  runInfoContainerElem.appendChild(movingTime);

  runInfoContainerElem.appendChild(runStartTime);
  runInfoContainerElem.appendChild(runEndTime);

  runInfoContainerElem.appendChild(runElevationGain);

  runInfoContainerElem.appendChild(activityType);

  runInfoContainerElem.classList.add("runInfoContainer");

  let latestRunContainerPlaceHolder = document.getElementById(
    "latestRunContainerPlaceHolder"
  );

  runContainerElem.appendChild(runInfoContainerElem);
  latestRunContainerPlaceHolder.appendChild(mapElem);
  latestRunContainerPlaceHolder.appendChild(runContainerElem);

  //Displaying Google Maps on dashboard with Polyline from Strava API response
  initMap(summaryPolyline, startLatitudeLongitude, endLatitudeLongitude)

  //Creating bar charts for run trends
  new Chart(document.getElementById("bar-chart"), {
    type: "bar",
    data: {
      labels: runDateArr,
      datasets: [
        {
          label: "Run Average Cadence",
          type: "line",
          borderColor: "#8e5ea2",
          data: runCadenceArr,
          fill: false,
        },
        {
          label: "Run Elevation Gain",
          type: "line",
          borderColor: "#3e95cd",
          data: runElevationGainArr,
          fill: false,
        },
        {
          label: "Run Average Heart Rate",
          type: "line",
          borderColor: "#FF0000",
          data: runAverageHeartRateArr,
          fill: false,
        },
        {
          label: "Run Average Cadence",
          type: "bar",
          backgroundColor: "rgba(0,0,0,0.2)",
          data: runCadenceArr,
        },
        {
          label: "Run Elevation Gain",
          type: "bar",
          backgroundColor: "rgba(0,0,0,0.2)",
          backgroundColorHover: "#3e95cd",
          data: runElevationGainArr,
        },
        {
          label: "Run Average Heart Rate",
          type: "bar",
          backgroundColor: "rgba(0,0,0,0.2)",
          backgroundColorHover: "#3e95cd",
          data: runAverageHeartRateArr,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Elevation Gain",
      },
      legend: { display: true },
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: false,
            },
          },
        ],
        xAxes: [
          {
            ticks: {
              autoSkip: false,
            },
          },
        ],
      },
    },
  });

  new Chart(document.getElementById("averageSpeed-chart"), {
    type: "bar",
    data: {
      labels: runDateArr,
      datasets: [
        {
          label: "Run Average Speed",
          type: "line",
          borderColor: "#ffa500",
          data: runAverageSpeedArr,
          fill: false,
        },
        {
          label: "Run Average Speed",
          type: "bar",
          backgroundColor: "rgba(0,0,0,0.2)",
          data: runAverageSpeedArr,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Run Average Speed (Metres Per Second)",
      },
      legend: { display: true },
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: false,
            },
          },
        ],
        xAxes: [
          {
            ticks: {
              autoSkip: false,
            },
          },
        ],
      },
    },
  });

  new Chart(document.getElementById("runDistance-chart"), {
    type: "bar",
    data: {
      labels: runDateArr,
      datasets: [
        {
          label: "Run Distance",
          type: "line",
          borderColor: "#00b300",
          data: runDistanceArr,
          fill: false,
        },
        {
          label: "Run Distance",
          type: "bar",
          backgroundColor: "rgba(0,0,0,0.2)",
          data: runDistanceArr,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Run Distance (Metres)",
      },
      legend: { display: true },
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: false,
            },
          },
        ],
        xAxes: [
          {
            ticks: {
              autoSkip: false,
            },
          },
        ],
      },
    },
  });
});

//This function declares a Google Maps map which takes the polyline (from Strava API response), latitude and longitude to display a map on the dashboard with the run route marked (with markers for start and end positions)
function initMap(polyline, startLatitudeLongitude, endLatitudeLongitude) {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 53.3634, lng: -6.2579 },
    zoom: 16,
  });

  let encoded_data = polyline;
  let decode = google.maps.geometry.encoding.decodePath(encoded_data);

  let line = new google.maps.Polyline({
    path: decode,
    strokeColor: "#00008B",
    strokeOpacity: 1.0,
    strokeWeight: 4,
    zIndex: 3,
  });

  function zoomToObject(obj) {
    var bounds = new google.maps.LatLngBounds();
    var points = obj.getPath().getArray();
    for (var n = 0; n < points.length; n++) {
      bounds.extend(points[n]);
    }
    map.fitBounds(bounds);
  }

  zoomToObject(line);

  line.setMap(map);

  let startLatLng = {
    lat: startLatitudeLongitude[0],
    lng: startLatitudeLongitude[1],
  };
  let endLatLng = {
    lat: endLatitudeLongitude[0],
    lng: endLatitudeLongitude[1],
  };
  new google.maps.Marker({
    position: startLatLng,
    map,
    icon: "https://maps.google.com/mapfiles/ms/icons/green-dot.png",
    title: "Hello World!",
  });

  new google.maps.Marker({
    position: endLatLng,
    map,
    icon: "https://maps.google.com/mapfiles/ms/icons/red-dot.png",
    title: "Hello World!",
  });
}

//Reference to firebase 'weatherData' to obtain last 30 records in database (as info is pushed to firebase at a 2 minute interval, the weather data displayed is for the last hour)
weatherDataRef.limitToLast(30).on("value", function (snapshot) {
  let timeData = [];
  let cloudData = [];
  let humidityData = [];
  let perceivedTemperatureData = [];
  let outdoorTemperatureData = [];
  let indoorTemperatureData = [];
  let pressureData = [];
  let rainVolumeData = [];
  let windSpeedData = [];
  let windGustData = [];

  //Populating weatherDataArr with weather data from Firebase. This is then used to populate different arrays that are used with Chart.js charts to show weather information for the past hour
  snapshot.forEach((child) => {
    weatherDataArr.push(child.val());

    cloudData = loopThroughWeatherData(weatherDataArr, "cloudCoverPercentage");
    humidityData = loopThroughWeatherData(weatherDataArr, "humidity");
    perceivedTemperatureData = loopThroughWeatherData(
      weatherDataArr,
      "perceivedTemperature"
    );
    outdoorTemperatureData = loopThroughWeatherData(
      weatherDataArr,
      "outdoor_temperature"
    );
    indoorTemperatureData = loopThroughWeatherData(
      weatherDataArr,
      "indoor_temperature"
    );
    pressureData = loopThroughWeatherData(weatherDataArr, "pressure");
    rainVolumeData = loopThroughWeatherData(
      weatherDataArr,
      "rainVolumeLastHour"
    );
    windSpeedData = loopThroughWeatherData(weatherDataArr, "windSpeed");
    windGustData = loopThroughWeatherData(weatherDataArr, "windGust");
    timeData = WeatherTimeData(weatherDataArr);
  });

  //Chart.js configuration for cloud cover
  var cloudCoverConfig = {
    type: "line",
    data: {
      labels: timeData,
      datasets: [
        {
          data: cloudData,
          label: "Cloud Cover Percentage",
          borderColor: "#808080",
          fill: false,
        },

        {
          data: rainVolumeData,
          label: "Rain Volume",
          borderColor: "#FFD25A",
          fill: false,
        },
      ],
    },
    options: {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
        xAxes: [
          {
            ticks: {
              autoSkip: false,
            },
          },
        ],
      },
      responsive: false,
      maintainAspectRatio: false,
    },
  };

  //Chart.js configuration for humidity
  var humidityConfig = {
    type: "line",
    data: {
      labels: timeData,
      datasets: [
        {
          data: humidityData,
          label: "Humidity",
          borderColor: "#A4BFEB",
          fill: false,
        },
      ],
    },
    options: {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
        xAxes: [
          {
            ticks: {
              autoSkip: false,
            },
          },
        ],
      },
      responsive: false,
      maintainAspectRatio: false,
    },
  };

  //Chart.js configuration for temperature
  var temperatureConfig = {
    type: "line",
    data: {
      labels: timeData,
      datasets: [
        {
          data: outdoorTemperatureData,
          label: "Temperature",
          borderColor: "#BBA0B2",
          fill: false,
        },
        {
          data: indoorTemperatureData,
          label: "Indoor Temperature",
          borderColor: "#B6C197",
          fill: false,
        },
        {
          data: perceivedTemperatureData,
          label: "Perceived Temperature",
          borderColor: "#A4A8D1",
          fill: false,
        },
      ],
    },
    options: {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
        xAxes: [
          {
            ticks: {
              autoSkip: false,
            },
          },
        ],
      },
      responsive: false,
      maintainAspectRatio: false,
    },
  };

  //Chart.js configuration for pressure
  var pressureConfig = {
    type: "line",
    data: {
      labels: timeData,
      datasets: [
        {
          data: pressureData,
          label: "Pressure",
          borderColor: "#376996",
          fill: false,
        },
      ],
    },
    options: {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
        xAxes: [
          {
            ticks: {
              autoSkip: false,
            },
          },
        ],
      },
      responsive: false,
      maintainAspectRatio: false,
    },
  };


  //Chart.js configuration for wind gust
  var windGustConfig = {
    type: "line",
    data: {
      labels: timeData,
      datasets: [
        {
          data: windGustData,
          label: "Wind Gust",
          borderColor: "#B6C197",
          fill: false,
        },
        {
          data: windSpeedData,
          label: "WindSpeed",
          borderColor: "#FFAA5A",
          fill: false,
        },
      ],
    },
    options: {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
        xAxes: [
          {
            ticks: {
              autoSkip: false,
            },
          },
        ],
      },
      responsive: false,
      maintainAspectRatio: false,
    },
  };

  //Initialising the different charts
  var chart = new Chart(cloudCoverChart, cloudCoverConfig);
  var chart = new Chart(humidityChart, humidityConfig);
  var chart = new Chart(temperatureChart, temperatureConfig);
  var chart = new Chart(pressureChart, pressureConfig);
  var chart = new Chart(windGustChart, windGustConfig);

  weatherDataArr = [];
});

var cloudCoverChart = document
  .getElementById("cloudCoverChart")
  .getContext("2d");
var humidityChart = document.getElementById("humidityChart").getContext("2d");
var temperatureChart = document
  .getElementById("temperatureChart")
  .getContext("2d");

var pressureChart = document.getElementById("pressureChart").getContext("2d");

var windGustChart = document.getElementById("windGustChart").getContext("2d");

let LatitudeLongitude = { lat: 53.3634, lng: -6.2579 };

let map;

function loopThroughWeatherData(arr, weatherCondition) {
  let finalArr = [];
  for (i = 0; i < arr.length; i++) {
    finalArr.push(arr[i][weatherCondition]);
  }
  return finalArr;
}


function WeatherTimeData(arr) {
  let finalArr = [];
  for (i = 0; i < arr.length; i++) {
    finalArr.push(arr[i].time);
  }
  return finalArr;
}

