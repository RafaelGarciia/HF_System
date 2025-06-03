import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame
from typing import Literal

# Lista com os temas aceitos pelo ttkbootstrap.Style
Theme = Literal[
    'cerculean',
    'cosmo',
    'cyborg',
    'darkly',
    'flatly',
    'journal',
    'litera',
    'lumen',
    'minty',
    'morph',
    'pulse',
    'sandstone',
    'simplex',
    'solar',
    'superhero',
    'united',
    'vapor',
    'yeti',
]


class Window(tk.Tk):
    """
    Classe base para criar uma janela com estilo e tamanho definidos.

    Esta classe herda de `tkinter.Tk` e configura uma janela com título, dimensões fixas,
    estilo visual (usando ttkbootstrap) e um container principal.

    Args:
        title (str): Título da janela.
        width (int): Largura da janela.
        height (int): Altura da janela.
        style (Theme, optional): Tema visual da janela, usando ttkbootstrap. Padrão é 'flatly'.

    Attributes:
        width (int): Largura da janela.
        height (int): Altura da janela.
        style (Style): Estilo visual aplicado à interface.
        container (tkinter.Frame): Frame principal que ocupa toda a janela.
    """

    def __init__(self, title, width, height, style: Theme = 'flatly'):
        """
        Inicializa a janela com as propriedades fornecidas.

        Args:
            title (str): O título da janela.
            width (int): Largura da janela.
            height (int): Altura da janela.
            style (str): Tema visual da janela.
        """

        super().__init__()

        self.width = width
        self.height = height

        self.title('Janela principal')
        self.geometry(f'{width}x{height}')
        self.resizable(False, False)
        self.style = Style(style)

        # Frame principal
        self.container = tk.Frame(self)
        self.container.pack(expand=True, fill='both')

    def show_frame(self, frame) -> None:
        """
        Exibe um novo frame dentro do container principal da aplicação.

        Remove (oculta) o frame atual do container e adiciona o frame
        passado como parâmetro, ajustando seu layout para preencher
        completamente a área disponível.

        Args:
            frame (tkinter.Frame): O Frame que será instanciada e exibido no container.
        """

        self.container.pack_forget()
        self.container.pack(expand=True, fill='both')
        page: Frame = frame(self.container)
        page.grid(row=0, column=0, sticky='nsew')

    def criar_menu(self, menu_dict: dict) -> tk.Menu:
        """
        Cria um menu superior em tkinter.Menu a partir de um dicionário de menus e comandos.

        Args:
            menu_dict (dict): Dicionário com a estrutura do menu.
                As chaves são os nomes das cascatas, e os valores são dicionários
                cujas chaves são os nomes dos comandos e os valores são funções
                de callback ou None para separadores.

        Returns:
            tk.Menu: Objeto do menu criado e configurado na janela.
        """

        menubar = tk.Menu(self, tearoff=False)

        for menu_name, commands in menu_dict.items():
            commands: dict
            submenu = tk.Menu(menubar, tearoff=False)
            for label, cmd in commands.items():
                if cmd is None:
                    submenu.add_separator()
                else:
                    submenu.add_command(label=label, command=cmd)
            menubar.add_cascade(label=menu_name, menu=submenu)

        self.config(menu=menubar)
        return menubar


class WindowOverrideredirect(Window):
    """
    Classe que cria uma janela personalizada sem a barra de título do sistema.

    Esta classe herda de `Window` e permite criar uma janela com um cabeçalho
    personalizado, onde o usuário pode clicar e arrastar para mover a janela.
    Além disso, oferece um menu básico com a opção de "Sair" para fechar a janela.

    Args:
        title (str): Título da janela.
        width (int): Largura da janela.
        height (int): Altura da janela.
        style (Theme, optional): Tema visual da janela, usando ttkbootstrap. Padrão é 'flatly'.

    Attributes:
        width (int): Largura da janela.
        height (int): Altura da janela.
        style (Style): Estilo visual aplicado à interface.
        container (tkinter.Frame): Frame principal que ocupa toda a janela.
        move_header (tk.Frame): A área do cabeçalho onde o usuário pode clicar e arrastar a janela.
    """

    def __init__(self, title, width, height, style: Theme = 'flatly'):
        """
        Inicializa a janela personalizada sem a barra de título do sistema.

        Args:
            title (str): Título da janela.
            width (int): Largura da janela.
            height (int): Altura da janela.
            style (Theme, optional): Tema visual da janela, usando ttkbootstrap. Padrão é 'flatly'.
        """
        super().__init__(title, width, height, style)

        # Remove a barra de título do sistema, permitindo a movimentação personalizada
        self.overrideredirect(True)

        # Cria o top menu provisório para a janela
        self.config(
            menu=self.criar_menu(
                {
                    'sistema': {
                        'Sair': self.quit,
                    }
                }
            )
        )

        # Cria a área de cabeçalho, que será usada para arrastar a janela
        self.move_header = tk.Frame(self, bg='#404040', height=25)
        self.move_header.place(
            x=0, y=0, relwidth=1
        )   # Posiciona o cabeçalho no topo da janela

        # Binda os eventos de clique e movimento do mouse ao cabeçalho para permitir arrastar a janela
        self.move_header.bind('<ButtonPress-1>', self.iniciar_mover)
        self.move_header.bind('<B1-Motion>', self.mover_janela)

        # Cria um contêiner para o conteúdo da janela
        self.container = tk.Frame(self)
        self.container.pack(
            expand=True,
            fill='both',
            pady=(25, 0),  # Dá espaço para o cabeçalho
        )

    def iniciar_mover(self, event):
        """
        Método chamado quando o usuário clica na área de arrastar.

        Este método registra a posição inicial do clique para que a janela
        possa ser movida com base no movimento do mouse.

        Parâmetros:
            event (tkinter.Event): O evento de clique do mouse.
        """

        # Armazena as coordenadas do clique para calcular a movimentação da janela
        self.x_click = event.x
        self.y_click = event.y

    def mover_janela(self, event):
        """
        Método chamado enquanto o usuário move o mouse com o botão esquerdo pressionado.

        Este método move a janela de acordo com a posição do mouse.

        Parâmetros:
            event (tkinter.Event): O evento de movimento do mouse.
        """

        # Calcula a nova posição da janela com base na posição do mouse
        x = self.winfo_pointerx() - self.x_click
        y = self.winfo_pointery() - self.y_click

        # Atualiza a posição da janela para a nova posição calculada
        self.geometry(f'+{x}+{y}')
