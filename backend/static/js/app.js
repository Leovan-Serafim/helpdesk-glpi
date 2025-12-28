document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("pergunta");
    const sendButton = document.getElementById("enviar");
    const chatBox = document.getElementById("chatBox");

    const enviarPergunta = async () => {
        const pergunta = input.value.trim();
        if (!pergunta) return;

        // Mensagem do usuário
        chatBox.innerHTML += `<div class="user">Você: ${pergunta}</div>`;
        input.value = "";

        // Placeholder da IA
        chatBox.innerHTML += `<div class="bot">IA: <em>pensando...</em></div>`;
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            const response = await fetch("/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ question: pergunta })
            });

            if (!response.ok) {
                throw new Error(`Erro ${response.status}`);
            }

            const data = await response.json();
            const respostaIA = data.resposta || "Sem resposta do servidor.";

            chatBox.lastChild.innerHTML =
                `<strong>IA:</strong> ${respostaIA.replace(/\n/g, "<br>")}`;

            chatBox.scrollTop = chatBox.scrollHeight;

        } catch (erro) {
            console.error(erro);
            chatBox.lastChild.innerHTML =
                `<strong>IA:</strong> <em style="color:red;">Erro: ${erro.message}</em>`;
        }
    };

    // Clique no botão
    sendButton.addEventListener("click", enviarPergunta);

    // Enter no input
    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            enviarPergunta();
        }
    });
});
