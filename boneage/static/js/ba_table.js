function sortTable(columnIndex) {
    const table = document.getElementById("sortable-table");
    const rows = Array.from(table.rows).slice(2); // Skip header and filter rows
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
    const genderFilter = document.getElementById("gender-filter").value;
    const table = document.getElementById("sortable-table");
    const rows = table.getElementsByTagName("tr");

    for (let i = 2; i < rows.length; i++) { // Skip header and filter rows
        const genderCell = rows[i].getElementsByTagName("td")[1];
        if (genderCell) {
            const genderText = genderCell.textContent || genderCell.innerText;
            rows[i].style.display = (genderText.indexOf(genderFilter) > -1 || genderFilter === "") ? "" : "none";
        }
    }
}