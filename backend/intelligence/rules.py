# intelligence/rules.py

def should_escalate(ticket):
    """
    Decide se um chamado deve ser escalado.
    """

    # Se o chamado é crítico e ainda está aberto
    if ticket["priority"] == "CRITICA" and ticket["status"] != "FECHADO":
        return True

    return False
