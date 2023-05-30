import unittest
from io import StringIO
from unittest.mock import patch

from blackjack import Cards, Deck, Player, Blackjack


class BlackjackTest(unittest.TestCase):
    def setUp(self):
        self.cards = Cards(10, 1)  # 10 of Hearts
        self.deck = Deck()
        self.player = Player(False, self.deck)
        self.dealer = Player(True, self.deck)
        self.game = Blackjack()
    def test_deck_generate(self):
        self.deck.generate()
        self.assertEqual(len(self.deck.cards), 52)

    def test_deck_draw(self):
        self.deck.generate()
        cards = self.deck.draw(2)
        self.assertEqual(len(cards), 2)
        self.assertEqual(len(self.deck.cards), 50)

    def test_deck_count(self):
        self.deck.generate()
        self.assertEqual(self.deck.count(), 52)

    def test_player_check_score(self):
        self.player.cards = [self.cards, Cards(1, 2)]  # 10 of Hearts and Ace of Clubs
        self.assertEqual(self.player.check_score(), 21)

    @patch('sys.stdout', new_callable=StringIO)
    def test_blackjack_playAgain(self, fake_output):
        expected_output = "Good luck\n"
        with patch('builtins.input', side_effect=['n']):
            self.game.playAgain()
            self.assertEqual(fake_output.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
