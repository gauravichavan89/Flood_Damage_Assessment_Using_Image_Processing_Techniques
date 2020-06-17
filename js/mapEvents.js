var province = provinceData;
var country = countryData;
var map;
var geocoder;
var centerOfBound;
mapboxgl.accessToken = 'pk.eyJ1IjoiaGFyaW5paGFyaWhhcmFrcmlzaG5hbiIsImEiOiJjanBkb3VjdWcza2ZnM2tvYnI1bHY3MjZ5In0.QzZDc-P0Nfz8XRFrtHzY_w';
var callLayerOnce = true;
var circlemarker;
var rectangle;
var drawingManager;
var bounds;
var start;
var end;
var BoundEnds = [{"position":"topright","lat":0.0,"lng":0.0},{"position":"topleft","lat":0.0,"lng":0.0},{"position":"bottomright","lat":0.0,"lng":0.0},{"position":"bottomleft","lat":0.0,"lng":0.0}];
var BoundEndsStreet = [{"position":"topright","lat":0.0,"lng":0.0},{"position":"topleft","lat":0.0,"lng":0.0},{"position":"bottomright","lat":0.0,"lng":0.0},{"position":"bottomleft","lat":0.0,"lng":0.0}];
var orgImgUrl ;
var boundedImgUrl;
var metersPerPxSat;
var geocoder;
var panorama;
var csvData = [{"centerlat":0.0,"centerlng":0.0,"address" :"","earthsimple":"","earthbounded":"","earthmeasure":0.0,"streetsimple":"","streetbounded":"","streetmeasure":0.0}];
var streetOrgImg;

document.addEventListener('DOMContentLoaded', function () {
  if (document.querySelectorAll('#googleMap').length > 0)
  {
    if (document.querySelector('html').lang)
      lang = document.querySelector('html').lang;
    else
      lang = 'en';

    var js_file = document.createElement('script');
    js_file.type = 'text/javascript';
    js_file.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAPq2rYTkerwHOhewlVUkhmdakPWDunh3Q&libraries=drawing&callback=initMap&language=' + lang;
    document.getElementsByTagName('head')[0].appendChild(js_file);
  }
});

function initMap()
{
	map = new google.maps.Map(document.getElementById('googleMap'), {zoom: 4});
	map.setCenter(country.geometry.location);
}

function registerMapEvents(){
	$(document).on('change','#provinceSelect', function () {
		var value = $(this).val();
		loadThisProvince(value);
	});
}

function loadThisProvince(provinceValue) {
	if(provinceValue == "None") {
		map.setCenter({lat:country.geometry.location.lat, lng:country.geometry.location.lng});
		map.setZoom(country.zoom);
		map.setMapTypeId('terrain');
		$("#markerGroup").addClass("displayNone");
	} else {
		$("#markerGroup").removeClass("displayNone");
		var filterednames = province.filter(function(obj) {
			return (obj.long_name === provinceValue);
		});
		map.setCenter({lat:filterednames[0].geometry.location.lat, lng:filterednames[0].geometry.location.lng});
		map.setZoom(filterednames[0].zoom);
		map.setMapTypeId('hybrid');
	}
}

function drawRec() {
	drawingManager = new google.maps.drawing.DrawingManager();
	if (!!rectangle && !!rectangle.overlay && !!rectangle.overlay.setMap) {
		rectangle.overlay.setMap(null);
	  }
	  drawingManager.setOptions({
		drawingMode: google.maps.drawing.OverlayType.RECTANGLE,
		drawingControl: false,
		drawingControlOptions: {
		  position: google.maps.ControlPosition.TOP_CENTER,
		  drawingModes: [google.maps.drawing.OverlayType.RECTANGLE]
		},
		rectangleOptions: {
		  strokeColor: '#000000',
		  strokeWeight: 3.5,
		  fillColor: '#000000',
		  fillOpacity: 1.0,
		  editable: true,
		  draggable: true
		}
	});
	drawingManager.setMap(map);
	google.maps.event.addListener(drawingManager, 'overlaycomplete', function(overlay) {
		  rectangle = overlay;
		  drawingManager.setOptions({
			drawingMode: null,
			drawingControl: false
		  });
		bounds = overlay.overlay.getBounds();
		start = bounds.getNorthEast();
		end = bounds.getSouthWest();
		tr = BoundEnds.filter(function(v){ 
				if(v["position"] == "topright") {
					v.lat = start.lat();
					v.lng = start.lng();
					return v;
				}
			});
		bl = BoundEnds.filter(function(v){ 
				if(v["position"] == "bottomleft") {
					v.lat = end.lat();
					v.lng = end.lng();
					return v;
				}
			});
		tl = BoundEnds.filter(function(v){ 
				if(v["position"] == "topleft") {
					v.lat = start.lat();
					v.lng = end.lng();
					return v;
				}
			});
		br = BoundEnds.filter(function(v){ 
				if(v["position"] == "bottomright") {
					v.lat = end.lat();
					v.lng = start.lng();
					return v;
				}
			});		
		console.log(start.toUrlValue(6));
	});
}

function drawRecStreet() {
	drawingManager = new google.maps.drawing.DrawingManager();
	if (!!rectangle && !!rectangle.overlay && !!rectangle.overlay.setMap) {
		rectangle.overlay.setMap(null);
	  }
	  drawingManager.setOptions({
		drawingMode: google.maps.drawing.OverlayType.RECTANGLE,
		drawingControl: false,
		drawingControlOptions: {
		  position: google.maps.ControlPosition.TOP_CENTER,
		  drawingModes: [google.maps.drawing.OverlayType.RECTANGLE]
		},
		rectangleOptions: {
		  strokeColor: '#000000',
		  strokeWeight: 3.5,
		  fillColor: '#000000',
		  fillOpacity: 1.0,
		  editable: true,
		  draggable: true
		}
	});
	drawingManager.setMap(panorama);
	google.maps.event.addListener(drawingManager, 'overlaycomplete', function(overlay) {
		  rectangle = overlay;
		  drawingManager.setOptions({
			drawingMode: null,
			drawingControl: false
		  });
		bounds = overlay.overlay.getBounds();
		start = bounds.getNorthEast();
		end = bounds.getSouthWest();
		trs = BoundEndsStreet.filter(function(v){ 
				if(v["position"] == "topright") {
					v.lat = start.lat();
					v.lng = start.lng();
					return v;
				}
			});
		bls = BoundEndsStreet.filter(function(v){ 
				if(v["position"] == "bottomleft") {
					v.lat = end.lat();
					v.lng = end.lng();
					return v;
				}
			});
		tls = BoundEndsStreet.filter(function(v){ 
				if(v["position"] == "topleft") {
					v.lat = start.lat();
					v.lng = end.lng();
					return v;
				}
			});
		brs = BoundEndsStreet.filter(function(v){ 
		if(v["position"] == "bottomright") {
					v.lat = end.lat();
					v.lng = start.lng();
					return v;
				}
			});		
		console.log(start.toUrlValue(6));
	});
}

function Export() 
{          
	var staticMapUrl = "https://maps.googleapis.com/maps/api/staticmap"; 
	//Set the Google Map Center.
	var bounds = new google.maps.LatLngBounds();
	var i;
	tr = BoundEnds.filter(function(v){ 
			if(v["position"] == "topright") {
				return v;
			}
		});
	bl = BoundEnds.filter(function(v){ 
			if(v["position"] == "bottomleft") {
				return v;
			}
		});
	tl = BoundEnds.filter(function(v){ 
			if(v["position"] == "topleft") {
				return v;
			}
		});
	br = BoundEnds.filter(function(v){ 
			if(v["position"] == "bottomright") {
				return v;
			}
		});	
	var polygonCoords = [
	  new google.maps.LatLng(tr[0].lat, tr[0].lng),
	  new google.maps.LatLng(br[0].lat, br[0].lng),
	  new google.maps.LatLng(bl[0].lat, bl[0].lng),
	  new google.maps.LatLng(tl[0].lat, tl[0].lng)
	];

	for (i = 0; i < polygonCoords.length; i++) {
	  bounds.extend(polygonCoords[i]);
	}
	console.log(bounds.getCenter());
	staticMapUrl += "?center=" + bounds.getCenter().lat() + "," +bounds.getCenter().lng();
	staticMapUrl += "&size="+$("#googleMap").width()+"x"+$("#googleMap").height(); 
	staticMapUrl += "&zoom=" + map.getZoom();
	staticMapUrl += "&style=visibility:on";  
	staticMapUrl += "&key=AIzaSyAPq2rYTkerwHOhewlVUkhmdakPWDunh3Q";	
	staticMapUrl += "&maptype=" + map.getMapTypeId();
	var canvas=document.createElement('canvas');
	var context = canvas.getContext('2d');
	var imageObj = new Image();
	imageObj.crossOrigin = "crossOrigin";
	imageObj.onload = function() {
		canvas.width=imageObj.width;
		canvas.height=imageObj.height;
		context.drawImage(imageObj, 0, 0,imageObj.width,imageObj.height);
		var dataurl=canvas.toDataURL('image/png');
		var imgMap = document.getElementById("imgMap");
		imgMap.src = dataurl;        
	};
	orgImgUrl = staticMapUrl;
	staticMapUrl += "&path=color:0xFFFFFFFF|weight:5|fillcolor:0xFFFFFFFF|";
	staticMapUrl += tr[0].lat + ","+ tr[0].lng + "|";
	staticMapUrl += br[0].lat + "," +br[0].lng + "|";
	staticMapUrl += bl[0].lat + ","+ bl[0].lng + "|";
	staticMapUrl += tl[0].lat + "," +tl[0].lng;
	boundedImgUrl = staticMapUrl;
	console.log("Original : " + orgImgUrl);
	console.log("Bounded : " + boundedImgUrl);
	metersPerPxSat = 156543.03392 * Math.cos(map.getCenter().lat() * Math.PI / 180) / Math.pow(2, map.getZoom());
	//Setting CSV data
	csvData[0].centerlat = bounds.getCenter().lat();
	csvData[0].centerlng = bounds.getCenter().lng();
	csvData[0].earthsimple = "\"" + orgImgUrl+ "\"";
	csvData[0].earthbounded = "\"" + boundedImgUrl+ "\"";
	csvData[0].earthmeasure = metersPerPxSat;
	geocoder = new google.maps.Geocoder();
	geocoder.geocode({
		'latLng': bounds.getCenter()
		}, function (results, status) {
			if (status ==
				google.maps.GeocoderStatus.OK) {
				if (results[1]) {
					csvData[0].address = "\"" + results[1].formatted_address+ "\"";
				} else {
					alert('No results found');
				}
			} else {
				alert('Geocoder failed due to: ' + status);
			}
	});
}

function ExportStreet() 
{          
	var staticMapUrl = "https://maps.googleapis.com/maps/api/streetview"; 
	//Set the Google Map Center.
	var bounds = new google.maps.LatLngBounds();
	var i;
	staticMapUrl += "?location=" + panorama.getPosition().lat() + "," +panorama.getPosition().lng();
	staticMapUrl += "&size="+$("#googleMap").width()+"x"+$("#googleMap").height(); 
	staticMapUrl += "&heading=0&pitch=0&fov=90";	
	staticMapUrl += "&key=AIzaSyAPq2rYTkerwHOhewlVUkhmdakPWDunh3Q";	
	streetOrgImg = staticMapUrl;
	console.log("streetOrgImg : " + streetOrgImg);
	csvData[0].streetsimple = "\"" + streetOrgImg+ "\"";
}

function convertArrayOfObjectsToCSV(args) {
	var result, ctr, keys, columnDelimiter, lineDelimiter, data;
	data = args.data || null;
	if (data == null || !data.length) {
		return null;
	}
	columnDelimiter = args.columnDelimiter || ',';
	lineDelimiter = args.lineDelimiter || '\n';
	keys = Object.keys(data[0]);
	result = '';
	result += keys.join(columnDelimiter);
	result += lineDelimiter;
	data.forEach(function(item) {
		ctr = 0;
		keys.forEach(function(key) {
			if (ctr > 0) result += columnDelimiter;
			result += item[key];
			ctr++;
		});
		result += lineDelimiter;
	});
	return result;
}

function downloadCSV(args) {
	var data, filename, link;
	var csv = convertArrayOfObjectsToCSV({
		data: csvData
	});
	if (csv == null) return;
	filename = args.filename || 'export.csv';
	if (!csv.match(/^data:text\/csv/i)) {
		csv = 'data:text/csv;charset=utf-8,' + csv;
	}
	data = encodeURI(csv);
	link = document.createElement('a');
	link.setAttribute('href', data);
	link.setAttribute('download', filename);
	link.click();
}

function loadStreetView(){
	$("#googleMap").empty();
	myLatLng = new google.maps.LatLng({lat: csvData[0].centerlat, lng: csvData[0].centerlng})
	var heading = google.maps.geometry.spherical.computeHeading(myLatLng,myLatLng)
	panorama = new google.maps.StreetViewPanorama(
	document.getElementById('googleMap'),
	{
	  position: {lat: csvData[0].centerlat, lng: csvData[0].centerlng},
	  pov: {heading: 100, pitch: 0},
	  zoom: 1
	});
	panorama.setPov({"heading":heading,"pitch":0})
}

