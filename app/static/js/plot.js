L.Icon.Default.imagePath = "https://unpkg.com/leaflet@1.9.4/dist/images/";

// init map
const map = L.map("map").setView([55.933, -3.213], 12);

// add openstreetmap tiles
const openstreetmap = L.tileLayer(
    "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        maxZoom: 19,
        attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    },
);

openstreetmap.addTo(map);

// add ENU markers

const merchistonMarker = L.marker([55.933224, -3.213707], {
    title: "Merchiston Campus",
    opacity: 0.6,
});

const craiglockhartMarker = L.marker([55.9180155592521, -3.2395898093778936], {
    title: "Craiglockhart Campus",
    opacity: 0.6,
});

const sighthillMarker = L.marker([55.92494380523382, -3.288342812238246], {
    title: "Sighthill Campus",
    opacity: 0.6,
});

merchistonMarker.addTo(map);
craiglockhartMarker.addTo(map);
sighthillMarker.addTo(map);

let selectPoints = [];
let markers = [];
let selectionBox = null;

function drawMarkerForIndex(index) {
    const marker = L.marker(selectPoints[index], {
        draggable: true,
    });

    marker.on("dragend", (e) => {
        selectPoints[index] = [
            e.target.getLatLng().lat,
            e.target.getLatLng().lng,
        ];

        if (selectionBox) {
            map.removeLayer(selectionBox);
            selectionBox = null;
        }

        drawSelection();
    });

    marker.addTo(map);
    markers.push(marker);
}

function drawSelection() {
    // Draw the selection box
    if (selectPoints[0] && selectPoints[1] && !selectionBox) {
        const bounds = L.latLngBounds(selectPoints[0], selectPoints[1]);

        selectionBox = L.rectangle(bounds, {
            color: "#ff7800",
            weight: 1,
        });

        selectionBox.addTo(map);
    }

    // Draw the markers
    if (selectPoints[0] && !markers[0]) {
        drawMarkerForIndex(0);
    }
    if (selectPoints[1] && !markers[1]) {
        drawMarkerForIndex(1);
    }
}

// Clear the selection
function clearSelection() {
    selectPoints = [];

    markers.forEach((marker) => map.removeLayer(marker));
    markers = [];

    if (selectionBox) {
        map.removeLayer(selectionBox);
        selectionBox = null;
    }
}

// Bind the map click event
map.on("click", (e) => {
    if (selectPoints.length >= 2) {
        return;
    }

    selectPoints.push([e.latlng.lat, e.latlng.lng]);

    drawSelection();
});

// Bind the clear selection button
const clearSelectionButton = L.easyButton("<img src='/static/Images/Icons/BinIcon.svg' />", () => {
    clearSelection();
});

clearSelectionButton.addTo(map);

// Mock the form submission

const submitButton = document.getElementById("submit-button");

submitButton.addEventListener("click", () => {
    if (selectPoints.length !== 2) {
        alert("Please select two points on the map");
        return;
    }

    const formElement = document.createElement("form");
    formElement.style.display = "none";
    formElement.method = "POST";
    formElement.action = "/wizard/plot";

    const longInput = document.createElement("input");
    longInput.name = "long";
    longInput.value = selectPoints[0][1].toString();
    formElement.appendChild(longInput);

    const latInput = document.createElement("input");
    latInput.name = "lat";
    latInput.value = selectPoints[0][0].toString();
    formElement.appendChild(latInput);

    const longInput2 = document.createElement("input");
    longInput2.name = "long2";
    longInput2.value = selectPoints[1][1].toString();
    formElement.appendChild(longInput2);

    const latInput2 = document.createElement("input");
    latInput2.name = "lat2";
    latInput2.value = selectPoints[1][0].toString();
    formElement.appendChild(latInput2);

    document.body.appendChild(formElement);

    formElement.submit();
});
