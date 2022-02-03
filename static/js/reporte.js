document.getElementById('reporte').addEventListener('click', () => {
    document.querySelector('.bg-modal').style.display = 'flex';
});

document.getElementById('close').addEventListener('click', () => {
    document.querySelector('.bg-modal').style.display = 'none';
})

$(document).ready( function () {
    $('.datatable').DataTable({
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.11.4/i18n/es_es.json"
        }
    });
} );