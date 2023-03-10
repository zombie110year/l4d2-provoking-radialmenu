from typing import Literal, Generator, Tuple
from io import StringIO


Direction = Literal["Center", "North", "NorthEast", "East", "SouthEast", "South", "SouthWest", "West", "NorthWest"]

class RadialPair:
    command: str
    text: str

    def __init__(self, command: str, text: str) -> None:
        self.command = command
        self.text = text

    @staticmethod
    def from_dict(d):
        if isinstance(d, dict):
            obj = RadialPair(d["command"], d["text"])
            return obj
        elif isinstance(d, RadialPair):
            return d


class RadialMenu:
    name: str
    team: Literal["Survivor"] | Literal["Infected"] | None
    alive: Literal["Alive"] | Literal["Dead"] | None

    Center: RadialPair | None
    North: RadialPair | None
    NorthEast: RadialPair | None
    East: RadialPair | None
    SouthEast: RadialPair | None
    South: RadialPair | None
    SouthWest: RadialPair | None
    West: RadialPair | None
    NorthWest: RadialPair | None

    SEQUENCE = ["Center", "North", "NorthEast", "East", "SouthEast", "South", "SouthWest", "West", "NorthWest"]

    def __init__(self, name: str) -> None:
        self.name = name
        self.team = None
        self.alive = None

        self.Center = None
        self.North = None
        self.NorthEast = None
        self.East = None
        self.SouthEast = None
        self.South = None
        self.SouthWest = None
        self.West = None
        self.NorthWest = None


    def pairs(self) -> Generator[Tuple[Direction, RadialPair], None, None]:
        for direction in self.SEQUENCE:
            obj = getattr(self, direction)
            if obj is None:
                continue

            yield (direction, obj)

    @staticmethod
    def from_dict(d):
        if isinstance(d, dict):
            obj = RadialMenu(d["name"])
            obj.team = d.get("team", None)
            obj.alive = d.get("alive", None)

            for dir in RadialMenu.SEQUENCE:
                pair = d.get(dir, None)
                if pair:
                    setattr(obj, dir, RadialPair.from_dict(pair))
            return obj
        elif isinstance(d, RadialMenu):
            return d


class Radials:
    contents: list[RadialMenu]

    def __init__(self, contents: list[RadialMenu]=None) -> None:
        if contents is None:
            self.contents = []
        else:
            self.contents = contents

    def add(self, menu: RadialMenu):
        self.contents.append(menu)

    def generate_config(self) -> str:
        "???????????????????????????????????????????????????<KEY> ?????????????????????????????????"
        template = '//bind <KEY> "+mouse_menu {name}"'
        names = set([c.name for c in self.contents])
        lines = [template.format(name=name) for name in names]
        return "\n".join(lines)

class Compiler:
    def __init__(self) -> None:
        self._indent = "\t"
        self._indent_level = 0
        self._nl = "\n"
        self._seperator = "\t"
        self._buf: StringIO | None = None

    def stringify(self, obj) -> str:
        self._buf = StringIO()
        if isinstance(obj, Radials):
            self.stringify_radials(obj)
        elif isinstance(obj, RadialMenu):
            self.stringify_radialmenu(obj)
        elif isinstance(obj, RadialPair):
            self.stringify_radialpair(obj)
        else:
            raise TypeError(f"??????????????? Radials, RadialMenu, RadialPair ?????????????????????{type(obj)}: {obj!r}")
        self._buf.seek(0, 0)
        text = self._buf.read()
        return text

    def stringify_radials(self, obj: Radials):
        self.write('"RadialMenu"')
        self.newline()
        self.write("{")
        self.indent()
        self.newline()
        for menu in obj.contents:
            self.write("//--------")
            self.newline()
            self.stringify_radialmenu(menu)
        self.unindent()
        self.newline()
        self.write("}")
        self.newline()

    def stringify_radialmenu(self, obj: RadialMenu):
        filters = ",".join(filter(lambda x: x is not None,
                         [obj.name, obj.team, obj.alive]))
        self.write(f'"{filters}"')
        self.newline()
        self.write("{")
        self.indent()
        self.newline()
        for direction, pair in obj.pairs():
            self.stringify_radialpair(pair, direction)
        self.unindent()
        self.newline()
        self.write("}")
        self.newline()


    def stringify_radialpair(self, obj: RadialPair, direction: str):
        self.write(f'"{direction}"')
        self.newline()
        self.write("{")
        self.indent()
        self.newline()
        self.write('"command"')
        self.seperate()
        self.write(f'"{obj.command}"')
        self.newline()
        self.write('"text"')
        self.seperate()
        self.write(f'"{obj.text}"')
        self.unindent()
        self.newline()
        self.write("}")
        self.newline()

    def indent(self):
        self._indent_level += 1

    def unindent(self):
        self._indent_level -= 1

    def newline(self):
        self._buf.write(self._nl)
        self._buf.write(self._indent * self._indent_level)

    def seperate(self):
        self._buf.write(self._seperator)

    def write(self, text: str):
        self._buf.write(text)


# ???????????????????????????????????????????????????
COMMANDS = {
    "null": RadialPair(";", "null"),
    # ??????
    "look": RadialPair("vocalize smartlook", "#L4D_rosetta_look"),
    "letsgo": RadialPair("vocalize PlayerMoveOn", "#L4D_rosetta_letsgo"),
    "youtakelead": RadialPair("vocalize PlayerLeadOn", "#L4D_rosetta_youtakelead"),
    "hurry": RadialPair("vocalize PlayerHurryUp", "#L4D_rosetta_hurry"),
    "nicejob": RadialPair("vocalize PlayerNiceJob", "#L4D_rosetta_nicejob"),
    "waithere": RadialPair("vocalize PlayerWaitHere", "#L4D_rosetta_waithere"),
    "totherescue": RadialPair("vocalize PlayerToTheRescue", "#L4D_rosetta_totherescue"),
    "becareful": RadialPair("vocalize PlayerWarnCareful", "#L4D_rosetta_becareful"),
    "withyou": RadialPair("vocalize PlayerImWithYou", "#L4D_rosetta_withyou"),
    "ready": RadialPair("vocalize PlayerAskReady", "#L4D_rosetta_ready"),
    "laugh": RadialPair("vocalize PlayerLaugh", "#L4D_rosetta_laugh"),
    "taunt": RadialPair("vocalize PlayerTaunt", "#L4D_rosetta_taunt"),
    "negative": RadialPair("vocalize PlayerNegative", "#L4D_rosetta_negative"),
    "no": RadialPair("vocalize PlayerNo", "#L4D_rosetta_no"),
    "sorry": RadialPair("vocalize PlayerSorry", "#L4D_rosetta_sorry"),
    "yes": RadialPair("vocalize PlayerYes", "#L4D_rosetta_yes"),
    "hurrah": RadialPair("vocalize PlayerHurrah", "#L4D_rosetta_hurrah"),
    "thankyou": RadialPair("vocalize PlayerThanks", "#L4D_rosetta_thankyou"),
    "grrrr": RadialPair("vocalize PlayerZombieTaunt", "#L4D_rosetta_grrrr"),
    "??????": RadialPair("say |??`) ??????????????????????????????;", "??????"),
    "?????????": RadialPair("say ( ????????) ?????????;", "?????????"),
    "666": RadialPair("say 666;", "666"),
    "?????????": RadialPair("say (?? ????????????????????????? ) ?????????;", "?????????"),
    # ???????????????
    "bm_??????hunter": RadialPair("say (????????????) ?????????????????????????????????;", "??????hunter"),
    "??????hunter": RadialPair("say ( ????????) ??????????????????hunter?????????~;", "??????hunter"),
    "????????????": RadialPair("say (????????????) ??????????????????????????????????????????~~;", "????????????"),
    "????????????": RadialPair("say ( ????????) ???????????????????????????~;", "????????????"),
    "??????tank": RadialPair("say (????????)????? ????????????????????????~~;", "??????tank"),
    "????????????": RadialPair("say |???????) ????????????????????????????????????????????????~;", "????????????"),
    "????????????": RadialPair("say ( ????????) ??????????????????????????????????????????~;", "????????????"),
    "bm_????????????": RadialPair("say ???(>??? <???)??? ?????????????????????????????????~~;", "????????????"),
    "bm_????????????": RadialPair("say (????????`)???*: ?????? ??????????????????????????????;", "????????????"),
    "????????????": RadialPair("say ??? ???('???^???) ????????????????????????????????????????????????~;", "????????????"),
    "????????????": RadialPair("say (????? ?????)??? ????????????.avi;", "????????????"),
    "bm_hunter??????": RadialPair("say (????????)???oo  ??? ????????????~~;", "Hunter??????"),
    "WRYYY": RadialPair("say ???(?????????'???)???WRYYYYYYYYYY!;", "WRYYY"),
    "????????????": RadialPair("say (???`????????).:?????????????????????HIGH??????????????????;", "????????????"),
    "sm_buy": RadialPair("sm_buy;", "????????????"),
    "bm_?????????": RadialPair("sm_buy; wait 15; menuselect 1; wait 15; menuselect 6; wait 15; menuselect 3; wait 15; menuselect 1; say (????? ?? ???`)????? ?????????????????????????????????????????????????????????;", "?????????"),
    "bm_????????????": RadialPair("sm_buy; wait 15; menuselect 3; wait 15; menuselect 2; wait 15; menuselect 1; say_team ????????????????????????????????????;", "????????????"),
    "bm_????????????": RadialPair("sm_buy; wait 15; menuselect 1; wait 15; menuselect 1; say o(>?? <)o??????????????????-???800???;", "??????"),
    "bm_???????????????": RadialPair("sm_buy; wait 15; menuselect 2; wait 15; menuselect 1;", "?????????"),
    "????????????": RadialPair("say ( ???) ????????????????????????????????????", "??????"),
    "?????????": RadialPair("say (????????)?????????~; vocalize PlayerLaugh;", "?????????"),
    "?????????": RadialPair("say ( ??>???<`) ???????????????????????????~~???~~; vocalize PlayerDeath;", "?????????"),
    "?????????": RadialPair("say_team (?? ????????????????????????? )????????????????????????; vocalize PlayerDeath;", "?????????"),
    "233": RadialPair("say *?????`)?????`)*?????`)?? ????????????23333~ (x ?? x); vocalize PlayerLaugh;", "233"),
    "??????": RadialPair("say_team o(>???<)o ???????????????????????????????????????????????????;", "??????"),
    "??????": RadialPair("say_team o(>???<)o ????????????????????????????????????????????????;", "??????"),
    "??????": RadialPair("say_team (??? ???? ??)??? ???? ??)??? ???? ??)??? ???? ??)????????????????????? ??????????????????????????????; vocalize PlayerYellRun;", "??????"),
    "?????????": RadialPair("say_team ??????????????????????????????; vocalize PlayerSorry", "?????????"),
}

ORDERS_SURVIVOR = RadialMenu.from_dict(
    {
        "name": "Orders",
        "team": "Survivor",
        "alive": "Alive",
        "Center": COMMANDS["look"],
        "North": COMMANDS["letsgo"],
        "NorthEast": COMMANDS["youtakelead"],
        "East": COMMANDS["hurry"],
        "SouthEast": COMMANDS["nicejob"],
        "South": COMMANDS["waithere"],
        "SouthWest": COMMANDS["totherescue"],
        "West": COMMANDS["becareful"],
        "NorthWest": COMMANDS["withyou"],
    }
)
QA_SURVIVOR = RadialMenu.from_dict(
    {
        "name": "QA",
        "team": "Survivor",
        "alive": "Alive",
        "Center": COMMANDS["ready"],
        "North": COMMANDS["laugh"],
        "NorthEast": COMMANDS["taunt"],
        "East": COMMANDS["negative"],
        "SouthEast": COMMANDS["no"],
        "South": COMMANDS["sorry"],
        "SouthWest": COMMANDS["yes"],
        "West": COMMANDS["hurrah"],
        "NorthWest": COMMANDS["thankyou"],
    }
)


# def ???????????????????????????(name: str, id: str) -> RadialMenu:
#     rp = RadialPair
#     RadialMenu.from_dict({
#         "name": f"bm_{id.lower()}",
#         "team": "Infected",
#         "Center": rp(f"say ????????????{name}??????????????????{name}?????????", "??????"),
#         "North": rp(f"say {name}"),
#         "NorthEast": rp(),
#         "East": rp(),
#         "SouthEast": rp(),
#         "South": rp(),
#         "SouthWest": rp(),
#         "West": rp(),
#         "NorthWest": rp(),
#     })

def main():
    x = Radials([ORDERS_SURVIVOR, QA_SURVIVOR])
    # ???????????????
    x.add(RadialMenu.from_dict({
        "name": "bm_provoke",
        "team": "Survivor",
        "Center": COMMANDS["????????????"],
        "North": COMMANDS["?????????"],
        "NorthEast": COMMANDS["666"],
        "East": COMMANDS["?????????"],
        "SouthEast": COMMANDS["bm_??????hunter"],
        "South": COMMANDS["??????hunter"],
        "SouthWest": COMMANDS["????????????"],
        "West": COMMANDS["????????????"],
        "NorthWest": COMMANDS["??????tank"],
    }))
    x.add(RadialMenu.from_dict({
        "name": "common_survivor",
        "team": "Survivor",
        "Center": COMMANDS["null"],
        "North": COMMANDS["233"],
        "NorthEast": COMMANDS["666"],
        "East": COMMANDS["?????????"],
        "SouthEast": COMMANDS["????????????"],
        "South": COMMANDS["??????"],
        "SouthWest": COMMANDS["??????"],
        "West": COMMANDS["??????"],
        "NorthWest": COMMANDS["?????????"],
    }))
    x.add(RadialMenu.from_dict({
        "name": "bm_provoke",
        "team": "Infected",
        "Center": COMMANDS["grrrr"],
        "North": COMMANDS["????????????"],
        "NorthEast": COMMANDS["bm_????????????"],
        "East": COMMANDS["bm_????????????"],
        "SouthEast": COMMANDS["????????????"],
        "South": COMMANDS["????????????"],
        "SouthWest": COMMANDS["bm_hunter??????"],
        "West": COMMANDS["WRYYY"],
        "NorthWest": COMMANDS["????????????"],
    }))
    x.add(RadialMenu.from_dict({
        "name": "bm_shop",
        "team": "Survivor",
        "alive": "Alive",

        # RadialPair(??????, ????????????)
        "Center": RadialPair("sm_buy;", "????????????"),
        "North": COMMANDS["bm_?????????"],
        "South": COMMANDS["bm_????????????"],
    }))
    x.add(RadialMenu.from_dict({
        "name": "bm_shop",
        "team": "Infected",
        "alive": "Alive",

        # RadialPair(??????, ????????????)
        "Center": RadialPair("sm_buy;", "????????????"),
        "North": COMMANDS["bm_????????????"],
        "South": COMMANDS["bm_???????????????"],
    }))
    cc = Compiler()
    text = cc.stringify(x)
    with open("root/scripts/radialmenu.txt", "wt", encoding="utf-8") as rm:
        rm.write(text)
    cfg = x.generate_config()
    print(cfg)


if __name__ == "__main__":
    main()
