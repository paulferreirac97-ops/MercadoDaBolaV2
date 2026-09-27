document.addEventListener("DOMContentLoaded", () => {
    carregarDados();
});

async function carregarDados() {
    const grid = document.getElementById('grid-transferencias');
    grid.innerHTML = '<p style="text-align: center; color: #8b92a5;">A carregar transferências do 365Scores...</p>';

    try {
        // Consome a API local que está a correr no terminal do VS Code
        const resposta = await fetch('http://localhost:5000/api/transferencias');
        const dados = await resposta.json();

        grid.innerHTML = ''; // Limpa o aviso de carregamento

        if (dados.length === 0) {
            grid.innerHTML = '<p style="text-align: center; color: #8b92a5;">Nenhuma transferência encontrada no 365Scores.</p>';
            return;
        }

        dados.forEach(linha => {
            const corStatus = linha.Status.toUpperCase() === 'FECHADO' ? 'badge-fechado' : 'badge-interesse';
            
            // Tratamento de imagens ausentes
            const urlJogador = linha.Jogador.replace(/ /g, "+");
            const urlClube = linha.Clube.replace(/ /g, "+");
            const foto = linha.foto_url === "0" ? `https://ui-avatars.com/api/?name=${urlJogador}&background=2b2b2b&color=ffffff` : linha.foto_url;
            const escudo = linha.escudo_url === "0" ? `https://ui-avatars.com/api/?name=${urlClube}&background=2b2b2b&color=ffffff` : linha.escudo_url;

            const cardHTML = `
                <div class="card">
                    <div class="card-jogador">
                        <img src="${foto}" alt="${linha.Jogador}">
                        <h3>${linha.Jogador}</h3>
                    </div>
                    <div class="card-status">
                        <span class="badge ${corStatus}">${linha.Status}</span>
                        <small>Fonte: 365Scores</small>
                    </div>
                    <div class="card-clube">
                        <img src="${escudo}" alt="${linha.Clube}">
                        <h3>${linha.Clube}</h3>
                    </div>
                </div>
            `;
            grid.innerHTML += cardHTML;
        });

    } catch (erro) {
        console.error("Erro ao procurar dados:", erro);
        grid.innerHTML = '<p style="text-align: center; color: #ff4d4d;">Erro ao ligar à base de dados.</p>';
    }
}