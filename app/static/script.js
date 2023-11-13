document.addEventListener("DOMContentLoaded", function () {

    // Obtenha todas as linhas da tabela
    var rows = document.querySelectorAll(".table-container table tbody tr");

    rows.forEach(function (row) {
        if (row.classList.contains("receita")) {
            row.style.backgroundColor = "#8fdd8f";
        } else if (row.classList.contains("despesa")) {
            row.style.backgroundColor = "#ff9999";
        }
    });
});