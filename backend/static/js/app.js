async function enviarPergunta() {
    const input = document.getElementById("pergunta");
    const chatBox = document.getElementById("chatBox");

    const pergunta = input.value.trim();
    if (!pergunta) return;

    chatBox.innerHTML += `<div class="user">Você: ${pergunta}</div>`;
    input.value = "";

    const response = await fetch("/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ pergunta })
    });

    const data = await response.json();

    chatBox.innerHTML += `<div class="bot">IA: ${data.resposta}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}
