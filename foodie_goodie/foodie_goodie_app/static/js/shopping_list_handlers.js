//add egredient through ajax and api
document.getElementById('addListElementBtn').addEventListener('click', function () {
    let name = document.getElementById('listElementName').value;
    let amount = document.getElementById('listElementAmount').value;
    let unit = document.getElementById('listElementUnit').value;
    console.log(name, amount, unit);

    //validation
    if (!name || !amount || isNaN(amount) || amount <= 0) {
        alert("Proszę podać poprawne dane. Nazwa i ilość nie mogą być puste, a ilość musi być większa od 0.");
        return;
    }

    fetch(addListElementUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: JSON.stringify({
            nazwaElementu: name,
            ilosc: amount,
            jednostka: unit
        })
        
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(data);
            let newRow = `<tr>
                <td>${data.list_element.nazwaElementu}</td>
                <td>${data.list_element.ilosc}</td>
                <td>${data.list_element.jednostka}</td>
                <td>
                    <input type="checkbox" 
                       name="list_element_${data.list_element.idElement}" 
                       id="list_element_${data.list_element.idElement}" 
                       class="element-checkbox list-element-${data.list_element.idElement}">
                </td>
                <td><a href="#" class="delete-btn" data-id="${data.list_element.idElement}">Usuń</a></td>
            </tr>`;
            document.querySelector("tbody").insertAdjacentHTML('beforeend', newRow);

            // Dodanie obsługi checkboxa dla nowego elementu
            attachCheckboxListener(document.getElementById(`list_element_${data.list_element.idElement}`));
        }
    })
    .catch(error => console.error("Błąd:", error));
});

// Zdarzenie kliknięcia do usuwania elementów (delegacja zdarzeń)
document.querySelector("tbody").addEventListener('click', function (event) {
    if (event.target && event.target.classList.contains('delete-btn')) {
        event.preventDefault();
        let listElementId = event.target.getAttribute('data-id');
        console.log(listElementId);

        fetch(deleteListElementUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}"
            },
            body: JSON.stringify({ idElement: listElementId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                event.target.closest('tr').remove(); // Usuwamy wiersz
            }
        })
        .catch(error => console.error("Błąd:", error));
    }
});

// Funkcja do wysyłania AJAXa przy zaznaczaniu checkboxa
function attachCheckboxListener(checkbox) {
    checkbox.addEventListener('change', function () {
        let listElementId = this.getAttribute('id').split('_')[2];
        let isChecked = this.checked;

        fetch(updateListElementStatusUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}"
            },
            body: JSON.stringify({
                idElement: listElementId,
                zaznaczony: isChecked
            })
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert("Błąd podczas aktualizacji stanu elementu.");
            }
        })
        .catch(error => console.error("Błąd:", error));
    });
}

document.querySelectorAll('.list-element-checkbox').forEach(checkbox => {
    attachCheckboxListener(checkbox);
});
