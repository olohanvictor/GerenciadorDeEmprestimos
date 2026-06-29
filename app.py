import flet as ft
from datetime import datetime

from database import (
    criar_tabela,
    listar_emprestimos,
    adicionar_emprestimo,
    marcar_devolvido,
    desfazer_devolucao,
    excluir_emprestimo
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

    campo_pesquisa = ft.TextField(
	 label="Pesquisar por nome, CPF ou livro",
	 prefix_icon=ft.Icons.SEARCH,
	 width=400,
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

    def excluir(id):
        excluir_emprestimo(id)
        atualizar_tabela()

        page.snack_bar = ft.SnackBar(
	  content=ft.Text("Empréstimo excluído!")
        )
        page.snack_bar.open = True
        page.update()
	
    def sucesso(msg):
        page.snack_bar = ft.SnackBar(
          content=ft.Text(msg),
          bgcolor="green"
        )
        page.snack_bar.open = True
        page.update()

    def erro(msg):
        page.snack_bar = ft.SnackBar(
         content=ft.Text(msg),
         bgcolor="red"
        )
        page.snack_bar.open = True
        page.update()
    
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

     pesquisa = campo_pesquisa.value.lower().strip()

     emprestimos = listar_emprestimos()

     for item in emprestimos:

        if pesquisa:
            if (
                pesquisa not in item["nome"].lower()
                and pesquisa not in item["cpf"].lower()
                and pesquisa not in item["livro"].lower()
            ):
                continue

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
                                    on_click=lambda e, id=item["id"]: devolver(id),
                                ),
				ft.IconButton(
    				    icon=ft.Icons.DELETE,
    				    tooltip="Excluir",
    				    icon_color="red",
    				    on_click=lambda e, id=item["id"]: excluir(id),
				),
                                ft.IconButton(
                                    icon=ft.Icons.UNDO,
                                    tooltip="Desfazer",
                                    on_click=lambda e, id=item["id"]: desfazer(id),
                                ),
                            ]
                        )
                    ),
                ]
            )
        )
     page.update()
    campo_pesquisa.on_change = lambda e: atualizar_tabela()
    def salvar(e):
        if not campo_nome.value.strip():
    	        erro("Informe o nome")
    	        campo_nome.error_text = "Obrigatório"
    	        page.update()
    	        return

        campo_nome.error_text = None
        
        if not campo_livro.value.strip():
                erro("Informe o nome do livro")
                campo_livro.error_text = "Obrigatório"
                page.update()
                return

        campo_livro.error_text = None
        
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

        page.snack_bar = ft.SnackBar(
                content=ft.Text("Emprestimo cadastrado!")
                )
        page.snack_bar.open = True
        page.update()

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
    campo_pesquisa,
    ft.Divider(),
    ft.Row(
        controls=[tabela],
        scroll=ft.ScrollMode.AUTO,
    ),
)

    atualizar_tabela()


ft.run(main)
