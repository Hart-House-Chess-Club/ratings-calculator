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