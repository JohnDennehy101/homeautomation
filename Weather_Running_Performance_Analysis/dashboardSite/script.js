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

// Create camera database reference
const camRef = database.ref("weatherData");

camRef.on("value", (snapshot) => {
  let timeData = [];
  let cloudData = [];
  snapshot.forEach((child) => {
    //console.log(child.key, child.val());
    testArr.push(child.val());
    console.log("intVal", testArr);
    cloudData = loopThroughWeatherData(testArr);
    timeData = WeatherTimeData(testArr);
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

  var chart = new Chart(cloudCover, cloudCoverConfig);
  testArr = [];
});

var cloudCover = document.getElementById("cloudCoverChart").getContext("2d");

let LatitudeLongitude = { lat: 53.3634, lng: -6.2579 };

let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 53.3634, lng: -6.2579 },
    zoom: 16,
  });

  let encoded_data =
    "keudInsee@Kj@a@xAw@hGw@|Eq@vF_AdG_@nBw@tG_@nC]pBe@zESpAs@lDInAGPIJy@CIGM@{@Aw@Mc@O_@WuAs@}DeB{DyBc@Sa@W_Aa@mAu@s@_@c@]_Ak@g@k@[o@U_@]a@m@cAsAgBuA{BMS]IGGOQWg@e@e@QK_@G_BIy@Ku@MwAKQGEGWIy@]o@QcB[eA[oB_As@Bq@Rq@Fg@LU@y@Ns@H_ARq@He@Gs@XOLq@HoAd@i@JqAZUBgBSyA?g@C_@Em@UGKBmAPo@l@cB`@aBRmAFmBGc@Ce@[_@Sa@OQIBKP[L{A@i@Q]G]Ka@KS[KKCs@@e@Ia@Jq@CKDcAHYFEH?NDl@@h@AXJh@LJABE@a@Bs@Au@O_@Sw@{@_CQu@MQSIOHGHcAhBQTIDM?kBOm@@[GMIO?GBMPOnAHzDKdBFx@KnCDzAAz@FhEBr@AhA@bANb@v@Vp@DjANV?jCf@x@AtABXLRRJFf@Ll@Hp@A`@Dt@Cb@DPHdA@rBk@v@QjAa@DINqA?c@h@eF@e@f@qDR{@NoBB}A|AkLFq@AQPoB?_@Le@?KNe@EUHaBf@gENmBJw@By@Fu@\\yARuALiAJ_@@q@DQDw@XqBVmAJ}@Py@LELUPBJHJ@f@XRPp@`@x@v@d@\\VHf@LZLn@`@vB|@p@PXNXXdAr@d@j@XJb@Tb@h@J@T?NDLNJD\\XRH\\VNBNLp@Rn@ZTRTLPNXNn@Rz@d@d@PfAx@VJdBT^LRBh@XPFPNn@C^K\\ODJl@\\\\@NJj@PfAz@zAn@HFLPPHDHhAz@j@Rv@j@^^`An@d@h@N\\LJJT?LBHLALN|@h@VKDBb@r@LJXN^Zb@l@p@h@NV?Hw@pE";
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
  /*new google.maps.Marker({
      position: LatitudeLongitude,
      map,
      title: "Hello World!",
    }); */
}

function loopThroughWeatherData(arr) {
  let finalArr = [];
  for (i = 0; i < arr.length; i++) {
    finalArr.push(arr[i].cloudCoverPercentage);
    //cloudCoverPercentage: 54
    /*description: "Cloudy"
        humidity: 20
        perceivedTemperature: 2.6
        pressure: 10
        rainVolumeLastHour: 0
        temperature: 3.2
        time: "14:14:45"
        windDirectionDegrees: 90
        windGust: 2.4
        windSpeed: 3.5*/
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
    /*description: "Cloudy"
        humidity: 20
        perceivedTemperature: 2.6
        pressure: 10
        rainVolumeLastHour: 0
        temperature: 3.2
        time: "14:14:45"
        windDirectionDegrees: 90
        windGust: 2.4
        windSpeed: 3.5*/
  }
  return finalArr;
}

initMap();

// Sync on any updates to the DB. THIS CODE RUNS EVERY TIME AN UPDATE OCCURS ON THE DB.
camRef.limitToLast(1).on("value", function (snapshot) {
  snapshot.forEach(function (childSnapshot) {
    const image = childSnapshot.val()["test"];
    console.log(image);
    document.getElementById("test").textContent = image;
  });
});
