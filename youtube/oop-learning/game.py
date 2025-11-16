from pokemon import Pokemon


class Game:
    def __init__(self, pokemon1: Pokemon, pokemon2: Pokemon) -> None:
        self._pokemon1 = pokemon1
        self._pokemon2 = pokemon2

    def _start(self):
        print(
            f"{self._pokemon1.name}があらわれた！{self._pokemon1.name}のHPは{self._pokemon1.hp}だ！"
        )
        print(
            f"{self._pokemon2.name}があらわれた！{self._pokemon2.name}のHPは{self._pokemon2.hp}だ！"
        )

    def battle(self) -> None:
        self._start()
        winner, loser = self._attack()
        self._show_result(winner, loser)

    def _attack(self) -> tuple[Pokemon, Pokemon]:
        while True:
            self._pokemon1.attack(self._pokemon2)
            if self._pokemon2.is_fainted():
                return (self._pokemon1, self._pokemon2)

            self._pokemon2.attack(self._pokemon1)
            if self._pokemon1.is_fainted():
                return (self._pokemon2, self._pokemon1)

    def _show_result(self, winner: Pokemon, loser: Pokemon) -> None:
        print(f"{loser.name}はたおれた。{winner.name}のかち！")
