function sortTable(columnIndex) {
    const table = document.getElementById("sortable-table");
    const rows = Array.from(table.rows).slice(2); // Adjusted to skip filter row
    const isAscending = table.rows[0].cells[columnIndex].getAttribute('data-order') === 'asc';

    rows.sort((a, b) => {
        const cellA = a.cells[columnIndex].innerText;
        const cellB = b.cells[columnIndex].innerText;
        if (cellA < cellB) {
            return isAscending ? -1 : 1;
        }
        if (cellA > cellB) {
            return isAscending ? 1 : -1;
        }
        return 0;
    });

    table.tBodies[0].append(...rows);

    // Toggle the order attribute
    table.rows[0].cells[columnIndex].setAttribute('data-order', isAscending ? 'desc' : 'asc');
}

function filterTable() {
    const nameFilter = document.getElementById("name-filter").value.toUpperCase();
    const ageFilter = document.getElementById("age-filter").value.toUpperCase();
    const cityFilter = document.getElementById("city-filter").value.toUpperCase();
    const table = document.getElementById("sortable-table");
    const rows = table.getElementsByTagName("tr");

    for (let i = 2; i < rows.length; i++) { // Adjusted to skip filter row
        let nameCell = rows[i].getElementsByTagName("td")[0];
        let ageCell = rows[i].getElementsByTagName("td")[1];
        let cityCell = rows[i].getElementsByTagName("td")[2];
        
        if (nameCell && ageCell && cityCell) {
            const nameText = nameCell.textContent || nameCell.innerText;
            const ageText = ageCell.textContent || ageCell.innerText;
            const cityText = cityCell.textContent || cityCell.innerText;
            
            rows[i].style.display = (nameText.toUpperCase().indexOf(nameFilter) > -1 || nameFilter === "") &&
                                    (ageText.toUpperCase().indexOf(ageFilter) > -1 || ageFilter === "") &&
                                    (cityText.toUpperCase().indexOf(cityFilter) > -1 || cityFilter === "") 
                                    ? "" : "none";
        }
    }
}