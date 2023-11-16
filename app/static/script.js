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
    var container = document.getElementById('extrato-container'); // Adicionado para verificar o contêiner

    console.log('Contêiner:', container); // Adicionado para verificar o contêiner

    btn.addEventListener('click', function () {
        modal.style.display = 'block';
    });

    closeModal.addEventListener('click', function () {
        modal.style.display = 'none';
        location.reload(); // Recarregar a página ao fechar o modal
    });

    window.addEventListener('click', function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

    // Adicione um event listener para o envio do formulário via AJAX
    form.addEventListener('submit', function (event) {
        event.preventDefault();

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
                console.log('Resposta do servidor:', data);
            
                if (formId === 'formExtrato') {
                    var container = document.getElementById('extrato-container');
            
                    if (container) {
                        container.innerHTML = data;
                    } else {
                        console.error('Contêiner não encontrado');
                    }
            
                    modal.style.display = 'none'; // Fechar o modal após o envio bem-sucedido
                } else {
                    modal.style.display = 'none';
                }
            })
            
            .catch(error => console.error('Erro:', error));
    });
}
