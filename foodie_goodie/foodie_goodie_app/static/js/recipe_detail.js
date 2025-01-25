var countStars = function () {
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var checkedRadio = document.querySelector('.stars input:checked');
    const starValue = checkedRadio ? checkedRadio.value : null;
    
    if (starValue!=null && starValue!=0) {
        // Wykonaj POST na URL z `/stars`
        fetch(window.location.href + "stars", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken, // Dodaj CSRF token do nagłówka
            },
            body: JSON.stringify({ rating: starValue }), // Prześlij ocenę w treści
        }).then(response => response.json())
        .then(data => window.location.href = window.location.href.replace('/stars', '') )
     }
    };

    document.querySelector('.stars').addEventListener('click', countStars)


function printContent() {
    // Pobieramy zawartość kontenera
    var content = document.getElementById("main-content").innerHTML;

    // Pobieramy zawartość całej strony
    var originalContent = document.body.innerHTML;

    // Ścieżka do CSS
    var cssPath = "{% static 'css/style.css' %}";

    // Tworzymy tymczasowy widok z CSS
    document.body.innerHTML = `
        <html>
            <head>
                <title>Drukowanie</title>
                <link rel="stylesheet" type="text/css" href="${cssPath}">
            </head>
            <body>${content}</body>
        </html>
    `;

    // Uruchamiamy drukowanie
    window.print();

    // Przywracamy oryginalną zawartość strony
    document.body.innerHTML = originalContent;

    // Opcjonalnie, odświeżamy skrypty i CSS
    location.reload();
}