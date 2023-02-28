from pathlib import Path
from subprocess import run as cmd

def build():
    vpk = "E:/SteamLibrary/steamapps/common/Left 4 Dead 2/bin/vpk.exe"
    root = Path("root")
    root_vpk = Path("root.vpk")
    out_vpk = Path("黑喵内鬼服骚话轮盘_挑衅和快速购买.vpk")

    if root_vpk.exists():
        root_vpk.unlink()
    if out_vpk.exists():
        out_vpk.unlink()
    cmd([vpk, root])
    root_vpk.rename(out_vpk)

if __name__ == "__main__":
    build()
