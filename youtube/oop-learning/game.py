from pokemon import Pokemon
import random

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
    
    def _determine_attack_order(self) -> tuple[Pokemon, Pokemon]:
        speed1 = self._pokemon1.speed
        speed2 = self._pokemon2.speed
        
        if speed1 > speed2:
            # pokemon1の方が素早い
            return (self._pokemon1, self._pokemon2)
        elif speed2 > speed1:
            # pokemon2の方が素早い
            return (self._pokemon2, self._pokemon1)
        else:
            if random.random() < 0.5:
                return (self._pokemon1, self._pokemon2)
            else:
                return (self._pokemon2, self._pokemon1)

    def _attack(self) -> tuple[Pokemon, Pokemon]:
        while True:
            fast_pokemon, slow_pokemon = self._determine_attack_order()
            fast_pokemon.attack(slow_pokemon)
            if slow_pokemon.is_fainted():
                return (fast_pokemon, slow_pokemon)

            slow_pokemon.attack(fast_pokemon)
            if fast_pokemon.is_fainted():
                return (slow_pokemon, fast_pokemon)

    def _show_result(self, winner: Pokemon, loser: Pokemon) -> None:
        print(f"{loser.name}はたおれた。{winner.name}のかち！")
