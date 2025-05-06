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