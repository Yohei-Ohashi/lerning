class Pokemon:
    def __init__(self, name: str, hp: int, speed: int, atk: int) -> None:
        self._name = name
        self._hp = hp
        self._max_hp = hp * 2
        self._atk = atk
        self._speed = speed

    @property
    def name(self) -> str:
        return self._name

    @property
    def hp(self) -> int:
        return self._hp
    
    @property
    def speed(self) -> int:
        return self._speed

    @hp.setter
    def hp(self, value: int) -> None:
        if value < 0:
            self._hp = 0
        elif value > self._max_hp:
            self._hp = self._max_hp
        else:
            self._hp = value

    def attack(self, target: "Pokemon") -> None:
        target.hp -= self._atk
        print(f"{self._name}のこうげき！", end="")
        self.attack_message(target)

    def attack_message(self, target: "Pokemon") -> None:
        pass

    def is_fainted(self) -> bool:
        return self._hp <= 0


class Pikachu(Pokemon):
    def __init__(self) -> None:
        super().__init__("ピカチュウ", 20, 12, 10)

    def attack_message(self, target: "Pokemon") -> None:
        print(
            f"10万ボルト！{target.name}は{self._atk}ダメージをもらった！{target.name}のHPは{target.hp}だ！"
        )


class Hitokage(Pokemon):
    def __init__(self) -> None:
        super().__init__("ヒトカゲ", 18, 12, 5)

    def attack_message(self, target: "Pokemon") -> None:
        print(
            f"ひのこ！{target.name}は{self._atk}ダメージをもらった！{target.name}のHPは{target.hp}だ！"
        )
