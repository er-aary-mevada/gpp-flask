function sortTable(table, column, asc = true) {
    const dirModifier = asc ? 1 : -1;
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll("tr"));

    // Sort rows
    const sortedRows = rows.sort((a, b) => {
        const aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
        const bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim();

        // Check if the content is a number
        const aNum = parseFloat(aColText.replace(/[^0-9.-]+/g,""));
        const bNum = parseFloat(bColText.replace(/[^0-9.-]+/g,""));
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return (aNum - bNum) * dirModifier;
        }
        
        return aColText.localeCompare(bColText) * dirModifier;
    });

    // Remove existing rows
    while (tBody.firstChild) {
        tBody.removeChild(tBody.firstChild);
    }

    // Add sorted rows
    tBody.append(...sortedRows);

    // Remember how the column is currently sorted
    table.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc", "th-sort-desc"));
    table.querySelector(`th:nth-child(${column + 1})`).classList.toggle("th-sort-asc", asc);
    table.querySelector(`th:nth-child(${column + 1})`).classList.toggle("th-sort-desc", !asc);
}

document.addEventListener("DOMContentLoaded", function() {
    const tables = document.querySelectorAll("table.table-striped");
    
    tables.forEach(table => {
        const headers = table.querySelectorAll("th");
        headers.forEach((header, index) => {
            if (!header.classList.contains('no-sort')) {
                header.classList.add('sortable');
                header.addEventListener("click", () => {
                    const currentIsAsc = header.classList.contains("th-sort-asc");
                    sortTable(table, index, !currentIsAsc);
                });
            }
        });
    });
});
