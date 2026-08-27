# 足球记录分析小程序 · GitHub Pages 部署说明

这是一个纯前端 PWA 小程序，可直接部署到 GitHub Pages 永久托管，并获得一个**永不过期的稳定网址**，可分享给任何人。

## 一、需要你做的（一次性，约 5 分钟）

1. **注册 GitHub**（免费）：到 https://github.com 注册一个账号。
2. **新建仓库**：右上角 `+` → `New repository`
   - Repository name：`football-miniapp`（可自定义）
   - 选择 **Public**（免费托管必须公开）
   - 不勾选任何初始化选项（README/license 都别勾，保持空仓库）
   - 点 `Create repository`
3. **生成授权令牌（Token）**（用于让我帮你推送代码）：
   - 右上角头像 → `Settings` → 左侧最底部 `Developer settings`
   - → `Personal access tokens` → `Tokens (classic)` → `Generate new token`
   - Note 随便填（如 `deploy-football`），Expiration 选 7 天
   - 勾选权限：`repo`（全选）、`workflow`
   - 点最底部 `Generate token`
   - **复制那串 `ghp_` 开头的令牌**（只显示一次，务必复制保存）

4. 把令牌发给我，并告诉我你的 **GitHub 用户名** 和 **仓库名**。

## 二、我来做（拿到令牌后自动完成）
- 推送全部代码到你的仓库 main 分支
- 通过 API 启用 GitHub Pages（Source = GitHub Actions）
- 等待几分钟自动部署完成后，给你**永久访问网址**：`https://用户名.github.io/football-miniapp/`

## 三、安全提示
- 令牌只用于本次部署，**部署完成后你可以把它删除/撤销**，不影响网站。
- 该令牌有 `repo` 权限，请勿转发给他人。
