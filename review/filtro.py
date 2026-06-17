class FiltroPalavroes:
    # Lista de palavrões para censurar (só palavras em minúsculo)
    _lista_palavroes = [
        'porra',
        'caralho',
        'puta',
        'merda',
        'arrombado',
        'cu',
        'foder',
        'cacete',
    ]

    @classmethod
    def get_palavroes(cls):
        """ Pega a lista de palavrões """
        return cls._lista_palavroes

    @classmethod
    def has_palavroes(cls, texto):
        """ Verifica se tem há palavrões, se sim retorna True, se não retorna False """
        if texto is None:
            return False

        palavras_ruins = cls.get_palavroes()
        texto = texto.lower()

        for palavra in palavras_ruins:
            if palavra in texto:
                return True
        return False