# MC Key Macro

我的世界键鼠宏小工具：一个置顶的半透明小窗，通过快捷键启停两组固定键鼠操作。

## 功能

| 快捷键 | 模式 | 行为 |
|---|---|---|
| `F9` | 万箭模式 | 循环执行：按 `2` → 右键按住 700ms → 按 `1` → 左键连点 6 次（间隔 0.2s） |
| `F12` | 左键 + 空格常驻 | 按住空格，同时每 0.2s 左键点击一次 |
| `F10` | 退出 | 停止所有循环并强制松开空格、`1`、`2`、左右键 |

- 两种模式互斥，运行中按另一个模式的快捷键无效
- 窗口置顶、半透明、无边框，尺寸 100×25
- 退出时统一释放按键，避免卡键

## 运行

```bash
pip install pynput
python atou.pyw
```

不想显示控制台窗口可以用：

```bash
pythonw atou.pyw
```

## 打包

```bash
pip install pyinstaller
pyinstaller atou.spec
```

产物为 `dist/atou.exe`（约 11 MB，单文件）。

## 项目结构

```
qqq/
├── atou.pyw        # 主程序（tkinter GUI + pynput 键鼠控制）
├── atou.spec       # PyInstaller 打包配置
├── mc_icon.ico     # 程序图标
└── README.md
```

## 说明

- 这是**固定键鼠宏**，不含图像识别，不判断游戏画面
- 按键 `1`、`2` 和鼠标操作是按默认键位写死的，改键位需要修改 `atou.pyw` 里的 `macro_loop()`
- 需要游戏窗口处于前台，宏会向当前活动窗口发送按键

## 免责声明

本项目仅供学习 tkinter、pynput 和 PyInstaller 使用。在多人服务器使用宏可能违反服务器规则，请自行确认并承担风险。
