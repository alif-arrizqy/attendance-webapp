const getHumidtyTomat = async (data) => {
    document.getElementById("valueHumidityTomat").innerHTML = data.data.value;
    document.getElementById("createdAtHumidityTomat").innerHTML =
        data.data.created_at;
};

const getTemperatureTomat = async (data) => {
    document.getElementById("valueTemperatureTomat").innerHTML = data.data.value;
    document.getElementById("createdAtTemperatureTomat").innerHTML =
        data.data.created_at;
};

const getMoistureTomat = async (data) => {
    document.getElementById("valueMoistureTomat").innerHTML = data.data.value;
    document.getElementById("createdAtMoistureTomat").innerHTML =
        data.data.created_at;
};

setInterval(() => {
    axios
        .get("http://localhost:5100/api/humidity/tomat", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getHumidtyTomat(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
    axios
        .get("http://localhost:5100/api/temperature/tomat", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getTemperatureTomat(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
    axios
        .get("http://localhost:5100/api/moisture/tomat", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getMoistureTomat(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
}, 5000)

setTimeout(() => {
    axios
        .get("http://localhost:5100/api/humidity/tomat", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getHumidtyTomat(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
    axios
        .get("http://localhost:5100/api/temperature/tomat", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getTemperatureTomat(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
    axios
        .get("http://localhost:5100/api/moisture/tomat", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getMoistureTomat(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
}, 3000);