var lat = document.getElementById("lat");
var lng = document.getElementById("lng");

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  lat.value=position.coords.latitude;
  lng.value=position.coords.longitude;
}