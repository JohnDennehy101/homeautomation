// Your web app's Firebase configuration
const firebaseConfig = {
  /*apiKey: process.env.apiKey,
    authDomain: process.env.authDomain,
    databaseURL: process.env.databaseURL,
    projectId: process.env.projectId,
storageBucket: process.env.storageBucket,
  messagingSenderId: process.env.messagingSenderId,
  appId: process.env.appId,*/
  apiKey: config.firebaseApiKey,
  authDomain: config.firebaseAuthDomain,
  databaseURL: config.firebaseDatabaseURL,
  projectId: config.firebaseProjectId,
  storageBucket: config.firebaseStorageBucket,
  messagingSenderId: config.firebaseMessagingSenderId,
  appId: config.firebaseAppId,
};

firebase.initializeApp(firebaseConfig);

/*firebase.database().ref('weather-running-performance-default-rtdb/test').once('value').then(function(snapshot) {
    console.log(snapshot);
});*/

// Get a reference to the database service
const database = firebase.database();

// Create weather database reference
const weatherDataRef = database.ref("weatherData");

// Create run database reference
const runDataRef = database.ref("runningData");

runDataRef.on("value", function (snapshot) {
  let runDataArr = [];
  let runCadenceArr = [];
  let runAverageSpeedArr = [];
  let runAverageHeartRateArr = [];
  let runDistanceArr = [];
  let runDateArr = [];
  let runElevationGainArr = [];
  snapshot.forEach((child) => {
    runDataArr.push(child.val());
  });
  for (let i = 0; i < runDataArr.length; i++) {
    runCadenceArr.push(runDataArr[i]["average_cadence"]);
    runAverageSpeedArr.push(runDataArr[i]["average_speed"]);
    runDistanceArr.push(runDataArr[i]["distance"]);
    runElevationGainArr.push(runDataArr[i]["total_elevation_gain"]);
    runAverageHeartRateArr.push(runDataArr[i]["average_heartrate"]);
    runDateArr.push(runDataArr[i]["run_date"]);
  }

  let latestRun = runDataArr[runDataArr.length - 1];
  console.log(latestRun);
  let runContainerElem = document.createElement("div");
  //runContainerElem.id = 'runContainerMap'
  //runContainerElem.style.width = '70%';
  //runContainerElem.style.display = 'flex'
  let mapElem = document.createElement("div");
  mapElem.id = "map";
  let runInfoContainerElem = document.createElement("div");
  //Need to come back to this - adding material icons would be a nice touch
  //let averageRunCadence = document.createElement('p')
  let averageRunCadence = document.createElement("div");
  averageRunCadence.classList.add("runMetric");
  //averageRunCadence.style.display = 'inline-block'
  averageRunCadence.style.width = "50%";
  //averageRunCadence.textContent = 'Average Cadence ' + latestRun['average_cadence']
  averageRunCadence.innerHTML =
    '<p>Average Cadence</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["average_cadence"] +
    "</p>";

  //let averageRunHeartRate = document.createElement('p')
  let averageRunHeartRate = document.createElement("div");
  //averageRunHeartRate.style.display = 'inline-block'
  averageRunHeartRate.classList.add("runMetric");
  averageRunHeartRate.style.width = "50%";
  //averageRunHeartRate.textContent = 'Average Heart Rate ' + latestRun['average_heartrate']
  averageRunHeartRate.innerHTML =
    '<p>Average Heart Rate</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["average_heartrate"] +
    "</p>";

  //let averageRunSpeed = document.createElement('p')
  let averageRunSpeed = document.createElement("div");
  averageRunSpeed.classList.add("runMetric");
  //averageRunSpeed.style.display = 'inline-block'
  averageRunSpeed.style.width = "50%";
  //averageRunSpeed.textContent = 'Average Speed ' + latestRun['average_speed']
  averageRunSpeed.innerHTML =
    '<p>Average Speed</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["average_speed"] +
    "</p>";
  //Latitude and Longitude positions for Google Maps Markers
  let startLatitudeLongitude = latestRun["start_latlng"];
  let endLatitudeLongitude = latestRun["end_latlng"];

  //let maxHeartRate = document.createElement('p')
  let maxHeartRate = document.createElement("div");
  maxHeartRate.classList.add("runMetric");
  maxHeartRate.innerHTML =
    '<p>Max Heart Rate</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["max_heartrate"] +
    "</p>";
  //maxHeartRate.textContent = 'Max Heart Rate ' + latestRun['max_heartrate']
  //maxHeartRate.style.display = 'inline-block'
  maxHeartRate.style.width = "50%";

  //let maxRunSpeed = document.createElement('p')
  let maxRunSpeed = document.createElement("div");
  maxRunSpeed.classList.add("runMetric");
  //maxRunSpeed.style.display = 'inline-block'
  maxRunSpeed.style.width = "50%";
  //maxRunSpeed.textContent = 'Max Speed ' + latestRun['max_speed']
  maxRunSpeed.innerHTML =
    '<p>Max Speed</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["max_speed"] +
    "</p>";

  //let movingTime = document.createElement('p')
  let movingTime = document.createElement("div");
  movingTime.classList.add("runMetric");
  //movingTime.style.display = 'inline-block'
  movingTime.style.width = "50%";
  //movingTime.textContent = 'Moving Time (seconds) ' + latestRun['moving_time']
  movingTime.innerHTML =
    '<p>Moving Time (seconds)</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["moving_time"] +
    "</p>";
  //let runDate = document.createElement('p')
  let runDate = document.createElement("div");
  //runDate.style.display = 'inline-block'

  runDate.style.width = "50%";
  runDate.classList.add("runMetric");
  runDate.innerHTML =
    '<p>Run Date</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["run_date"] +
    "</p>";
  //runDate.textContent = 'Run Date ' + latestRun['run_date']

  //let runStartTime = document.createElement('p')
  let runStartTime = document.createElement("div");
  runStartTime.classList.add("runMetric");
  //runStartTime.style.display = 'inline-block'
  runStartTime.style.width = "50%";
  //runStartTime.textContent = 'Start Time ' + latestRun['start_time']
  runStartTime.innerHTML =
    '<p>Run Start Time</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["start_time"] +
    "</p>";

  //let runEndTime = document.createElement('p')
  let runEndTime = document.createElement("div");
  runEndTime.classList.add("runMetric");
  //runEndTime.style.display = 'inline-block'
  runEndTime.style.width = "50%";
  //runEndTime.textContent = 'End Time ' + latestRun['end_time']
  runEndTime.innerHTML =
    '<p>Run End Time</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["end_time"] +
    "</p>";

  //let activityType = document.createElement('p')
  let activityType = document.createElement("div");
  activityType.classList.add("runMetric");
  activityType.innerHTML =
    '<p>Activity Type</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["type"] +
    "</p>";
  //activityType.textContent = 'Activity Type ' + latestRun['type']
  //activityType.style.display = 'inline-block'
  activityType.style.width = "50%";

  //Polyline for Google Maps Display
  let summaryPolyline = latestRun["summary_polyline"];

  //let runTitle = document.createElement('p')
  let runTitle = document.createElement("div");
  runTitle.classList.add("runMetric");

  //runTitle.textContent = 'Activity Title ' + latestRun['title']
  runTitle.innerHTML =
    '<p>Activity Title</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["title"] +
    "</p>";
  //runTitle.style.display = 'inline-block';
  runTitle.style.width = "50%";
  //let runElevationGain = document.createElement('p')
  let runElevationGain = document.createElement("div");
  runElevationGain.classList.add("runMetric");
  //runElevationGain.style.display = 'inline-block'
  runElevationGain.style.width = "50%";
  //runElevationGain.textContent = 'Total Elevation Gain ' + latestRun['total_elevation_gain']
  runElevationGain.innerHTML =
    '<p>Elevation Gain</p><i class="material-icons">arrow_forward</i>' +
    "<p>" +
    latestRun["total_elevation_gain"] +
    "</p>";

  //Appending items (probably will be changed)
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

  //Commenting out to save on API calls
  //initMap(summaryPolyline, startLatitudeLongitude, endLatitudeLongitude)
  console.log(runElevationGainArr);
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
  console.log(startLatLng);
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

weatherDataRef.limitToLast(60).on("value", function (snapshot) {
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

  snapshot.forEach((child) => {
    //console.log(child.key, child.val());
    weatherDataArr.push(child.val());
    //console.log("intVal",cloudDataArr);

    //cloudData = loopThroughWeatherData(weatherDataArr)
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
//var perceivedTemperatureChart = document.getElementById('perceivedTemperatureChart').getContext('2d');
//var indoorTemperatureChart = document.getElementById('indoorTemperatureChart').getContext('2d');
var pressureChart = document.getElementById("pressureChart").getContext("2d");
//var windSpeedChart = document.getElementById('windSpeedChart').getContext('2d');
var windGustChart = document.getElementById("windGustChart").getContext("2d");
//var rainVolumeChart = document.getElementById('rainVolumeChart').getContext('2d');

let LatitudeLongitude = { lat: 53.3634, lng: -6.2579 };

let map;

function loopThroughWeatherData(arr, weatherCondition) {
  let finalArr = [];
  for (i = 0; i < arr.length; i++) {
    finalArr.push(arr[i][weatherCondition]);
    //finalArr.push(arr[i].cloudCoverPercentage);
    //cloudCoverPercentage: 54
    description: "Cloudy";
    humidity: 20;
    perceivedTemperature: 2.6;
    pressure: 10;
    rainVolumeLastHour: 0;
    temperature: 3.2;
    time: "14:14:45";
    windDirectionDegrees: 90;
    windGust: 2.4;
    windSpeed: 3.5;
  }
  return finalArr;
}

function test(time) {
  console.log(time);
}

test(timeData);

function WeatherTimeData(arr) {
  let finalArr = [];
  for (i = 0; i < arr.length; i++) {
    finalArr.push(arr[i].time);
    //cloudCoverPercentage: 54
    description: "Cloudy";
    humidity: 20;
    perceivedTemperature: 2.6;
    pressure: 10;
    rainVolumeLastHour: 0;
    temperature: 3.2;
    time: "14:14:45";
    windDirectionDegrees: 90;
    windGust: 2.4;
    windSpeed: 3.5;
  }
  return finalArr;
}

// Sync on any updates to the DB. THIS CODE RUNS EVERY TIME AN UPDATE OCCURS ON THE DB.
camRef.limitToLast(1).on("value", function (snapshot) {
  snapshot.forEach(function (childSnapshot) {
    const image = childSnapshot.val()["test"];
    console.log(image);
    document.getElementById("test").textContent = image;
  });
});

function getDateData() {
  var data = [];
  for (var i = 0; i < assessmentDates.length; i++) {
    let time = assessmentDates[i].indexOf("-202");
    let formattedDate = "";

    formattedDate = assessmentDates[i].substr(0, time);

    data.push(formattedDate);
  }

  return data;
}
