let lastSortedColumn = null;
let isAscending = true;

function sortTable(table, column) {
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll("tr"));

    // Toggle sort direction if clicking the same column
    if (lastSortedColumn === column) {
        isAscending = !isAscending;
    } else {
        isAscending = true;
        lastSortedColumn = column;
    }

    const dirModifier = isAscending ? 1 : -1;

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

    // Update sort indicators
    const headers = table.querySelectorAll("th");
    headers.forEach((header, index) => {
        header.classList.remove("sort-asc", "sort-desc");
        if (index === column) {
            header.classList.add(isAscending ? "sort-asc" : "sort-desc");
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    const tables = document.querySelectorAll("table.table-striped");
    
    tables.forEach(table => {
        const headers = table.querySelectorAll("th");
        headers.forEach((header, index) => {
            if (!header.classList.contains('no-sort')) {
                header.classList.add('sortable');
                // Remove any existing click listeners
                header.replaceWith(header.cloneNode(true));
                
                // Add new click listener
                table.querySelector(`th:nth-child(${index + 1})`).addEventListener("click", () => {
                    sortTable(table, index);
                });
            }
        });
    });
});
