document$.subscribe(() => {
  const $table = $('#rankTable');
  if (!$table.length || $table.hasClass('dataTable')) {
    return; // Table not present or already initialized
  }

  const dt = $table.DataTable({
    paging:    false,
    info:      true,
    ordering:  true,
    searching: true,

    searchPanes: {
      columns: [1, 2, 3], 
      viewTotal: true
    },

    dom: 'Pfrt',
    columnDefs: [
      { targets: [1, 2], visible: false, searchable: true },
      {
        targets: [3, 4, 5, 6, 7, 8, 9],
        render: function (data, type) {
            if (type === 'sort' || type === 'type') {
                const match = data.match(/\((\d+)\)/); 
                return match ? parseInt(match[1], 10) : Infinity;
            }
            return data;
        }
    },
    {
      targets: 9,
      className: 'fw-semibold',
    }    
    ],
    order: [[9, 'asc']],
    language: {
      search: '_INPUT_',
      searchPlaceholder: 'Search models…'
    },
  });

  // ─── Highlight top-3 rows with podium colours ───────────────────────
  function paintWinners() {
    // clear any previous podium colours
    dt.rows().nodes().to$().removeClass('winner-gold winner-silver winner-bronze');

    // Get the current sort direction (ascending or descending)
    const sortOrder = dt.order();
    const isDescending = sortOrder[0][1] === 'desc';  // Check if it's descending

    var rows = dt.rows({ order: 'applied', search: 'applied' }).indexes().toArray();

    rows = rows.sort((a, b) => {
      const extractRank = (str) => {
          const match = str.match(/\((\d+)\)/); // Match number inside parentheses
          return match ? parseInt(match[1], 10) : Infinity; // Use Infinity if not found
      };
  
      const valueA = extractRank(dt.cell(a, 9).data());
      const valueB = extractRank(dt.cell(b, 9).data());
  
      return !isDescending ? valueB - valueA : valueA - valueB;
  });
    if (isDescending)
      var top3 = rows.slice(0, 3);
      
    else {
      var top3 = rows.slice(rows.length - 3, rows.length);
      top3.reverse();
    }
    // Apply podium classes based on the sorted top 3 rows
    if (top3[0] !== undefined) $(dt.row(top3[0]).node()).addClass('winner-gold');
    if (top3[1] !== undefined) $(dt.row(top3[1]).node()).addClass('winner-silver');
    if (top3[2] !== undefined) $(dt.row(top3[2]).node()).addClass('winner-bronze');
  }

  paintWinners();

  dt.on('draw', paintWinners);

  $('.dtsp-titleRow').hide();
});
