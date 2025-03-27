function initializeListControls(options = {}) {
  const {
    tableId = 'dataTable',
    filterFormId = 'filterForm',
    searchFormId = 'searchForm',
  } = options;

  // Initialize filter form
  const filterForm = document.getElementById(filterFormId);
  if (filterForm) {
    filterForm.addEventListener('change', () => {
      filterForm.submit();
    });
  }

  // Initialize search form
  const searchForm = document.getElementById(searchFormId);
  if (searchForm) {
    // Add debounce for search
    let timeout = null;
    const searchInput = searchForm.querySelector('input[type="search"]');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
          searchForm.submit();
        }, 300);
      });
    }
  }
}

// Wait for jQuery to be loaded
window.addEventListener('load', function() {
    if (typeof jQuery === 'undefined') {
        console.error('jQuery is not loaded!');
        return;
    }

    // Sorting functionality
    function initializeSorting() {
        $('.sortable').each(function() {
            var $th = $(this);
            var $table = $th.closest('table');
            var $tbody = $table.find('tbody');
            var columnIndex = $th.index();

            $th.on('click', function() {
                var isAsc = !$th.hasClass('sort-asc');
                
                // Remove sort classes from all headers
                $table.find('th').removeClass('sort-asc sort-desc');
                
                // Add sort class to current header
                $th.addClass(isAsc ? 'sort-asc' : 'sort-desc');
                
                // Get all rows and sort them
                var rows = $tbody.find('tr').get();
                rows.sort(function(a, b) {
                    var $aCell = $(a).children('td').eq(columnIndex);
                    var $bCell = $(b).children('td').eq(columnIndex);
                    var aText = $aCell.text().trim();
                    var bText = $bCell.text().trim();
                    
                    // Try to compare as numbers first
                    var aNum = parseFloat(aText);
                    var bNum = parseFloat(bText);
                    if (!isNaN(aNum) && !isNaN(bNum)) {
                        return isAsc ? aNum - bNum : bNum - aNum;
                    }
                    
                    // Fall back to string comparison
                    return isAsc ? 
                        aText.localeCompare(bText) : 
                        bText.localeCompare(aText);
                });
                
                // Reattach sorted rows
                $tbody.empty();
                $.each(rows, function(i, row) {
                    $tbody.append(row);
                });
            });
        });
    }

    // Initialize when DOM is loaded
    $(document).ready(function() {
        console.log('Initializing sorting...');
        initializeSorting();
        initializeListControls();
    });

    // Reinitialize when switching tabs
    $(document).on('shown.bs.tab', 'a[data-toggle="tab"]', function() {
        console.log('Tab switched, reinitializing sorting...');
        initializeSorting();
        initializeListControls();
    });
});
