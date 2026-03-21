
document.getElementById('btn-predict').addEventListener("click", async () => {

    const btn = document.getElementById("btn-predict");
    const btnTxt = document.getElementById("btnTxt");

    // 🔹 Show loading state
    btnTxt.innerText = "Calculating...";
    btn.disabled = true;

    // read values 
    const mileage = parseInt(document.getElementById('mileage').value);
    const carAge = parseInt(document.getElementById('carAge').value);
    const engine = parseFloat(document.getElementById('engine').value);
    const maxPower = parseFloat(document.getElementById('maxPower').value);
    const torque = parseFloat(document.getElementById('torque').value);
    const km_driven_per_year = parseFloat(document.getElementById('DrivenDistance').value);
    const fuel = document.getElementById('fueltype').value;
    const transmission = document.getElementById('transmission').value;
    const owner = document.getElementById('NumOfOwner').value;


    // Build payload
    const payload = {
        mileage: mileage,
        engine: engine,
        max_power: maxPower,
        torque: torque,
        km_driven_per_year: km_driven_per_year,
        car_age: carAge,
        fuel: fuel,
        transmission: transmission,
        owner: owner
    };

    // 3 call API
    try {
        const response = await fetch("/predict-car", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });


        // 4 read response
        const data = await response.json();

        if (!response.ok) {
            throw new Error("API error");
        }

        // 5 update UI
        document.getElementById("resultPrice").innerText =
            "Estimated Car Price: \n$" + Number(data.Prediction).toLocaleString();

        document.getElementById("resultCard").classList.add("visible");
    }

    catch (error) {
        console.error(error);
        alert("Prediction failed. Please try again.");
    }

    // 🔹 Restore button
    btnTxt.innerText = "Estimate Price →";
    btn.disabled = false;

})


// console.log(mileage)