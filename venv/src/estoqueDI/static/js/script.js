// Script para mostrar/ocultar a tabela ao clicar no botão
$(document).ready(function () {
    $(".historico-button").click(function () {
        // Obtém o ID da tabela associada ao botão clicado
        var tabelaAlvo = $(this).data("tabela");

        // Oculta todas as tabelas
        $(".historico-tabela").hide();

        // Exibe a tabela associada ao botão clicado
        $("#" + tabelaAlvo).show();
    });
});

//MODAL DAS MENSAGENS
$(document).ready(function () {
    var messagesContainer = $('#message-container');
    var modalMessageContent = $('#modal-message-content');

    if (messagesContainer.length && messagesContainer.children().length) {
        messagesContainer.children().appendTo(modalMessageContent);
        $('#messageModal').modal('show');
    }
});
$(document).ready(function () {
    $('th').click(function () {
        var table = $(this).parents('table').eq(0);
        var rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index()));
        this.asc = !this.asc;
        if (!this.asc) { rows = rows.reverse() }
        for (var i = 0; i < rows.length; i++) { table.append(rows[i]) }
    });
    function comparer(index) {
        return function (a, b) {
            var valA = getCellValue(a, index), valB = getCellValue(b, index);
            return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.localeCompare(valB);
        };
    }
    function getCellValue(row, index) { return $(row).children('td').eq(index).text() }
});