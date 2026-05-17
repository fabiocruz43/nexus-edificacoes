function mostrarServico(id) {
    const detalhes = document.querySelectorAll(".detalhe");

    detalhes.forEach(function(item) {
        item.classList.remove("ativo");
    });

    const escolhido = document.getElementById(id);

    if (escolhido) {
        escolhido.classList.add("ativo");

        escolhido.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });
    }
}