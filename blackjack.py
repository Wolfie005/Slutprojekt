import random as rand


class Cards:
    """
    A class to represent the cards.

    ...

    Attributes
    ----------
    value : str
        Value of the card
    suit : str
        Suit of the card
    cost : str


    Methods
    -------
    show():
        Prints the card suit and value in a card.
    price():
        Returns the value of the card
    """

    def __init__(self, value, suit):
        """
        Constructs all the necessary attributes for the card object.

        Parameters
        ----------
        value : str
            Value of the card
        suit : str
            Suit of the card
        """

        self.suit = '♥♦♣♠'[suit]
        self.cost = value
        self.value = ['A ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', 'J ', 'Q ', 'K '][value - 1]

    def show(self):
        """
        Prints a card with its information.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        print('┌──────────┐')
        print(f'| {self.value}       |')
        print('|          |')
        print(f'|    {self.suit}     |')
        print('|          |')
        print(f'|       {self.value} |')
        print('└──────────┘')

    def price(self):
        """
        Returns the value of the card.

        Parameters
        ----------
        None

        Returns
        -------
        10 (int): If self.card is a 10, J, Q or K it returns 10.
        11 (int): If self.card is an Ace it returns 11.
        self.cost (int): Returns the value of the card.
        """

        if self.cost >= 10:
            return 10
        elif self.cost == 1:
            return 11
        return self.cost


class Deck:
    """
    A class to crate a card deck.

    ...

    Attributes
    ----------
    iteration : str
        Value of the card
    cards : list
        List of the cards the player have

    Methods
    -------
    generate():
        Genterated the deck
    draw():
        Removes the random card you get
    count():
        Counts the number of cards in the deck
    """

    def __init__(self):
        """
        Creates a list of the deck.

        Parameters
        ----------
        None
        """

        self.cards = []

    def generate(self):
        """
        Generates the cards and puts them in the deck.

        It creates a suit for every value.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        for v in range(1, 14):
            for s in range(4):
                self.cards.append(Cards(v, s))

    def draw(self, iteration):
        """
        It randomly picks a card for the player and removes it from the deck.

        Parameters
        ----------
        None

        Returns
        -------
        cards (list): Puts the card you got in the list called cards.
        """

        cards = []
        for i in range(iteration):
            card = rand.choice(self.cards)
            self.cards.remove(card)
            cards.append(card)
        return cards

    def count(self):
        """
        Count the number of cards in the deck.

        Parameters
        ----------
        None

        Returns
        -------
        len(self.cards) (int): The length of the cards list.
        """

        return len(self.cards)


class Player:
    """
    A class to crate the players (dealer and player).

    ...

    Attributes
    ----------
    isDealer : any
            The dealer
    deck : list
            Gives access to the deck

    Methods
    -------
    hit():
        Draws a card form the deck and checks their score.
    deal():
        Draw 2 card amd checks if it's a blackjack.
    check_score():
        Will add up the score of all the cards the player have. If the player have an Ace and their hand is over 21 it
        changes to a one
    show():
        Shows all the cards and the player score.
    """

    def __init__(self, isDealer, deck):
        """
        Creates the player hand, player score, gets the deck the dealer.

        Parameters
        ----------
        isDealer : any
                The dealer
        deck : list
                Gives access to the deck
        """

        self.cards = []
        self.isDealer = isDealer
        self.deck = deck
        self.score = 0

    def hit(self):
        """
        Draws a card from the deck to the players hand.

        Parameters
        ----------
        None

        Returns
        -------
        0 (int):
        1 (int):
        Returns 1 if the hand is bigger than 21. Else returns 0
        """

        self.cards.extend(self.deck.draw(1))
        self.check_score()
        if self.score > 21:
            return 1
        return 0

    def deal(self):
        """
        Deals out 2 cards to the player at the beginning.

        Parameters
        ----------
        None

        Returns
        -------
        Returns 1 if the score is 21. Else returns 0
        """

        self.cards.extend(self.deck.draw(2))
        self.check_score()
        if self.score == 21:
            return 1
        return 0

    def check_score(self):
        """
        Checks the score and add up the number of Aces. If the score is over 21 the Ace converts to a one.

        Parameters
        ----------
        None

        Returns
        -------
        The score of the player.
        """
        a_counter = 0
        self.score = 0
        for card in self.cards:
            if card.price() == 11:
                a_counter += 1
            self.score += card.price()

        while a_counter != 0 and self.score > 21:
            a_counter -= 1
            self.score -= 10
        return self.score

    def show(self):
        """
        Shows all the cards and the score of the player.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        if self.isDealer:
            print("Dealer's Cards")
        else:
            print("Player's Cards")

        for i in self.cards:
            i.show()

        print('Score: ' + str(self.score))


class Blackjack:
    """
    The game is generated here.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    play():
        Creates the game itself.
    """

    def __init__(self):
        """
        Shows all the card and the score of the player.

        Parameters
        ----------
        None
        """

        self.deck = Deck()
        self.deck.generate()
        self.player = Player(False, self.deck)
        self.dealer = Player(True, self.deck)

    def play(self):
        """
        Creates the game itself.

        The player and the dealer will be delt their cards. The player will show their cards and will check if it's a
        blackjack, if the player has a blackjack it will check if the dealer also has a blackjack if not the player
        wins. If the player doesn't have a blackjack, the player will have the option to Hit or Stand until they
        exceed 21. If the player stands, the dealer will draw a card until the score is over 17. If the dealer is over
        21 you win, otherwise the score will be compared and the higher score wins.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        p_status = self.player.deal()
        d_status = self.dealer.deal()

        self.player.show()

        if p_status == 1:
            print('Player got Blackjack! Congrats!')
            if d_status == 1:
                print("Dealer and Player got Blackjack! It's a push. (Tie)")
            return 1

        cmd = ''
        while cmd != 'stand':
            bust = 0
            cmd = input('Hit or Stand? > ')

            if cmd == 'hit':
                bust = self.player.hit()
                self.player.show()
            if bust == 1:
                print('Player busted. Good Game!')
                return 1
        print('\n')
        self.dealer.show()
        if d_status == 1:
            print('Dealer got Blackjack! Better luck next time!')
            return 1

        while self.dealer.check_score() < 17:
            if self.dealer.hit() == 1:
                self.dealer.show()
                print('Dealer busted. Congrats!')
                return 1
            self.dealer.show()

        if self.dealer.check_score() == self.player.check_score():
            print("It's a Push (Tie). Better luck next time!")
        elif self.dealer.check_score() > self.player.check_score():
            print('Dealer wins. Good Game!')
        elif self.dealer.check_score() < self.player.check_score():
            print('Player wins. Congratulations!')

    def playAgain(self):
        """
        Asks if you want to play again.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        cmd = ''
        while cmd != 'n':
            cmd = input('Wanna play again? (Y/N) > ')
            if cmd == 'y':
                Blackjack().play()
        print('Good luck')


