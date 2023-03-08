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
        "根据包含的菜单，生成几行配置模板，<KEY> 键表示需要绑定的快捷键"
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
            raise TypeError(f"只能序列化 Radials, RadialMenu, RadialPair 对象，但传入了{type(obj)}: {obj!r}")
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


# 游戏自带的默认指令和以前写的旧指令
COMMANDS = {
    # 原版
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
    "怂了": RadialPair("say |д`) 这可真是令人感到害怕;", "怂了"),
    "嘿嘿嘿": RadialPair("say ( ಡωಡ) 嘿嘿嘿;", "嘿嘿嘿"),
    "666": RadialPair("say 666;", "666"),
    "嘤嘤嘤": RadialPair("say (˚ ˃̣̣̥᷄⌓˂̣̣̥᷅ ) 嘤嘤嘤;", "嘤嘤嘤"),
    # 黑喵服务器
    "bm_挑衅hunter": RadialPair("say (●♡∀♡) 我蛋蛋好痒，快来捏我！;", "挑衅hunter"),
    "空爆hunter": RadialPair("say ( ಡωಡ) 嘿嘿嘿，就等hunter飞下来~;", "空爆hunter"),
    "挑衅牛牛": RadialPair("say (●♡∀♡) 有牛牛吗，有牛牛吗，快来撅我~~;", "挑衅牛牛"),
    "击倒冲锋": RadialPair("say ( ಡωಡ) 牛牛寸止挑战大成功~;", "击倒冲锋"),
    "胆汁tank": RadialPair("say (ಡωಡ)っθ 吃我秘制小汉堡儿~~;", "胆汁tank"),
    "暗中观察": RadialPair("say |ω・´) 看看是哪个倒霉鬼要被我下一个整呢~;", "暗中观察"),
    "牛牛秒杀": RadialPair("say ( ಡωಡ) 牛牛速运已结束，用户默认好评~;", "牛牛秒杀"),
    "bm_猴子秒杀": RadialPair("say ヽ(>∀ <☆)ノ 这是沸↓羊↑羊↑的感觉~~;", "猴子秒杀"),
    "bm_胖子秒杀": RadialPair("say (ﾉ´ヮ`)ﾉ*: ･ﾟ 弹射起飞，体验良好！;", "胖子秒杀"),
    "口水高伤": RadialPair("say ☆ ～('▽^人) 一口老痰，这酸爽简直让人无法相信~;", "口水高伤"),
    "舌头拉人": RadialPair("say (ﾉ´ з—)— 亚洲捆绑.avi;", "舌头拉人"),
    "bm_hunter高扑": RadialPair("say (ಡωಡ)っoo  ∩ 蛋蛋没咯~~;", "Hunter高扑"),
    "WRYYY": RadialPair("say ╰(●｀∀'●)╯WRYYYYYYYYYY!;", "WRYYY"),
    "嗨到不行": RadialPair("say (・`∀´・).:☆我累哇赛高尼HIGH↑铁鸭子哒！;", "嗨到不行"),
    "sm_buy": RadialPair("sm_buy;", "一键购买"),
    "bm_买胆汁": RadialPair("sm_buy; wait 15; menuselect 1; wait 15; menuselect 6; wait 15; menuselect 3; wait 15; menuselect 1; say (´• ω •`)っθ 臭豆腐、俘虏、老干妈，往里倒罐臭卤虾！;", "买胆汁"),
    "bm_买电击器": RadialPair("sm_buy; wait 15; menuselect 3; wait 15; menuselect 2; wait 15; menuselect 1; say_team 买电击器了，尸体在哪里？;", "买电击器"),
    "bm_特感买血": RadialPair("sm_buy; wait 15; menuselect 1; wait 15; menuselect 1; say o(>ω <)o满血复活！（-￥600）;", "买血"),
    "bm_特感买自杀": RadialPair("sm_buy; wait 15; menuselect 2; wait 15; menuselect 1;", "买自杀"),
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


# def 黑喵特感针对某玩家(name: str, id: str) -> RadialMenu:
#     rp = RadialPair
#     RadialMenu.from_dict({
#         "name": f"bm_{id.lower()}",
#         "team": "Infected",
#         "Center": rp(f"say 嘿嘿嘿，{name}酱……可爱的{name}酱……", "发癫"),
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
    # 黑喵、挑衅
    x.add(RadialMenu.from_dict({
        "name": "bm_provoke",
        "team": "Survivor",
        "Center": COMMANDS["怂了"],
        "North": COMMANDS["嘿嘿嘿"],
        "NorthEast": COMMANDS["666"],
        "East": COMMANDS["嘤嘤嘤"],
        "SouthEast": COMMANDS["bm_挑衅hunter"],
        "South": COMMANDS["空爆hunter"],
        "SouthWest": COMMANDS["挑衅牛牛"],
        "West": COMMANDS["击倒冲锋"],
        "NorthWest": COMMANDS["胆汁tank"],
    }))
    x.add(RadialMenu.from_dict({
        "name": "bm_provoke",
        "team": "Infected",
        "Center": COMMANDS["暗中观察"],
        "North": COMMANDS["牛牛秒杀"],
        "NorthEast": COMMANDS["bm_猴子秒杀"],
        "East": COMMANDS["bm_胖子秒杀"],
        "SouthEast": COMMANDS["口水高伤"],
        "South": COMMANDS["舌头拉人"],
        "SouthWest": COMMANDS["bm_hunter高扑"],
        "West": COMMANDS["WRYYY"],
        "NorthWest": COMMANDS["嗨到不行"],
    }))
    x.add(RadialMenu.from_dict({
        "name": "bm_shop",
        "team": "Survivor",
        "alive": "Alive",

        # RadialPair(指令, 显示文本)
        "Center": RadialPair(";", "快捷商店"),
        "North": COMMANDS["bm_买胆汁"],
        "South": COMMANDS["bm_买电击器"],
    }))
    x.add(RadialMenu.from_dict({
        "name": "bm_shop",
        "team": "Infected",
        "alive": "Alive",

        # RadialPair(指令, 显示文本)
        "Center": RadialPair(";", "快捷商店"),
        "North": COMMANDS["bm_特感买血"],
        "South": COMMANDS["bm_特感买自杀"],
    }))
    cc = Compiler()
    text = cc.stringify(x)
    with open("root/scripts/radialmenu.txt", "wt", encoding="utf-8") as rm:
        rm.write(text)
    cfg = x.generate_config()
    print(cfg)


if __name__ == "__main__":
    main()
