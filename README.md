# 为 L4D2 编写的挑衅与快捷购买的轮盘选单 MOD

参考了 ion's vocalizer 这个 MOD，其中的编写方式可以看看 [ion_radialmenu](references/ion_radialmenu.txt)。
如果要自行修改喊话内容和指令，可以直接在 [radialmenu.txt](root/scripts/radialmenu.txt) 里编辑。
注意，`say xxx` 之后需要添加英文分号 `;`，否则喊话内容末尾会出现诸如 `123#` 的随机数字。

## 安装

将此项目生成的 VPK 文件放在 `Left 4 Dead 2/left4dead2/addons` 文件夹之下。
然后在 `Left 4 Dead 2/left4dead2/cfg/autoexec.cfg` 文件里添加快捷键绑定相关配置（如果没有此文件，直接新建一个纯文本文件即可）：

```
bind v "+mouse_menu bm_provoke"; // 挑衅相关喊话
bind b "+mouse_menu bm_shop";    // 快捷商店
```

### 使用 Python 脚本

在本项目中，如果需要自行修改部分内容并重新生成 VPK，需要先配置以下选项：

1. 确认你安装了 Left 4 Dead 2 Authoring Tools，主要是需要利用此软件包中的 `vpk.exe` 工序来打包 VPK；一般来说，只要在 Steam 上购买了求生之路2，就会送（不会默认安装），只需要手动安装即可。
2. 将 `vpk.exe` 的路径填入到 `build.py` 文件的 `vpk` 变量中，这是为了让 Python 能找到程序并调用。
3. 将 `install.py` 文件里的 `out_vpk` 替换成你的求生之路 MOD 安装路径，这样，就能直接 `python install.py` 安装了。

修改内容需要编辑 `generate.py` 脚本，在 `main` 函数里按照前面的格式添加 `RadialMenu` 对象即可，注意 `COMMANDS[...]` 是直接引用前面写好的指令，如果要自定义，需要创建 `RadialPair` 对象。

```sh
# 编辑过 generate.py 脚本后，运行该脚本生成 radialmenus.txt 文件
python generate.py
# 运行 vpk 打包
python build.py
# 根据配置好的路径信息将 VPK 复制到对应位置，如果需要覆盖，按 y + 回车，如果要放弃，直接回车
python install.py
```

generate 时会显示对应的配置项，每一行前面的 `//` 是求生之路控制台的注释，去掉才可以执行。
按需将其绑定在对应按键上即可，按键代码可以查 [Valve 开发文档]<https://developer.valvesoftware.com/wiki/Bind#Special_Keys> 。

Orders 和 QA 是游戏自带的，`bm_provoke` 和 `bm_shop` 是我自用的。

```
//bind <KEY> "+mouse_menu Orders"
//bind <KEY> "+mouse_menu bm_provoke"
//bind <KEY> "+mouse_menu bm_shop"
//bind <KEY> "+mouse_menu QA"
```

## 使用

在游戏里，按住 `v` 或 `b` 键就可打开轮盘，移动鼠标选择要发送的话题，松开 `v` 或 `b` 键即可发送。

其中 `b`（shop）功能需要生还者或特感存活才能使用。
