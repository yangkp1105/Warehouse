@echo off
echo 正在诊断网络...

echo 1. 测试 GitHub 连通性...
ping github.com -n 4

echo.
echo 2. 测试 GitHub HTTPS 端口...
curl -I https://github.com --connect-timeout 5

echo.
echo 3. 查看 Git 配置...
git config --global --list | findstr http

echo.
echo 4. 测试 Git 推送（详细模式）...
set GIT_CURL_VERBOSE=1
git push origin main --dry-run

pause