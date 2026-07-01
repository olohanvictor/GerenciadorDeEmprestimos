import flet as ft
import utils
import database

def main(page: ft.Page):
    #Inicializa a tabela
    database.criar_tabela()

    page.title = "Biblioteca - Controle de Empréstimos"
    page.window.maximized = True
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    # Variável que controla qual ID está em edição (None se for um novo cadastro)
    id_em_edicao = None

    # --- COMPONENTES VISUAIS ---
    titulo = ft.Text("Biblioteca - Controle de Empréstimos", size=30, weight=ft.FontWeight.BOLD)
    campo_nome = ft.TextField(label="Nome", width=250)
    campo_cpf = ft.TextField(label="CPF", width=180)
    campo_livro = ft.TextField(label="Livro", width=300)
    campo_data_emprestimo = ft.TextField(label="Data empréstimo", hint_text="DD/MM/AAAA", width=180)
    campo_data_devolucao = ft.TextField(label="Data devolução", hint_text="DD/MM/AAAA", width=180)
    campo_pesquisa = ft.TextField(label="Pesquisar por nome, CPF ou livro", prefix_icon=ft.Icons.SEARCH, width=400)

    botao_salvar = ft.ElevatedButton("Salvar", on_click=lambda e: salvar(e), icon=ft.Icons.SAVE)
    botao_cancelar = ft.TextButton("Cancelar", on_click=lambda e: limpar_edicao(), visible=False, icon=ft.Icons.CANCEL)
    
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

    # --- SINAIS DE POP-UP (SnackBars) ---
    def sucesso(msg):
        page.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor="green")
        page.snack_bar.open = True
        page.update()

    def erro(msg):
        page.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor="red", duration=4000)
        page.snack_bar.open = True
        page.update()
    
    # --- PROCESSOS DE DIGITAÇÃO E VALIDAÇÃO ---
    def ao_mudar_cpf(e):
        campo_cpf.value = utils.formatar_cpf_str(campo_cpf.value)
        page.update()

    def ao_mudar_data_emp(e):
        campo_data_emprestimo.value = utils.formatar_data_str(campo_data_emprestimo.value)
        page.update()

    def ao_mudar_data_dev(e):
        campo_data_devolucao.value = utils.formatar_data_str(campo_data_devolucao.value)
        page.update()

    def validar_campo_data_ao_sair(campo):
        if not campo.value.strip():
            campo.error_text = None
        elif len(campo.value) < 10:
            campo.error_text = "Data incompleta!"
        elif not utils.es_data_valida(campo.value):
            campo.error_text = "Data inválida!"
        else:
            campo.error_text = None
        page.update()

    # Vinculando os eventos explicitamente
    campo_cpf.on_change = ao_mudar_cpf
    campo_data_emprestimo.on_change = ao_mudar_data_emp
    campo_data_devolucao.on_change = ao_mudar_data_dev
    campo_data_emprestimo.on_blur = lambda e: validar_campo_data_ao_sair(campo_data_emprestimo)
    campo_data_devolucao.on_blur = lambda e: validar_campo_data_ao_sair(campo_data_devolucao)
    campo_pesquisa.on_change = lambda e: atualizar_tabela()

    # --- CONTROLE E FLUXO DE EDIÇÃO ---
    def iniciar_edicao(item_dict):
        nonlocal id_em_edicao
        id_em_edicao = item_dict["id"]
        
        campo_nome.value = item_dict["nome"]
        campo_cpf.value = item_dict["cpf"]
        campo_livro.value = item_dict["livro"]
        campo_data_emprestimo.value = item_dict["data_emprestimo"]
        campo_data_devolucao.value = item_dict["data_devolucao"]
        
        botao_salvar.text = "Atualizar Empréstimo"
        botao_salvar.icon = ft.Icons.EDIT
        botao_salvar.bgcolor = ft.Colors.PURPLE
        botao_salvar.color = ft.Colors.WHITE
        botao_cancelar.visible = True
        
        campo_nome.focus()
        page.update()

    def limpar_edicao():
        nonlocal id_em_edicao
        id_em_edicao = None
        
        campo_nome.value = ""
        campo_cpf.value = ""
        campo_livro.value = ""
        campo_data_emprestimo.value = ""
        campo_data_devolucao.value = ""
        
        campo_nome.error_text = None
        campo_livro.error_text = None
        campo_data_emprestimo.error_text = None
        campo_data_devolucao.error_text = None
        
        botao_salvar.text = "Salvar"
        botao_salvar.icon = ft.Icons.SAVE
        botao_salvar.bgcolor = None
        botao_salvar.color = None
        botao_cancelar.visible = False
        page.update()

    # --- MONTAGEM DA TABELA (ESTÁVEL) ---
    def atualizar_tabela():
        tabela.rows.clear()
        pesquisa = campo_pesquisa.value.lower().strip()
        emprestimos = database.listar_emprestimos()

        for item in emprestimos:
            # Transforma em dicionário comum do Python de forma explícita
            item_dados = dict(item)

            if pesquisa and (
                pesquisa not in item_dados["nome"].lower()
                and pesquisa not in item_dados["cpf"].lower()
                and pesquisa not in item_dados["livro"].lower()
            ):
                continue

            est_devolvido = bool(item_dados["devolvido"])

            if est_devolvido:
                status_widget = ft.Text("✅ Devolvido", color="green", weight=ft.FontWeight.BOLD)
            else:
                status_widget = ft.Text("📚 Emprestado", color="blue", weight=ft.FontWeight.BOLD)

            id_atual = item_dados["id"]

            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item_dados["nome"])),
                        ft.DataCell(ft.Text(item_dados["cpf"])),
                        ft.DataCell(ft.Text(item_dados["livro"])),
                        ft.DataCell(ft.Text(item_dados["data_emprestimo"])),
                        ft.DataCell(ft.Text(item_dados["data_devolucao"])),
                        ft.DataCell(status_widget),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        ft.Icons.EDIT, 
                                        tooltip="Editar", 
                                        icon_color="blue_400", 
                                        on_click=lambda e, it=item_dados: iniciar_edicao(it)
                                    ),
                                    ft.IconButton(
                                        ft.Icons.CHECK, 
                                        tooltip="Marcar devolvido", 
                                        icon_color="green" if not est_devolvido else "grey_400",
                                        disabled=est_devolvido,
                                        on_click=lambda e, idx=id_atual: executar_devolucao(idx)
                                    ),
                                    ft.IconButton(
                                        ft.Icons.UNDO, 
                                        tooltip="Desfazer devolução", 
                                        icon_color="orange" if est_devolvido else "grey_400",
                                        disabled=not est_devolvido,
                                        on_click=lambda e, idx=id_atual: executar_desfazer(idx)
                                    ),
                                    ft.IconButton(
                                        ft.Icons.DELETE, 
                                        tooltip="Excluir", 
                                        icon_color="red", 
                                        on_click=lambda e, idx=id_atual: executar_exclusao(idx)
                                    ),
                                ]
                            )
                        ),
                    ]
                )
            )
        page.update()

    # --- SALVAR OU ATUALIZAR ---
    def salvar(e):
        if not campo_nome.value.strip(): #Se o valor for nulo, erro.
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

        validar_campo_data_ao_sair(campo_data_emprestimo)
        validar_campo_data_ao_sair(campo_data_devolucao)

        if campo_data_emprestimo.error_text or not campo_data_emprestimo.value.strip():
            if not campo_data_emprestimo.value.strip(): campo_data_emprestimo.error_text = "Obrigatório"
            erro("Corrija a data de empréstimo antes de salvar.")
            return

        if campo_data_devolucao.error_text or not campo_data_devolucao.value.strip():
            if not campo_data_devolucao.value.strip(): campo_data_devolucao.error_text = "Obrigatório"
            erro("Corrija a data de devolução antes de salvar.")
            return

        if id_em_edicao is not None:
            database.atualizar_emprestimo(
                id_em_edicao, campo_nome.value, campo_cpf.value, campo_livro.value,
                campo_data_emprestimo.value, campo_data_devolucao.value
            )
            sucesso("Empréstimo atualizado com sucesso!")
        else:
            database.adicionar_emprestimo(
                campo_nome.value, campo_cpf.value, campo_livro.value,
                campo_data_emprestimo.value, campo_data_devolucao.value
            )
            sucesso("Empréstimo cadastrado com sucesso!")

        limpar_edicao()
        atualizar_tabela()

    # --- AÇÕES INTERMEDIÁRIAS DO BANCO ---
    def executar_devolucao(id_emp):
        database.marcar_devolvido(id_emp)
        sucesso("Status atualizado para Devolvido!")
        atualizar_tabela()

    def executar_desfazer(id_emp):
        database.desfazer_devolucao(id_emp)
        sucesso("Status alterado de volta para Emprestado!")
        atualizar_tabela()

    def executar_exclusao(id_emp):
        database.excluir_emprestimo(id_emp)
        sucesso("Empréstimo excluído!")
        if id_em_edicao == id_emp:
            limpar_edicao()
        atualizar_tabela()

    # --- LAYOUT PRINCIPAL ---
    formulario = ft.Row(
        controls=[
            campo_nome, campo_cpf, campo_livro,
            campo_data_emprestimo, campo_data_devolucao,
            botao_salvar, botao_cancelar
        ],
        wrap=True,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    page.add(
        titulo,
        ft.Card(content=ft.Container(formulario, padding=15)),
        campo_pesquisa,
        ft.Divider(),
        ft.Row(controls=[tabela], scroll=ft.ScrollMode.AUTO),
    )

    atualizar_tabela()

ft.run(main)
