def appearance(my_pokemon, enemy_pokemon):
    print(f"{my_pokemon["name"]}があらわれた。{my_pokemon["name"]}のHPは{my_pokemon["hp"]}だ。")
    print(f"{enemy_pokemon["name"]}があらわれた。{enemy_pokemon["name"]}のHPは{enemy_pokemon["hp"]}だ。")

def calc_hp(atk_pokemon, def_pokemon):
    def_hp = def_pokemon["hp"]
    
    if def_hp - atk_pokemon["atk"][0][1] > 0:
        def_hp -= atk_pokemon["atk"][0][1]
        return def_hp 
    else:
        return 0
    

def battle(my_pokemon, enemy_pokemon):
    print(f"{my_pokemon["name"]}のこうげき！{my_pokemon["atk"][0][0]}！{enemy_pokemon["name"]}は{my_pokemon["atk"][0][1]}ダメージをもらった。{enemy_pokemon["name"]}のHPは{calc_hp(my_pokemon, enemy_pokemon)}だ。")

def main():
    pikachu = {
        "name": "ピカチュウ",
        "hp": 20,
        "atk": [
            ["10万ボルト", 10]
        ]
    }
    hitokage = {
        "name": "ヒトカゲ",
        "hp": 18,
        "atk": {
            "ひのこ": 5
        }
    }
    
    appearance(pikachu, hitokage)
    battle(pikachu, hitokage)

if __name__ in "__main__":
    main()

ex_output = """ピカチュウがあらわれた。ピカチュウのHPは20だ。
ヒトカゲがあらわれた。ヒトカゲのHPは18だ。
ピカチュウのこうげき！10万ボルト！ヒトカゲは10ダメージをもらった。ヒトカゲのHPは8だ。
ヒトカゲのこうげき！10万ボルト！ピカチュウは5ダメージをもらった。ピカチュウのHPは15だ。
ピカチュウのこうげき！10万ボルト！ヒトカゲは10ダメージをもらった。ヒトカゲのHPは0だ。
ヒトカゲはたおれた。ピカチュウのかち！
"""