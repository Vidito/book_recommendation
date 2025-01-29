function getRecommendations() {
    let query = document.getElementById("query").value;
    let resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "<p>Loading recommendations...</p>";

    fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query })
    })
        .then(response => response.json())
        .then(data => {
            resultsDiv.innerHTML = "";

            if (data.error) {
                resultsDiv.innerHTML = `<p style="color:red">${data.error}</p>`;
                return;
            }

            data.forEach(book => {
                let bookDiv = document.createElement("article");
                bookDiv.className = "book";
                bookDiv.innerHTML = `<h3>${book.title}</h3><p><strong>Genre:</strong> ${book.genre}</p><p>${book.summary}</p>`;

                bookDiv.style.marginTop = "10px";

                resultsDiv.appendChild(bookDiv);
            });
        })
        .catch(error => {
            resultsDiv.innerHTML = "<p style='color:red'>Failed to fetch recommendations.</p>";
            console.error("Error:", error);
        });
}
