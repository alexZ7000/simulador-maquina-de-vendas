from src.shared.helpers.DevSystem import DevSystem
from src.shared.helpers.ScreenProperties import *

# Importação de imagens
vending_machine_image = PhotoImage(file=r"src/ui/assets/images/home/vending_machine.png")

class MaquinaDeVendas:
    """Lógica da máquina de vendas"""
    def __init__(self, home):
        self.estados = ['s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']
        self.entradas = {'m25': 0.25, 'm50': 0.50, 'm100': 1.00}
        self.estado_atual = 's0'
        self.saldo = 0.0
        self.home = home

    def inserir_moeda(self, valor):
        if valor in self.entradas.values():
            self.saldo += valor
            self.atualizar_estado()
            self.home.atualizar_saldo(f"Saldo atual: R$ {self.saldo:.2f}")
            self.verificar_saldo()
        else:
            self.home.atualizar_status("Moeda inválida.")

    def atualizar_estado(self):
        if self.saldo == 0:
            self.estado_atual = 's0'
        elif self.saldo == 0.25:
            self.estado_atual = 's1'
        elif self.saldo == 0.50:
            self.estado_atual = 's2'
        elif self.saldo == 0.75:
            self.estado_atual = 's3'
        elif self.saldo == 1.00:
            self.estado_atual = 's4'
        elif self.saldo == 1.25:
            self.estado_atual = 's5'
        elif self.saldo == 1.50:
            self.estado_atual = 's6'
        elif self.saldo == 1.75:
            self.estado_atual = 's7'
        elif self.saldo >= 2.00:
            self.estado_atual = 's8'
            self.home.atualizar_status("Saldo suficiente! Aperte o botão para retirar o refrigerante.")

    def verificar_saldo(self):
        if self.estado_atual == 's8':
            self.home.atualizar_status("Aperte o botão para dispensar o refrigerante.")
        else:
            restante = 2.00 - self.saldo
            self.home.atualizar_status(f"Insira mais R$ {restante:.2f}.")

    def dispensar_produto(self):
        if self.estado_atual == 's8':
            troco = self.saldo - 2.00
            self.home.atualizar_status("Dispensando refrigerante...")
            if troco > 0:
                self.home.atualizar_status(f"Dispensando troco: R$ {troco:.2f}")
            self.resetar_maquina()
        else:
            self.home.atualizar_status("Saldo insuficiente para dispensar o refrigerante.")

    def resetar_maquina(self):
        self.saldo = 0.0
        self.estado_atual = 's0'
        self.home.atualizar_saldo(f"Saldo atual: R$ {self.saldo:.2f}")
        self.home.atualizar_status("Máquina pronta para nova operação.")

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
               command=lambda: self.maquina.dispensar_produto).place(x=1100, y=500)

        # Rótulo de status
        self.status_label = Label(self.frame, font=("Arial", 14), text="Insira moedas.", background="#ccccff")
        self.status_label.place(x=500, y=600)

        # Rótulo de saldo
        self.saldo_label = Label(self.frame, font=("Arial", 14), text="Saldo atual: R$ 0.00", background="#ccccff")
        self.saldo_label.place(x=500, y=650)

        # Botão de saída
        Button(self.frame, font=("Arial", 14), text="Sair do App", cursor="hand2", command=self.confirm).place(x=1300, y=800)

# Criação do menu principal
menu_home = Home()
menu_home.show()
dev_system = DevSystem(menu_home)
menu_home.set_dev_system(DevSystem)

root.mainloop()
