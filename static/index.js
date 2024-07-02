document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');

    function search() {
        const query = searchInput.value;
        fetch('/search?q=' + encodeURIComponent(query))
            .then(response => response.json())
            .then(data => {
                const resultsDiv = document.getElementById('results');
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

    searchButton.addEventListener('click', search);

    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            search();
        }
    });
});
