class DevSystem:
    """Classe para referenciar objetos"""

    def __init__(self, menu_home):
        """Construtor"""
        self.menu_home = menu_home

    def get_reference(self, reference_name):
        """Função para pegar a referência dos objetos"""
        if reference_name == "menu_home":
            return self.menu_home
        else:
            raise Exception(f"reference_name not found, string name is wrong: {reference_name}")
