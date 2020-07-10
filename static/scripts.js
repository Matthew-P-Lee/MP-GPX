var lat = document.getElementById("lat");
var lng = document.getElementById("lng");

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    lat.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  lat.value=position.coords.latitude;
  lng.value=position.coords.longitude;
}

function submitLocation() {
	if (lat.value.length == 0) {
		getLocation();
		btnLocation.className="btn btn-success";
		btnLocation.innerHTML="Download GPX File!";
	}
	else
	{
		document.forms['location'].submit();
	}
}