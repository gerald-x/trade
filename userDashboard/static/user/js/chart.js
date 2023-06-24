import * as chartJs from 'https://cdn.jsdelivr.net/npm/chart.js@4.3.0/+esm';
import zoomPlugin from 'https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@2.0.1/+esm'

chartJs.Chart.register(...chartJs.registerables, zoomPlugin)

document.addEventListener("DOMContentLoaded", ()=>{
    // Get the canvas element
    const ctx = document.getElementById('myChart').getContext("2d");
    const balance = document.getElementById("balance");

    // Generate random data for demonstration
    const data = {
    labels: [],
    datasets: [{
        label: 'Profit/Loss on dummy stock',
        data: [],
        borderColor: 'rgba(0, 123, 255, 1)',
        tension: 0.1,
        fill: false,
    }]
    };


    // Configure the options for the chart
    const options = {
        responsive: true,
        hover: {
            mode: 'nearest',
            intersect: true
        },
        plugins: {
            zoom: {
                zoom: {
                    wheel: {
                        enabled: true // SET SCROOL ZOOM TO TRUE
                    },
                    pinch: {
                        enabled: true
                    },
                    mode: "x",
                    speed: 50,
                },
                pan: {
                    enabled: true,
                    mode: "x",
                    speed: 50,
                },
            }
        },
        scales: {
            x: {
                ticks: {
                    maxRotation: 75,
                    minRotation: 75, // Set the angle value to rotate the labels
                    maxRotation: 0,  // Set rotation to 0 to prevent label rotation
                    autoSkip: true,
                    maxTicksLimit: 10,  // Set the maximum number of labels to display
                },
            },
        },
    }

    const config = {
        type: 'line',
        data: data,
        options: options,
        plugins: [zoomPlugin]
    };

    // Create the chart
    const myChart = new chartJs.Chart(ctx, config);

    fetch(`${window.location.protocol}//${window.location.host}/dashboard/stock/records/`)
    .then(res=>res.json())
    .then(data => {
        for (let i = 0; i < data.length; i++) {
            console.log(data[i].current_value, data)
            // Push the new label and data to the respective arrays
            myChart.data.labels.push(new Date(data[i].time).toLocaleString('en-US', {
                day: 'numeric',
                month: 'short',
                year: 'numeric',
                hour: 'numeric',
                minute: 'numeric',
                hour12: false
              })
            );
            myChart.data.datasets[0].data.push(data[i].current_value);  
            balance.innerHTML = `$Balance: ${parseFloat(data[i].current_value).toFixed(2)}`;       
        }

        myChart.update();
    })


    setInterval(()=>{
        fetch(`${window.location.protocol}//${window.location.host}/dashboard/stock/records/`)
        .then(res=>res.json())
        .then(data => {
            const retrieved_time = data[data.length-1].time;
            const retrieved_value = data[data.length-1].current_value;

            const current_label = myChart.data.labels;
            const current_data =  myChart.data.datasets[0].data;

            const formattedDate = new Date(retrieved_time).toLocaleString('en-US', {
                day: 'numeric',
                month: 'short',
                year: 'numeric',
                hour: 'numeric',
                minute: 'numeric',
                hour12: false
            });

            if (formattedDate !== current_label[current_label.length-1] && current_data[current_data.length-1] !== retrieved_value) {
                // Push the new label and data to the respective arrays
                myChart.data.labels.push(new Date(retrieved_time).toLocaleString('en-US', {
                    day: 'numeric',
                    month: 'short',
                    year: 'numeric',
                    hour: 'numeric',
                    minute: 'numeric',
                    hour12: false
                    })
                );
                myChart.data.datasets[0].data.push(retrieved_value);
                myChart.update();
                balance.innerHTML = `$Balance: ${parseFloat(retrieved_value).toFixed(2)}`;       
            }
        })        
    }, 60000)

})
