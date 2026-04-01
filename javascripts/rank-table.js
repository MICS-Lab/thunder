document$.subscribe(() => {
    const tables = [

        {
            id: '#ranksumTableOriginal',
            rankCol: 9,
            radix: 10
        },

        {
            id: '#ranksumTableUpToDate',
            rankCol: 9,
            radix: 10
        },

        {
            id: '#spiderTable',
            rankCol: 12,
            radix: 10
        },

        {
            id: '#perDatasetLinearTable',
            rankCol: 19,
            radix: 10
        },

        {
            id: '#zeroshotTable',
            rankCol: 19,
            radix: 10
        },
    ];

    const range = (start, end) => Array.from({
        length: end - start + 1
    }, (_, i) => start + i);

    tables.forEach(cfg => {
        const $table = $(cfg.id);
        if (!$table.length || $table.hasClass('dataTable')) return;

        const renderCols = range(3, cfg.rankCol); // columns [3..rankCol]

        const dt = $table.DataTable({
            paging: false,
            info: true,
            ordering: true,
            searching: true,

            searchPanes: {
                columns: [1, 2, 3],
                viewTotal: true
            },

            dom: 'Pfrt',
            columnDefs: [{
                    targets: [1, 2],
                    visible: false,
                    searchable: true
                },
                {
                    targets: renderCols,
                    render: function(data, type) {
                        if (type === 'sort' || type === 'type') {
                            const match = String(data ?? '').match(/\((\d+)\)/);
                            return match ? parseInt(match[1], cfg.radix) : Infinity;
                        }
                        return data;
                    }
                },
                {
                    targets: cfg.rankCol,
                    className: 'fw-semibold'
                }
            ],
            order: [
                [cfg.rankCol, 'asc']
            ],
            language: {
                search: '_INPUT_',
                searchPlaceholder: 'Search models…'
            }
        });

        // ─── Highlight top-3 rows with podium colours ───────────────────────
        const paintWinners = () => {
            dt.rows().nodes().to$().removeClass('winner-gold winner-silver winner-bronze');

            const isDescending = dt.order()?.[0]?.[1] === 'desc';
            let rows = dt.rows({
                order: 'applied',
                search: 'applied'
            }).indexes().toArray();

            const getRank = (rowIdx) => {
                const cell = dt.cell(rowIdx, cfg.rankCol).data();
                const match = String(cell ?? '').match(/\((\d+)\)/);
                return match ? parseInt(match[1], cfg.radix) : Infinity;
            };

            rows.sort((a, b) => {
                const A = getRank(a),
                    B = getRank(b);
                return !isDescending ? (B - A) : (A - B);
            });

            const prepRows = isDescending ? rows : rows.reverse();
            const colorClasses = ['winner-gold', 'winner-silver', 'winner-bronze'];

            let currentId = 0;
            let topId = 0;
            const maxTopGroups = Math.min(prepRows.length, colorClasses.length);

            while (currentId < prepRows.length && topId < maxTopGroups) {
                const rowIdx = prepRows[currentId];
                $(dt.row(rowIdx).node()).addClass(colorClasses[topId]);

                const nextRowIdx = prepRows[currentId + 1];

                if (nextRowIdx == null) {
                    break;
                }

                if (getRank(rowIdx) !== getRank(nextRowIdx)) {
                    topId += 1;
                }

                currentId += 1;
            }

        };

        paintWinners();
        dt.on('draw', paintWinners);
    });

    $('.dtsp-titleRow').hide();
});