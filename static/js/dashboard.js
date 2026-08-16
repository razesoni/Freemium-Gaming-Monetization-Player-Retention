$(document).ready(function () {
    $('.select2').select2({
        width: '100%',
        placeholder: "Select option(s)"
    });

    function getFilterPayload() {
        return {
            genres: $('#genres').val() || [],
            segments: $('#segments').val() || [],
            devices: $('#devices').val() || [],
            countries: $('#countries').val() || []
        };
    }

    function renderPlotly(chartId, chartData) {
        if (chartData && chartData.data) {
            Plotly.react(chartId, chartData.data, chartData.layout, { responsive: true });
        } else {
            document.getElementById(chartId).innerHTML = `
                <div class="text-warning text-center p-4">No data available for current selection.</div>
            `;
        }
    }

    function renderTable(columns, rows) {
        const thead = $('#table-head-row');
        const tbody = $('#table-body');
        thead.empty();
        tbody.empty();

        if (!columns || columns.length === 0 || !rows || rows.length === 0) {
            tbody.append('<tr><td colspan="12" class="text-center text-muted">No records found.</td></tr>');
            return;
        }

        columns.forEach(col => thead.append(`<th>${col}</th>`));
        rows.forEach(row => {
            let rowHtml = '<tr>';
            columns.forEach(col => {
                rowHtml += `<td>${row[col] !== null ? row[col] : '-'}</td>`;
            });
            rowHtml += '</tr>';
            tbody.append(rowHtml);
        });
    }

    function updateDashboard() {
        const payload = getFilterPayload();

        $.ajax({
            url: '/api/filter',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(payload),
            success: function (res) {
                // KPIs
                $('#kpi-revenue').text(res.kpis.total_revenue);
                $('#kpi-paying').text(res.kpis.paying_users);
                $('#kpi-f2p').text(res.kpis.f2p_users);
                $('#kpi-arppu').text(res.kpis.arppu);

                // Tab 1: Monetization
                renderPlotly('chart-pareto', res.charts.fig_pareto);
                renderPlotly('chart-genre-rev', res.charts.fig_genre_rev);
                renderPlotly('chart-depth', res.charts.fig_depth);

                // Tab 2: Engagement vs. Spend
                renderPlotly('chart-corr', res.charts.fig_corr);
                renderPlotly('chart-scatter', res.charts.fig_scatter);
                renderPlotly('chart-session-box', res.charts.fig_session_box);

                // Tab 3: Platform & Cohorts
                renderPlotly('chart-device', res.charts.fig_device);
                renderPlotly('chart-country', res.charts.fig_country);
                renderPlotly('chart-latency', res.charts.fig_latency);

                // Tab 4: Table
                renderTable(res.table_cols, res.table_data);
            },
            error: function (err) {
                console.error("Dashboard update failed:", err);
            }
        });
    }

    $('#apply-filters-btn').on('click', updateDashboard);

    $('#reset-filters-btn').on('click', function () {
        $('#genres').val($('#genres option').map(function () { return this.value; }).get()).trigger('change');
        $('#segments').val($('#segments option').map(function () { return this.value; }).get()).trigger('change');
        $('#devices').val($('#devices option').map(function () { return this.value; }).get()).trigger('change');
        $('#countries').val(null).trigger('change');
        updateDashboard();
    });

    $('#download-csv-btn').on('click', function () {
        const payload = getFilterPayload();
        fetch('/api/download-csv', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
            .then(response => response.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'freemium_game_analytics.csv';
                document.body.appendChild(a);
                a.click();
                a.remove();
            });
    });

    $('button[data-bs-toggle="tab"]').on('shown.bs.tab', function () {
        window.dispatchEvent(new Event('resize'));
    });

    updateDashboard();
});