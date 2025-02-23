class Player:
    """
    Just a unique key ig. Prob could be cleaner
    """
    count = 0

    def __init__(self):
        self.ident = Player.count
        Player.count += 1