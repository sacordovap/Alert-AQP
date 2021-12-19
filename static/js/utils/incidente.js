function resetearForm() {
    $('#observaciones').val("");
    $('#falsa_alarma').prop('checked', false);
    $('#incidente_form').val("");
}

function setIncidenteModal(id) {
    $('#incidente_form').val(id);
}