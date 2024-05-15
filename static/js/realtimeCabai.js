const getHumidtyCabai = async (data) => {
    document.getElementById("valueHumidityCabai").innerHTML = data.data.value;
    document.getElementById("createdAtHumidityCabai").innerHTML =
        data.data.created_at;
};

const getTemperatureCabai = async (data) => {
    document.getElementById("valueTemperatureCabai").innerHTML = data.data.value;
    document.getElementById("createdAtTemperatureCabai").innerHTML =
        data.data.created_at;
};

const getMoistureCabai = async (data) => {
    document.getElementById("valueMoistureCabai").innerHTML = data.data.value;
    document.getElementById("createdAtMoistureCabai").innerHTML =
        data.data.created_at;
};

setInterval(() => {
    axios
        .get("http://localhost:5100/api/humidity/cabai", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getHumidtyCabai(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
    axios
        .get("http://localhost:5100/api/temperature/cabai", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getTemperatureCabai(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
    axios
        .get("http://localhost:5100/api/moisture/cabai", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getMoistureCabai(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
}, 5000)

setTimeout(() => {
    axios
        .get("http://localhost:5100/api/humidity/cabai", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getHumidtyCabai(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
    axios
        .get("http://localhost:5100/api/temperature/cabai", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getTemperatureCabai(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
    axios
        .get("http://localhost:5100/api/moisture/cabai", (timeout = 1000))
        .then((response) => {
            // console.log(response.data)
            getMoistureCabai(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
}, 3000);