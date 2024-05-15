const getHumidtyTerung = async (data) => {
    document.getElementById("valueHumidityTerung").innerHTML = data.data.value;
    document.getElementById("createdAtHumidityTerung").innerHTML =
        data.data.created_at;
};

const getTemperatureTerung = async (data) => {
    document.getElementById("valueTemperatureTerung").innerHTML = data.data.value;
    document.getElementById("createdAtTemperatureTerung").innerHTML =
        data.data.created_at;
};

const getMoistureTerung = async (data) => {
    document.getElementById("valueMoistureTerung").innerHTML = data.data.value;
    document.getElementById("createdAtMoistureTerung").innerHTML =
        data.data.created_at;
};

setInterval(() => {
    axios
        .get("http://localhost:5100/api/humidity/terung", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getHumidtyTerung(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
    axios
        .get("http://localhost:5100/api/temperature/terung", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getTemperatureTerung(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
    axios
        .get("http://localhost:5100/api/moisture/terung", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getMoistureTerung(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
}, 5000)

setTimeout(() => {
    axios
        .get("http://localhost:5100/api/humidity/terung", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getHumidtyTerung(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
    axios
        .get("http://localhost:5100/api/temperature/terung", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getTemperatureTerung(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
    axios
        .get("http://localhost:5100/api/moisture/terung", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getMoistureTerung(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
}, 3000);