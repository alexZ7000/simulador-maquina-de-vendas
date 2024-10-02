from src.shared.helpers.DevSystem import DevSystem
from src.shared.helpers.ScreenProperties import *
from tkinter import messagebox

# Importação de imagens
vending_machine_image = PhotoImage(file=r"src/ui/assets/images/home/vending_machine.png")


# Estados possíveis da máquina
estados = {
    0: "R$0,00", 1: "R$0,25", 2: "R$0,50", 3: "R$0,75",
    4: "R$1,00", 5: "R$1,25", 6: "R$1,50", 7: "R$1,75", 8: "R$2,00"
}

# Função de transição e saída
transicoes = {
    (0, 'm25'): (1, 'n'), (0, 'm50'): (2, 'n'), (0, 'm100'): (4, 'n'), (0, 'b'): (0, 'n'),
    (1, 'm25'): (2, 'n'), (1, 'm50'): (3, 'n'), (1, 'm100'): (5, 'n'), (1, 'b'): (1, 'n'),
    (2, 'm25'): (3, 'n'), (2, 'm50'): (4, 'n'), (2, 'm100'): (6, 'n'), (2, 'b'): (2, 'n'),
    (3, 'm25'): (4, 'n'), (3, 'm50'): (5, 'n'), (3, 'm100'): (7, 'n'), (3, 'b'): (3, 'n'),
    (4, 'm25'): (5, 'n'), (4, 'm50'): (6, 'n'), (4, 'm100'): (8, 'n'), (4, 'b'): (0, 'r'),  # R$2,00 = refrigerante
    (5, 'm25'): (6, 'n'), (5, 'm50'): (7, 'n'), (5, 'm100'): (8, 't25'), (5, 'b'): (1, 'r'),  # R$2,25 -> refrigerante e troco R$0,25
    (6, 'm25'): (7, 'n'), (6, 'm50'): (8, 'n'), (6, 'm100'): (8, 't50'), (6, 'b'): (2, 'r'),  # R$2,50 -> refrigerante e troco R$0,50
    (7, 'm25'): (8, 'n'), (7, 'm50'): (8, 't25'), (7, 'm100'): (8, 't75'), (7, 'b'): (3, 'r'),  # R$2,75 -> refrigerante e troco R$0,75
    (8, 'm25'): (8, 't25'), (8, 'm50'): (8, 't50'), (8, 'm100'): (8, 't100'), (8, 'b'): (0, 'r')   # R$2,00 ou mais -> refrigerante
}

class MaquinaDeVendas:
    """Lógica da máquina de vendas"""
    def __init__(self, home):
        self.home = home
        self.estado_atual = 0

    def inserir_moeda(self, valor):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('src/ui/assets/sound/click.wav'))
        moedas = {'m25': 0.25, 'm50': 0.50, 'm100': 1.00}
        for entrada, val in moedas.items():
            if valor == val:
                self.estado_atual, output = transicoes.get((self.estado_atual, entrada), (self.estado_atual, 'n'))
                self.home.atualizar_saldo(f"Saldo atual: {estados[self.estado_atual]}")
                self.tratar_saida(output)
                return
        self.home.atualizar_status("Moeda inválida.")

    def tratar_saida(self, output):
        if output.startswith('t'):
            troco = output[1:]  # Ex.: 't25' -> troco de R$0,25
            messagebox.showinfo("Troco", f"Você recebeu {troco} de troco!")
        elif self.estado_atual == 8:
            messagebox.showinfo("Refrigerante", "Pressione o botão para retirar o refrigerante!")

    def dispensar_produto(self):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('src/ui/assets/sound/click.wav'))
        if self.estado_atual == 8:
            messagebox.showinfo("Refrigerante", "Refrigerante retirado!")
            self.estado_atual = 0
            self.home.atualizar_saldo(f"Saldo atual: {estados[self.estado_atual]}")
            self.home.atualizar_status("Máquina pronta para nova operação.")
        else:
            self.home.atualizar_status("Saldo insuficiente para dispensar o refrigerante.")

class Home(ScreenProperties):
    def __init__(self):
        super().__init__()
        self.maquina = MaquinaDeVendas(self)

    def atualizar_status(self, texto):
        """Atualiza a mensagem de status na tela"""
        self.status_label.config(text=texto)

    def atualizar_saldo(self, texto):
        """Atualiza o saldo na tela"""
        self.saldo_label.config(text=texto)

    def sumir_texto(self):
        pass

    def confirm(self):
        self.sumir_texto()
        """Função para exibir uma caixinha de confirmação ao usuário,
        para ele decidir se realmente quer sair"""
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('src/ui/assets/sound/click.wav'))
        self.resposta = askyesno(message='Você tem certeza que deseja sair?')
        if self.resposta:
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('src/ui/assets/sound/click.wav'))
            root.destroy()
        else:
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('src/ui/assets/sound/click.wav'))

    def _build_screen(self):
        """Função para construir a tela "Home" """
        Label(self.frame, image=vending_machine_image, width=256, background="#ccccff", height=256).place(x=x / 2 - 125,
                                                                                                          y=y / 2 - 356)

        # Botões para inserir moedas
        Button(self.frame, font=("Arial", 14), text="Inserir R$ 0.25", cursor="hand2",
               command=lambda: self.maquina.inserir_moeda(0.25)).place(x=500, y=500)
        Button(self.frame, font=("Arial", 14), text="Inserir R$ 0.50", cursor="hand2",
               command=lambda: self.maquina.inserir_moeda(0.50)).place(x=700, y=500)
        Button(self.frame, font=("Arial", 14), text="Inserir R$ 1.00", cursor="hand2",
               command=lambda: self.maquina.inserir_moeda(1.00)).place(x=900, y=500)

        # Botão para dispensar refrigerante
        Button(self.frame, font=("Arial", 14), text="Retirar refrigerante", cursor="hand2",
               command=lambda: self.maquina.dispensar_produto()).place(x=1100, y=500)

        # Rótulo de status
        self.status_label = Label(self.frame, font=("Arial", 14), text="Insira moedas.", background="#ccccff")
        self.status_label.place(x=500, y=600)

        # Rótulo de preço de refrigerante
        self.status_label = Label(self.frame, font=("Arial", 14), text="Refrigerante: 2,00 R$", background="#ccccff")
        self.status_label.place(x=500, y=650)

        # Rótulo de saldo
        self.saldo_label = Label(self.frame, font=("Arial", 14), text="Saldo atual: R$ 0.00", background="#ccccff")
        self.saldo_label.place(x=500, y=700)

        # Botão de saída
        Button(self.frame, font=("Arial", 14), text="Sair do App", cursor="hand2", command=self.confirm).place(x=1300, y=800)

# Criação do menu principal
menu_home = Home()
menu_home.show()
dev_system = DevSystem(menu_home)
menu_home.set_dev_system(DevSystem)

root.mainloop()
