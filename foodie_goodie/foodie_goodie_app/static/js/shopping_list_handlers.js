//add ingredient through ajax and api
document.getElementById('addListElementBtn').addEventListener('click', function () {
    let name = document.getElementById('listElementName').value;
    let amount = document.getElementById('listElementAmount').value;
    let unit = document.getElementById('listElementUnit').value;
    console.log(name, amount, unit);

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
            console.log("Data: ", data);
            let existingRow = document.querySelector(`tr[data-name="${data.list_element.nazwaElementu}"][data-unit="${data.list_element.jednostka}"]`);
            console.log(existingRow);
            if (existingRow) {
                console.log("Element już istnieje w DOM:", existingRow);
                let amountCell = existingRow.querySelector('.element-amount');
                amountCell.textContent = data.list_element.ilosc;
            } else {
                console.log("Element nie istnieje w DOM. Dodaję nowy wiersz.");
                let newRow = `<tr data-name="${data.list_element.nazwaElementu}" data-unit="${data.list_element.jednostka}">
                    <td>${data.list_element.nazwaElementu}</td>
                    <td class="element-amount">${data.list_element.ilosc}</td>
                    <td>${data.list_element.jednostka}</td>
                    <td>
                        <input type="checkbox" 
                           name="element_${data.list_element.idElement}" 
                           id="element_${data.list_element.idElement}" 
                           class="element-checkbox element-${data.list_element.idElement}">
                    </td>
                    <td><a href="#" class="delete-btn green-text" data-id="${data.list_element.idElement}">Usuń</a></td>
                </tr>`;
                document.querySelector("tbody").insertAdjacentHTML('beforeend', newRow);

                attachCheckboxListener(document.getElementById(`element_${data.list_element.idElement}`));
            }
        }
    })
    .catch(error => console.error("Błąd:", error));
});



//remove element from list
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
                event.target.closest('tr').remove();
            }
        })
        .catch(error => console.error("Błąd:", error));
    }
});



//checkbox update
function attachCheckboxListener(checkbox) {
    checkbox.addEventListener('change', function () {
        console.log("EEEE");
        let listElementId = this.getAttribute('id').split('_')[1];
        let isChecked = this.checked;
        console.log(listElementId, isChecked);

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


//in the beginning, iterate through all checkboxes and attach the listeners
document.querySelectorAll('.element-checkbox').forEach(checkbox => {
    attachCheckboxListener(checkbox);
});
