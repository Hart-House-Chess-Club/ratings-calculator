document.getElementById('fetch-btn').onclick = async function() {
    const output = document.getElementById('output');
    output.textContent = 'Loading...';
    try {
        const response = await fetch('http://127.0.0.1:5000/api/data');
        const data = await response.json();
        output.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        output.textContent = 'Error fetching data: ' + err;
    }
};

document.getElementById('predict-form').onsubmit = async function(e) {
    e.preventDefault();
    const output = document.getElementById('output');
    output.textContent = 'Loading...';

    const form = e.target;
    const formData = new FormData(form);

    // Parse ratings_list as an array of numbers
    const ratings_list = formData.get('ratings_list')
        .split(',')
        .map(s => parseInt(s.trim()))
        .filter(n => !isNaN(n));

    const payload = {
        cfc_id: parseInt(formData.get('cfc_id')),
        n_games: parseInt(formData.get('n_games')),
        ratings_list: ratings_list,
        wins: parseInt(formData.get('wins')),
        losses: parseInt(formData.get('losses')),
        draws: parseInt(formData.get('draws')),
        current_rating: parseInt(formData.get('current_rating')),
        all_time_high: parseInt(formData.get('all_time_high')),
        rating_type: parseInt(formData.get('rating_type')),
        quick_tourney: parseInt(formData.get('quick_tourney'))
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/api/predict_rating', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        output.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        output.textContent = 'Error fetching data: ' + err;
    }
};

document.getElementById('plot-btn').onclick = async function() {
    const cfc_id = document.getElementById('cfc_id').value;

    const chartDiv = document.getElementById('chart');
    chartDiv.innerHTML = "Loading...";

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/user_ratings_over_time?cfc_id=${cfc_id}`);
        const data = await response.json();

        if (data.error) {
            chartDiv.innerHTML = data.error;
            return;
        }

        // Combine and parse dates
        const parseDate = d3.timeParse("%Y-%m-%d");
        const regular = data.regular.map(d => ({...d, date: parseDate(d.date)}));
        const quick = data.quick.map(d => ({...d, date: parseDate(d.date)}));

        // Set up SVG
        chartDiv.innerHTML = "";
        const width = 700, height = 400, margin = {top: 30, right: 30, bottom: 50, left: 60};
        const svg = d3.select("#chart")
            .append("svg")
            .attr("width", width)
            .attr("height", height);

        // Combine for scales
        const allData = regular.concat(quick);
        const x = d3.scaleTime()
            .domain(d3.extent(allData, d => d.date))
            .range([margin.left, width - margin.right]);
        const y = d3.scaleLinear()
            .domain([d3.min(allData, d => d.rating_after) - 50, d3.max(allData, d => d.rating_after) + 50])
            .range([height - margin.bottom, margin.top]);

        // Axes
        svg.append("g")
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(x));
        svg.append("g")
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y));

        // Line generators
        const line = d3.line()
            .x(d => x(d.date))
            .y(d => y(d.rating_after));

        // Plot regular
        svg.append("path")
            .datum(regular)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 2)
            .attr("d", line);

        // Plot quick
        svg.append("path")
            .datum(quick)
            .attr("fill", "none")
            .attr("stroke", "orange")
            .attr("stroke-width", 2)
            .attr("d", line);

        // Add legend
        svg.append("circle").attr("cx",width-120).attr("cy",40).attr("r",6).style("fill","steelblue");
        svg.append("text").attr("x", width-110).attr("y", 45).text("Regular").style("font-size","15px").attr("alignment-baseline","middle");
        svg.append("circle").attr("cx",width-120).attr("cy",60).attr("r",6).style("fill","orange");
        svg.append("text").attr("x", width-110).attr("y", 65).text("Quick").style("font-size","15px").attr("alignment-baseline","middle");

        // Axis labels
        svg.append("text")
            .attr("text-anchor", "end")
            .attr("x", width/2)
            .attr("y", height - 10)
            .text("Date");
        svg.append("text")
            .attr("text-anchor", "end")
            .attr("transform", "rotate(-90)")
            .attr("y", 20)
            .attr("x", -height/2 + 40)
            .text("CFC Rating");

    } catch (err) {
        chartDiv.innerHTML = "Error loading chart: " + err;
    }
};