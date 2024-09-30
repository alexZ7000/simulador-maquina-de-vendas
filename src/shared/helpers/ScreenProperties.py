from tkinter import *
from tkinter.messagebox import askyesno
import pygame.mixer

root = Tk()  # Janela
root.title("Máquina de Vendas")  # Título da janela
x, y = (root.winfo_screenwidth()), (root.winfo_screenheight())  # Pega a resolução do monitor sem considerar a escala
root.geometry(f'{x}x{y}')  # Dimensão da tela
root.minsize(1910, 1070)  # Resolução mínima para redimencionalizar
root.maxsize(1920, 1080)  # Forçar resolução Full HD (1920x1080) do DevQuiz
root.attributes("-fullscreen", 1)  # Colocar em tela cheia
frame = Frame(root)

pygame.mixer.init()

class ScreenProperties:
    """Classe que irá definir todos os itens que todos os "Menu" vão usar"""

    def __init__(self):
        """Criação da minha tela"""
        self.theme_txt = None
        self.dev_system = None
        self.frame = Frame(root, bg="#ccccff")
        self._build_screen()

    def set_dev_system(self, dev_system):
        """ Função para colocar os objetos referenciados no "DevSystem" em todas as Classes que herdarem de "Menu".
            :param dev_system: Pegar referencias
            :returns: Não retorna nada
        """
        self.dev_system = dev_system

    def show(self):
        """ Função para mostrar todos os widgets que forem "self.frame" """
        self.frame.pack(fill=BOTH, expand=True)

    def hide(self):
        """ Função para esconder widgets que não
        serão mais usados em uma tela nova e para
        excluir caracteres inseridos nos "Entry" """
        self.frame.forget()
        self.reset_entry()

    def _build_screen(self):
        """Função para construir minha tela"""
        pass

    def reset_entry(self):
        """Função para limpar os caracteres inseridos no "Entry" """
        pass
