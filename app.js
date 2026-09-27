document.addEventListener("DOMContentLoaded", () => {
    carregarTransferencias();
    pedirPermissaoNotificacao();
});

async function carregarTransferencias() {
    try {
        const response = await fetch('/api/transferencias');
        if (!response.ok) {
            throw new Error('Falha na comunicação com o servidor.');
        }
        
        const dados = await response.json();
        
        if (dados.erro) {
            throw new Error(dados.erro);
        }

        renderizarCards(dados);
        verificarNovasTransferencias(dados);

    } catch (error) {
        console.error("Erro ao procurar os dados:", error);
        const container = document.getElementById('grid-transferencias');
        if (container) {
            container.innerHTML = `
                <div style="text-align: center; color: #ef4444; padding: 40px; grid-column: 1 / -1;">
                    Erro ao carregar as informações da base de dados.
                </div>
            `;
        }
    }
}

function renderizarCards(transferencias) {
    const container = document.getElementById('grid-transferencias');
    if (!container) return;

    if (transferencias.length === 0) {
        container.innerHTML = '<div style="text-align: center; color: #9ca3af; padding: 40px; grid-column: 1 / -1;">Nenhuma transferência encontrada.</div>';
        return;
    }

    container.innerHTML = '';

    transferencias.forEach(row => {
        const jogador = row.Jogador || 'Nome do Atleta';
        const origem = row.Origem || 'Sem Clube';
        const destino = row.Destino || 'Nome do Clube';
        const valor = row.Valor && row.Valor !== "Não revelado" ? ` - ${row.Valor}` : '';
        const statusText = (row.Status || 'TRANSFERÊNCIA').toUpperCase();
        const fonte = row.Fonte || '365Scores';

        const isRumor = statusText.includes("RUMOR");
        const classeBadge = isRumor ? "badge-rumor" : "badge-fechado";

        const imgJogador = `https://ui-avatars.com/api/?name=${encodeURIComponent(jogador)}&background=2b2b2b&color=ffffff`;
        const imgClube = `https://ui-avatars.com/api/?name=${encodeURIComponent(destino)}&background=2b2b2b&color=ffffff`;

        const cardHTML = `
            <div class="card">
                <div class="card-jogador">
                    <img src="${imgJogador}" alt="Foto de ${jogador}">
                    <h3>${jogador}</h3>
                </div>
                <div class="card-status">
                    <span class="badge ${classeBadge}">${statusText}${valor}</span>
                    <small>Fonte: ${fonte}</small>
                </div>
                <div class="card-clube">
                    <img src="${imgClube}" alt="Escudo de ${destino}">
                    <h3>${destino}</h3>
                </div>
                ${origem !== 'Sem Clube' ? `<div style="text-align: center; font-size: 12px; color: #9ca3af; margin-top: 8px;">De: ${origem}</div>` : ''}
            </div>
        `;

        container.innerHTML += cardHTML;
    });
}

// Registo de PWA e Notificações Push
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
        .then(() => console.log("Service Worker registado com sucesso!"))
        .catch(err => console.log("Erro ao registar Service Worker:", err));
}

function pedirPermissaoNotificacao() {
    if (window.Notification && Notification.permission !== "granted") {
        Notification.requestPermission();
    }
}

function verificarNovasTransferencias(dados) {
    if (!dados || dados.length === 0) return;
    
    const primeiroItem = dados[0];
    const identificadorAtual = primeiroItem.Jogador + (primeiroItem.Destino || '');
    const ultimoIdSalvo = localStorage.getItem('ultimo_id_transferencia');

    if (ultimoIdSalvo && ultimoIdSalvo !== identificadorAtual) {
        if (window.Notification && Notification.permission === "granted") {
            navigator.serviceWorker.ready.then(registration => {
                registration.showNotification("⚽ Nova Transferência!", {
                    body: `${primeiroItem.Jogador} foi para ${primeiroItem.Destino || 'um novo clube'}!`,
                    icon: "https://cdn-icons-png.flaticon.com/512/33/33736.png"
                });
            });
        }
    }
    localStorage.setItem('ultimo_id_transferencia', identificadorAtual);
}