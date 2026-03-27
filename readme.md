# 🌟 森空岛全自动签到脚本 (GitHub Actions 专版)

极其轻量级的森空岛每日自动签到脚本，专为 GitHub Actions 打造。无需本地服务器，无需复杂配置，云端自动运行。
由 https://github.com/kafuneri/Skland-Sign-In 项目修改而来

## ✨ 核心功能
* **双端支持**：一次配置，自动完成《明日方舟》与《明日方舟：终末地》的每日签到。
* **极致轻量**：剥离了所有本地配置和消息推送代码，只保留最纯粹的签到请求。
* **云端托管**：利用 GitHub Actions 每日定时执行，完全免费，解放双手。
* **多账号支持**：支持单账号或多账号同时签到。

---

## 📂 文件结构准备

在开始之前，请点右上角Fork到你自己的仓库，再确保你的代码仓库（**建议设置为 Private 私有仓库**）包含以下 4 个文件：

1.  `skland_api.py`：底层的 API 请求与加密处理文件（保持原样即可）。
2.  `main.py`：极简版的主运行逻辑脚本。
3.  `requirements.txt`：Python 依赖列表。
4.  `.github/workflows/sign-in.yml`：GitHub Actions 的自动化工作流配置文件（注意路径，`.github` 前面有个点）。

---
##  Token获取
1. 登录森空岛官网：https://www.skland.com/
2. 打开：https://web-api.skland.com/account/info/hg
3. 复制返回 JSON 中 content 字段的完整字符串，作为签到 Token

---
## 🚀 部署与使用指南

### 第一步：配置 Token (最重要的步骤)
千万**不要**把 Token 直接写在代码里！我们用Github自带的密钥管理。

1. 进入你的 GitHub 仓库主页。
2. 点击上方的 **Settings** (设置) 选项卡。
3. 在左侧边栏找到 **Secrets and variables**，展开后点击 **Actions**。
4. 点击绿色的 **New repository secret** 按钮。
5. 根据你的需求填写：
   * **如果是单账号**：
     * Name 填入：`SKLAND_TOKEN`
     * Secret 填入：你的 Token 字符串
   * **如果是多账号**：
     * Name 填入：`SKLAND_TOKENS`
     * Secret 填入：每行一个 Token，回车换行
   * 程序会优先解析多账号的token，多账号有东西单账号会直接跳过
6. 点击 **Add secret** 保存。

### 第二步：手动触发测试
配置好 Token 后，我们可以先手动跑一次看看效果：

1. 点击仓库上方的 **Actions** 选项卡。
2. (如果是第一次使用，可能会提示你需要开启 Actions 功能，点击绿色的确认按钮开启即可)。
3. 在左侧点击 **Skland Auto Sign In** 工作流。
4. 点击右侧的 **Run workflow** 下拉菜单，再点击绿色的 **Run workflow** 按钮。
5. 刷新页面，等待十几秒钟，点进刚刚运行的任务，展开 `Run sign in` 步骤的日志。如果你看到 `✅ 签到成功` 或 `今日已签到过了`，恭喜你，大功告成！🎉

### 第三步：享受全自动签到
确认手动运行成功后，你就不需要再做任何事情了。
根据 `.github/workflows/sign-in.yml` 中的配置，脚本默认会在**每天北京时间早上 5:00 (UTC 21:00)** 和
在**每天北京时间下午 1:00 (UTC 5:00)** 自动醒来为你签到。

---

## ⚠️ 注意事项与 FAQ

* **Token 会过期吗？**
  森空岛的 Token 有效期通常非常长（几个月甚至更久），只要你不主动在 App 里退出登录或修改密码，一般不需要频繁更换。如果某天发现 Actions 报错提示 Token 无效，重新抓包替换 Secret 即可。
* **我绑定的角色没有签到？**
  脚本会自动读取你 Token 绑定的**所有**角色。请确保你的森空岛账号确实已经绑定了方舟或终末地的游戏角色。

## 后记
  这个项目里api为 https://github.com/kafuneri/Skland-Sign-In 项目搬过来的，main.py为这个项目里同名文件修改来的。写这个代码有用到ai辅助，主要用作解析api、解读代码功能、文字编写。之前找了些自动签到，但我用的时候只签明日方舟，然后我就借鉴了一个库的代码写了一个