document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const resultsDiv = document.getElementById('results');
    const suggestionsList = document.getElementById('suggestions');
    const anomaliesDiv = document.getElementById('anomalies');

    function search() {
        const query = searchInput.value;
        fetch('/search?q=' + encodeURIComponent(query))
            .then(response => response.json())
            .then(data => {
                resultsDiv.innerHTML = '';
                if (data.hits.length === 0) {
                    resultsDiv.innerHTML = '<p>No se encontraron resultados.</p>';
                } else {
                    data.hits.forEach(hit => {
                        resultsDiv.innerHTML += `
                            <div class="result-item">
                                <h3><a href="${hit.url}">${hit.title}</a></h3>
                                <p>${hit.content}</p>
                            </div>`;
                    });
                }
            });
    }

    function suggest() {
        const query = searchInput.value;
        fetch('/suggest?q=' + encodeURIComponent(query))
            .then(response => response.json())
            .then(data => {
                suggestionsList.innerHTML = '';
                data.forEach(suggestion => {
                    const optionElement = document.createElement('option');
                    optionElement.value = suggestion;
                    suggestionsList.appendChild(optionElement);
                });
            });
    }

    function loadAnomalies() {
        fetch('/anomalies')
            .then(response => response.json())
            .then(data => {
                anomaliesDiv.innerHTML = '';
                if (data.length === 0) {
                    anomaliesDiv.innerHTML = '<p>No se encontraron anomalías.</p>';
                } else {
                    data.forEach(anomaly => {
                        anomaliesDiv.innerHTML += `
                            <div class="anomaly-item">
                                <h3>Job ID: ${anomaly.job_id}</h3>
                                <p>Anomaly Score: ${anomaly.anomaly_score}</p>
                                <p>Timestamp: ${anomaly.timestamp}</p>
                            </div>`;
                    });
                }
            });
    }

    searchButton.addEventListener('click', search);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            search();
        }
    });
    searchInput.addEventListener('input', suggest);
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            e.preventDefault();
            if (suggestionsList.options.length > 0) {
                searchInput.value = suggestionsList.options[0].value;
                search();
            }
        }
    });
    suggestionsList.addEventListener('click', function(e) {
        if (e.target && e.target.nodeName === "OPTION") {
            searchInput.value = e.target.value;
            search();
        }
    });

    // Cargar anomalías al cargar la página
    loadAnomalies();
});
