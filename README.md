# 为 L4D2 编写的挑衅与快捷购买的轮盘选单 MOD

参考了 ion's vocalizer 这个 MOD，其中的编写方式可以看看 [ion_radialmenu](references/ion_radialmenu.txt)。
如果要自行修改喊话内容和指令，可以直接在 [radialmenu.txt](root/scripts/radialmenu.txt) 里编辑。
注意，`say xxx` 之后需要添加英文分号 `;`，否则喊话内容末尾会出现诸如 `123#` 的随机数字。

## 安装

将此 MOD 的 VPK 文件放在 `Left 4 Dead 2/left4dead2/addons` 文件夹之下。
然后在 `Left 4 Dead 2/left4dead2/cfg/autoexec.cfg` 文件里添加（如果没有此文件，直接新建一个纯文本文件即可）：

```
bind v "+mouse_menu provoke"; // 挑衅相关喊话
bind b "+mouse_menu shop";    // 快捷商店
```

## 使用

在游戏里，按住 `v` 或 `b` 键就可打开轮盘，移动鼠标选择要发送的话题，松开 `v` 或 `b` 键即可发送。

其中 `b`（shop）功能需要生还者或特感存活才能使用。
