const graphDiv = document.getElementById("graph");
const button = document.getElementById("but");

fetch(
    "localhost:5000/data?name="+ button.value //use "http://localhost:3000" if running sample express backend locally, or replace with your own backend endpoint url
).then(async res => {
    dx = []
    dy = []
    dt = []
    json = res.json()
    for(let i = 0; i < json.length; i ++){
        dx.push(json[i][1])
        dy.push(json[i][0])
        dt.push(json[i][2])
    }
    Plotly.plot('graph',[{
        mode:"text",
        x: dx,
        y: dy,
        text: dt,
        font: {
            size: 1
        }

    }]); 
})

