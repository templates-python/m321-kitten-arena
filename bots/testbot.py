import json
import time


class TestBot:
    """
    This is a helper class to run the bot in the local environment.
    The name MUST match the filename.
    """

    def __init__(self, name="TestKitten", error=None, timeout=3, standard_response="ACK", invalid_standard_response="OK"):
        self.name = name
        self._bot = TestKitten(name, error, standard_response, invalid_standard_response)
        self._timeout = timeout
        self._error = error

    def request(self, data):
        """
        Request for a response

        If data contains an attribute forced_action, the bot will always return that value.
        If data contains an attribute timeout and the value of it is true, it will wait the amount of ms defined on
        initialization of the Bot.

        :param data:
        :return:
        """

        if isinstance(data, dict):
            payload = data
        else:
            payload = json.loads(data)

        if self._error == "TIMEOUT_ERROR":
            print(f"{self._bot.name}: Timeout due to self._timeout ({self._timeout}s)")
            time.sleep(self._timeout)

        if "timeout" in payload:
            print(f"{self._bot.name}: Timeout due to parameter 'timeout' in data ({payload["timeout"]}s)")
            time.sleep(payload["timeout"])

        # lets you define, how the bot should respond (for testing)
        if "forced_response" in payload:
            return payload["forced_response"]

        action = payload["action"]
        if action == "PLAY":
            return self._bot.play(payload)

        elif action == "START":
            return self._bot.start_round(payload)

        elif action == "DRAW":
            return self._bot.draw(payload)

        elif action == "INFORM":
            return self._bot.inform(payload)

        elif action == "DEFUSE" or action == "PLACE":
            return self._bot.defuse(payload)

        elif action == "FUTURE":
            return self._bot.see_the_future(payload)

        elif action == "EXPLODE":
            return self._bot.explode()

        elif action == "GAMEOVER":
            return self._bot.gameover()

        print(f"Unknown Action: \n\n{action}\n\n")
        return None


class TestKitten:
    """
    This bot tests the arena on a given error. Possible errors:
    - INVALID_RESPONSE
    - PLAY_NONEXISTENT_CARD
    - TIMEOUT_ERROR
    """

    def __init__(self, name, error=None, standard_response="ACK", invalid_standard_response="OK"):
        self._name = name
        self._error = error

        if self._error == "INVALID_RESPONSE":
            self._standard_response = invalid_standard_response
        else:
            self._standard_response = standard_response

        self._hand = []

    def start_round(self, payload):
        """
        Function that is called when the game starts

        :param payload: information about gamestart
        :return "ACK": OK string
        """
        return self._standard_response

    def play(self, payload):
        """
        Function that is called when the bot needs to play

        :param payload: information about the game state
        :return card_name: name of card
        """
        if self._error == "PLAY_NONEXISTENT_CARD":
            return self.play_nonexistent()
        elif self._error == "INVALID_RESPONSE":
            return self._standard_response
        else:
            return self._hand[0]

    def draw(self, payload):
        """
        Function that is called when the bot draws a card

        :param payload: information about the game state
        :return "ACK": OK string
        """
        card = payload["card"]

        self._hand.append(card)

        return self._standard_response

    def inform(self, payload):
        """
        Function that is called when something happens in the game

        :param payload: information about the game state
        :return "ACK": OK string
        """
        return self._standard_response

    def defuse(self, payload):
        """
        Function that is called when the bot needs to defuse

        :param payload: information about the game state
        :return position: position where in the deck the EXPLODING_KITTEN is placed
        """
        return self._standard_response

    def see_the_future(self, payload):
        """
        Function that is called when the bot played a future card

        :param payload: information about the next three cards
        :return "ACK": OK string
        """
        return self._standard_response

    def explode(self):
        """
        Function that is called when the bot explodes

        :return "ACK": OK string
        """
        return self._standard_response

    def gameover(self):
        """
        Function that is called when the game is over

        :return "ACK": OK string
        """
        return self._standard_response

    def play_nonexistent(self):
        list_of_cards = [
            "NORMAL",
            "SKIP",
            "SHUFFLE",
            "DEFUSE",
            "SEE_THE_FUTURE",
            "EXPLODING_KITTEN",
        ]

        for card in list_of_cards:
            if card not in self._hand:
                print(f"{self._name}: Play nonexistent card from Deck ({card})")
                return card

    @property
    def name(self):
        return self._name


if __name__ == "__main__":
    normal_bot = TestBot("NormalBot")
    timeout_bot = TestBot("TimeoutKitten", "TIMEOUT_ERROR")
    invalid_bot = TestBot("InvalidKitten", "INVALID_RESPONSE")
    nonexistent_bot = TestBot("NonexistentKitten", "PLAY_NONEXISTENT_CARD")

    data = {
        # "forced_response": "Okidoki",
        "timeout": 1,
        "action": "DRAW",
        "card": "SKIP"
    }

    print("\n====================================================\nDRAW: \n")
    print(normal_bot.request(data))
    print(timeout_bot.request(data))
    print(invalid_bot.request(data))
    print(nonexistent_bot.request(data))

    data1 = {
        "action": "PLAY"
    }

    print("\n====================================================\nPLAY: \n")
    print(normal_bot.request(data1))
    print(timeout_bot.request(data1))
    print(invalid_bot.request(data1))
    print(nonexistent_bot.request(data1))
