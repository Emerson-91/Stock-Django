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