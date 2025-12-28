from database.connection import get_connection
from datetime import datetime, timedelta


def seed():
    conn = get_connection()
    cur = conn.cursor()

    # =========================
    # CLIENTE
    # =========================
    cur.execute(
        "INSERT INTO clientes (nome, cnpj, contato) VALUES (?, ?, ?)",
        ("Empresa Alfa", "00.000.000/0001-00", "ti@empresa.com")
    )

    # =========================
    # EQUIPAMENTOS (4)
    # =========================
    equipamentos = [
        ("Desktop", "Dell", "Optiplex 3080", "ABC123", "Financeiro"),
        ("Desktop", "HP", "ProDesk 400", "DEF456", "Administrativo"),
        ("Desktop", "Lenovo", "ThinkCentre M720", "GHI789", "Comercial"),
        ("Desktop", "Dell", "Precision 3650", "JKL012", "TI"),
    ]

    for eq in equipamentos:
        cur.execute(
            """INSERT INTO equipamentos
               (cliente_id, tipo, marca, modelo, serial, localizacao)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (1, *eq)
        )

    # =========================
    # USUÁRIO
    # =========================
    cur.execute(
        "INSERT INTO usuarios (nome, email, cliente_id) VALUES (?, ?, ?)",
        ("João Silva", "joao@empresa.com", 1)
    )

    # =========================
    # CHAMADOS (15)
    # =========================
    base_date = datetime.now() - timedelta(days=20)

    chamados = [
        # Equipamento 1 — Financeiro (HD com problema)
        (1, "Sistema lento", "Hardware", "Aberto"),
        (1, "Erro ao abrir sistema financeiro", "Software", "Aberto"),
        (1, "Travamentos constantes", "Hardware", "Aberto"),
        (1, "Erro de leitura em disco", "Hardware", "Fechado"),

        # Equipamento 2 — Administrativo (Atualização Windows)
        (2, "Tela azul após atualização", "Sistema", "Fechado"),
        (2, "Sistema não inicia", "Sistema", "Fechado"),
        (2, "Impressora não funciona", "Periféricos", "Aberto"),
        (2, "Erro de driver desconhecido", "Sistema", "Aberto"),

        # Equipamento 3 — Comercial (Rede instável)
        (3, "VPN desconectando", "Rede", "Aberto"),
        (3, "Erro de login no sistema", "Sistema", "Aberto"),
        (3, "Sistema não sincroniza dados", "Software", "Aberto"),
        (3, "Internet instável", "Rede", "Fechado"),

        # Equipamento 4 — TI (Drivers / Hardware)
        (4, "USB não reconhece", "Hardware", "Aberto"),
        (4, "Periféricos desconectando", "Hardware", "Aberto"),
        (4, "Erro após troca de hardware", "Hardware", "Aberto"),
    ]

    for equipamento_id, problema, categoria, status in chamados:
        cur.execute(
            """INSERT INTO chamados
               (cliente_id, equipamento_id, usuario_id, problema, categoria, status, data_abertura)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                1,
                equipamento_id,
                1,
                problema,
                categoria,
                status,
                base_date.strftime("%Y-%m-%d")
            )
        )
        base_date += timedelta(days=1)

    # =========================
    # SOLUÇÕES (PARCIAIS)
    # =========================
    cur.execute(
        """INSERT INTO solucoes
           (categoria, descricao_problema, procedimento)
           VALUES (?, ?, ?)""",
        ("Hardware", "Sistema lento e travando", "Verificado possível falha em disco rígido")
    )

    cur.execute(
        """INSERT INTO solucoes
           (categoria, descricao_problema, procedimento)
           VALUES (?, ?, ?)""",
        ("Sistema", "Tela azul após atualização", "Rollback de atualização do Windows")
    )

    conn.commit()
    conn.close()

    print("Seed executado com sucesso (15 chamados, 4 equipamentos)")


if __name__ == "__main__":
    seed()
