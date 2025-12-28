def validate_tickets(tickets):
    """
    Verifica problemas básicos nos tickets.
    Não corrige, apenas sinaliza.
    """

    issues = []

    for ticket in tickets:
        if not ticket.get("id"):
            issues.append("Ticket sem ID")

        if not ticket.get("user_id"):
            issues.append(f"Ticket {ticket.get('id')} sem usuário associado")

        if not ticket.get("status_id"):
            issues.append(f"Ticket {ticket.get('id')} sem status")

    return issues


def validate_users(users):
    """
    Verifica inconsistências simples nos usuários.
    """

    issues = []

    for user in users:
        if not user.get("name"):
            issues.append(f"Usuário ID {user.get('id')} sem nome")

        if not user.get("email"):
            issues.append(f"Usuário {user.get('name')} sem e-mail")

    return issues
