from pathlib import Path
from subprocess import run as cmd

def install():
    src_vpk = Path("黑喵内鬼服骚话轮盘_挑衅和快速购买.vpk")
    out_vpk = Path("E:/SteamLibrary/steamapps/common/Left 4 Dead 2/left4dead2/addons/黑喵内鬼服骚话轮盘_挑衅和快速购买.vpk")

    if not src_vpk.exists():
        print("没找到 vpk，先编译")
        return
    if out_vpk.exists():
        yes = True if input("同名 vpk 已存在，是否覆盖？[y/n] ").strip().lower().startswith("y") else False
        if not yes:
            return

    out_vpk.write_bytes(src_vpk.read_bytes())
    print(f"installed '{out_vpk!s}'")

if __name__ == "__main__":
    install()
