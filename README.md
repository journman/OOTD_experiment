# 双塔防小游戏 · OODT Mini Games

两个独立运行的 Python / pygame 面向对象课程项目，也提供 Windows 64 位免安装版。

| 游戏 | 内容 |
| --- | --- |
| 植物大战僵尸 | 14 个关卡、16 种植物、5 种僵尸；昼夜场景、选卡、选关、逐关解锁与进度保存 |
| 保卫萝卜 / 保卫水果 | 2 个连续关卡、3 种水果防御塔、4 种怪物；金币、生命值与击杀统计 |

## 下载即玩

打开 [Releases 下载页](https://github.com/wlc221222-creator/oodt-mini-games/releases/latest)：

- **两个游戏一起下载**：`oodt-mini-games-windows-x64.zip`。
- **只下载植物大战僵尸**：`plants-vs-zombies-windows-x64.zip`。
- **只下载保卫萝卜**：`defend-carrot-windows-x64.zip`。
- **源码压缩包**：`oodt-mini-games-source.zip`，或点击仓库的 Code → Download ZIP。

Windows 10/11 64 位：解压后双击对应 `.exe`；不需要安装 Python、pygame 或其他运行库。发布包不包含个人存档，新玩家从 1-1 和两种基础植物开始。

植物大战僵尸 EXE 版的存档位置：

```text
%LOCALAPPDATA%\OODTMiniGames\PlantsVsZombies\savegame.json
```

源码运行时，存档保存在 `plants_vs_zombies/savegame.json`。进度逐关保存，通关奖励依次解锁；冒险通关后可在地图重玩已解锁关卡。

## 操作

### 植物大战僵尸

- 主菜单点击“植物与僵尸图鉴”，或在任意界面按 `I` 查看全部 16 种植物和 5 种僵尸的介绍。`Tab` 切换分类，`←` / `→` 翻页，`I` / `Esc` 或返回按钮关闭；查看时战斗暂停，关闭后继续。未解锁植物可查看介绍，仍需冒险通关获得。
- 主菜单：点击冒险模式继续闯关，或点击选择关卡打开地图。
- 选卡：点击植物加入阵容，点击已选卡片移除；`A` 快速选满，`Enter` 开始。
- 战斗：`1`–`8` 选择卡片；左键种植或收集阳光；右键取消选择。五行草坪从第一关起全部可种，选卡后显示格子与落点预览；冷却、阳光不足和格子占用会显示原因。
- 通关：点击“下一关”或按 `Enter` 继续；`R` 重试当前关卡。
- `F` 切换全屏；`Esc` 退出全屏 / 返回庭院，主菜单按 `Esc` 退出。

前七关分别为：五路初战、两翼夹击、极速突袭、重甲攻坚、阳光补给、无光之夜、月下决战。
选卡页显示本关规则；战斗中显示波次名称、清波后的倒计时和即将来袭的行。
极速突袭的僵尸移速提高 30%；补给关清波获得阳光；夜间关卡不再掉落天降阳光，需要向日葵维持经济。
原有存档、植物奖励和逐关解锁顺序保持兼容。

夜战扩展新增 2-3 至 2-9 七关，小喷菇、阳光菇、胆小菇、大嘴花、窝瓜、地刺、寒冰菇，以及旗帜僵尸和读报僵尸。
地图与种子册均支持左右按钮或 `←` / `→` 翻页；鼠标停在种子卡上查看能力。
新增植物仍通过冒险通关解锁，寒冰菇在 2-9 后解锁，可重玩夜间关卡试用。
旧七关已通关的存档加载后可直接继续 2-3。各品种机制、数值缩放和解锁顺序见 [夜战扩展说明](plants_vs_zombies/EXPANSION.md)。

### 保卫萝卜 / 保卫水果

- 点击右下角“水果与怪物图鉴”或按 `I` 查看名称、攻击点数、怪物速度与生命值；查看时暂停战斗，`I` / `Esc` 或返回按钮继续。
- 击杀怪物获得金币、累计积分和击杀数；到达终点的怪物只扣萝卜生命，不发奖励。建塔花费金币，不扣累计积分；积分在本次两关挑战内累计，重开后清零。
- `1`–`3` 选择防御水果，左键在空草地建造；路径和萝卜位置不能建造。
- 右键取消选择；胜负界面点击或按 `R` 重新开始；`Esc` 退出。
- 第一关结束后自动进入第二关。

## 截图

截图展示不同解锁阶段，发布包不附带这些测试进度。

![植物大战僵尸菜单](docs/screenshots/pvz-menu.png)
![植物大战僵尸关卡地图](docs/screenshots/pvz-map.png)
![植物大战僵尸夜战](docs/screenshots/pvz-night.png)
![保卫萝卜](docs/screenshots/defend-carrot.png)

## 从源码运行

需要 Python 3.12 或更高版本，以及 `requirements.txt` 中的依赖。Python 3.14
会自动安装提供相同 `pygame` 导入模块的 `pygame-ce`，避免从源码编译旧版
pygame；Python 3.12/3.13 使用 pygame 2.6.1。

```bash
python -m pip install -r requirements.txt
python plants_vs_zombies/main.py
python defend_carrot/main.py
```

两个游戏使用各自的 `config.py`、`entities.py` 和 `Game` 控制器；从各自入口独立运行。

## 验证

```bash
python plants_vs_zombies/tests/test_adventure_flow.py
python plants_vs_zombies/tests/test_ui_flow.py
python plants_vs_zombies/tests/test_progress.py
python plants_vs_zombies/tests/test_packaged_save.py
python plants_vs_zombies/tests/test_gameplay_revision.py
python plants_vs_zombies/tests/test_level_balance.py
python plants_vs_zombies/tests/test_expansion.py
python defend_carrot/tests/test_smoke.py
```

完整植物大战僵尸战斗测试可通过 `python tools/test_source.py` 运行，测试存档隔离在临时目录中。

## 自行生成 Windows EXE

在 Windows 64 位 Python 3.12 环境中：

```bash
python -m pip install -r requirements-build.txt
python tools/build_windows.py
```

构建输出为 `dist/PlantsVsZombies.exe` 和 `dist/DefendCarrot.exe`。构建脚本会运行实际 EXE 自检，确认素材加载、初始关卡、种植/建造和渲染可用。

## 面向对象结构

- `Entity` 抽象基类：统一更新与绘制接口。
- 具体植物 / 水果 / 怪物类：封装各自行为，用继承和多态组织对象。
- `Game`：协调实体、输入、经济、关卡与胜负状态。
- 植物大战僵尸的 `assets.py` 与 `garden_ui.py`：集中管理素材与界面表现。

## 素材来源

植物大战僵尸图片来自参考项目 [marblexu/PythonPlantsVsZombies](https://github.com/marblexu/PythonPlantsVsZombies) 中的素材包，相关角色与美术归原权利人。此仓库用于课程学习与非商业演示；第三方素材的权利和来源说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。保卫萝卜项目的画面由程序绘制。
