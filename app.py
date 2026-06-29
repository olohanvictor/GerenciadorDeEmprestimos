import flet as ft
from datetime import datetime

from database import (
    criar_tabela,
    listar_emprestimos,
    adicionar_emprestimo,
    marcar_devolvido,
    desfazer_devolucao
)


def main(page: ft.Page):
    criar_tabela()

    page.title = "Biblioteca - Controle de Empréstimos"
    page.window.maximized = True
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    titulo = ft.Text(
        "Biblioteca - Controle de Empréstimos",
        size=30,
        weight=ft.FontWeight.BOLD
    )

    campo_nome = ft.TextField(
        label="Nome",
        width=250
    )

    campo_cpf = ft.TextField(
        label="CPF",
        width=180
    )

    campo_livro = ft.TextField(
        label="Livro",
        width=300
    )

    campo_data_emprestimo = ft.TextField(
        label="Data empréstimo",
        width=150
    )

    campo_data_devolucao = ft.TextField(
        label="Data devolução",
        width=150
    )

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("CPF")),
            ft.DataColumn(ft.Text("Livro")),
            ft.DataColumn(ft.Text("Pegou")),
            ft.DataColumn(ft.Text("Devolver")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[]
    )

    def formatar_cpf(e):
        cpf = ''.join(filter(str.isdigit, campo_cpf.value))

        if len(cpf) > 11:
            cpf = cpf[:11]

        if len(cpf) > 9:
            cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        elif len(cpf) > 6:
            cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:]}"
        elif len(cpf) > 3:
            cpf = f"{cpf[:3]}.{cpf[3:]}"
        else:
            cpf = cpf

        campo_cpf.value = cpf
        page.update()

    campo_cpf.on_change = formatar_cpf

    def formatar_data(campo):
        data = ''.join(filter(str.isdigit, campo.value))

        if len(data) > 8:
            data = data[:8]

        if len(data) > 4:
            data = f"{data[:2]}/{data[2:4]}/{data[4:]}"
        elif len(data) > 2:
            data = f"{data[:2]}/{data[2:]}"
        else:
            data = data

        campo.value = data

    def data_emprestimo_change(e):
        formatar_data(campo_data_emprestimo)
        page.update()

    def data_devolucao_change(e):
        formatar_data(campo_data_devolucao)
        page.update()

    campo_data_emprestimo.on_change = data_emprestimo_change
    campo_data_devolucao.on_change = data_devolucao_change

    def data_valida(data):
        try:
            datetime.strptime(data, "%d/%m/%Y")
            return True
        except:
            return False

    def atualizar_tabela():
        tabela.rows.clear()

        emprestimos = listar_emprestimos()

        for item in emprestimos:
            status = "✅ Devolvido" if item["devolvido"] else "📚 Emprestado"

            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item["nome"])),
                        ft.DataCell(ft.Text(item["cpf"])),
                        ft.DataCell(ft.Text(item["livro"])),
                        ft.DataCell(ft.Text(item["data_emprestimo"])),
                        ft.DataCell(ft.Text(item["data_devolucao"])),
                        ft.DataCell(ft.Text(status)),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.CHECK,
                                        tooltip="Marcar devolvido",
                                        on_click=lambda e,
                                        id=item["id"]:
                                        devolver(id)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.UNDO,
                                        tooltip="Desfazer",
                                        on_click=lambda e,
                                        id=item["id"]:
                                        desfazer(id)
                                    )
                                ]
                            )
                        )
                    ]
                )
            )

        page.update()

    def salvar(e):
        if campo_nome.value.strip() == "":
            return

        if campo_livro.value.strip() == "":
            return

        if not data_valida(campo_data_emprestimo.value):
            campo_data_emprestimo.error_text = "Data inválida"
            page.update()
            return

        campo_data_emprestimo.error_text = None

        if not data_valida(campo_data_devolucao.value):
            campo_data_devolucao.error_text = "Data inválida"
            page.update()
            return

        campo_data_devolucao.error_text = None

        adicionar_emprestimo(
            campo_nome.value,
            campo_cpf.value,
            campo_livro.value,
            campo_data_emprestimo.value,
            campo_data_devolucao.value
        )

        campo_nome.value = ""
        campo_cpf.value = ""
        campo_livro.value = ""
        campo_data_emprestimo.value = ""
        campo_data_devolucao.value = ""

        atualizar_tabela()

    def devolver(id):
        marcar_devolvido(id)
        atualizar_tabela()

    def desfazer(id):
        desfazer_devolucao(id)
        atualizar_tabela()

    formulario = ft.Row(
        controls=[
            campo_nome,
            campo_cpf,
            campo_livro,
            campo_data_emprestimo,
            campo_data_devolucao,
            ft.ElevatedButton(
                "Salvar",
                on_click=salvar
            )
        ],
        wrap=True
    )

    page.add(
        titulo,
        formulario,
        ft.Divider(),
        tabela
    )

    atualizar_tabela()


ft.run(main)