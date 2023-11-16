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