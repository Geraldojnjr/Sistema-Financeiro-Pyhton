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

    setupModalButton('btnModalDespesa', 'modalDespesa', 'closeModalDespesa', 'formDespesa', '/adicionar_despesa');
    setupModalButton('btnModalReceita', 'modalReceita', 'closeModalReceita', 'formReceita', '/adicionar_receita');
    setupModalButton('btnModalExtrato', 'modalExtrato', 'closeModalExtrato', 'formExtrato', '/extrato_mensal');
    setupModalButton('btnModalAddCatReceita', 'modalCatReceita', 'closeModalCatReceita', 'formCatReceita', '/cadastrar_categoria_receita');
    setupModalButton('btnModalAddCatDespesa', 'modalCatDespesa', 'closeModalCatDespesa', 'formCatDespesa', '/cadastrar_categoria_despesa');
});

function setupModalButton(btnId, modalId, closeModalId, formId, action) {
    var btn = document.getElementById(btnId);
    var modal = document.getElementById(modalId);
    var closeModal = document.getElementById(closeModalId);
    var form = document.getElementById(formId);

    btn.addEventListener('click', function () {
        modal.style.display = 'block';
    });

    closeModal.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

    // Adicione um event listener para o envio do formulário via AJAX
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        console.log('Formulário enviado:', formId);

        // Obtenha os dados do formulário
        const formData = new FormData(this);

        // Envie os dados via AJAX usando fetch
        fetch(action, {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro de rede: ${response.status}`);
                }
                return response.text();
            })
            .then(data => {
                if (formId === 'formExtrato') {
                    console.log('Resposta do servidor:', data);
                    document.body.innerHTML = data;
                    modal.style.display = 'none';
                } else {
                    console.log('Resposta do servidor:', data);
                    modal.style.display = 'none';
                }
            })
            .catch(error => console.error('Erro:', error));

        if (formId === 'formExtrato') {
            console.log('Evitando recarregamento da página.');
            return false;
        }
    });
}
