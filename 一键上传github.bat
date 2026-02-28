@echo off
chcp 65001 >nul
title 一键上传工具 - Money Games (Token模式)
color 0A

echo ============================================
echo   一键上传 Money Games (Token模式)
echo ============================================
echo.
echo 开始时间: %date% %time%
echo.

cd /d "C:\CodeProjects\Money Games"
if %errorlevel% neq 0 (
    echo ❌ 无法进入项目目录！
    pause
    exit
)
echo 📁 当前目录: %cd%
echo.

REM 请在这里填入你的 GitHub Token（去掉@符号）
set TOKEN=你的TOKEN放在这里

REM 临时关闭 SSL 验证
echo 🔓 临时关闭 SSL 验证...
git config --global http.sslVerify false

REM 设置更长的超时时间（5分钟）
echo ⏱️ 设置超时时间为 5分钟...
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 300

REM 添加文件（强制添加所有文件）
echo 📦 强制添加所有文件...

echo 添加 main.py...
git add -f main.py

if exist "__pycache__" (
    echo 添加 __pycache__ 文件夹...
    git add -f __pycache__/
)

if exist "blackjack_pyc.py" (
    echo 添加 blackjack_pyc.py...
    git add -f blackjack_pyc.py
)

if exist "make_bj_pyc.py" (
    echo 添加 make_bj_pyc.py...
    git add -f make_bj_pyc.py
)

if exist "neuron_poker-master" (
    echo 添加 neuron_poker-master 文件夹...
    git add -f neuron_poker-master/
) else (
    echo ⚠️ neuron_poker-master 文件夹不存在，请检查路径
    echo 尝试添加 neuron_poker_master（不带横线）...
    if exist "neuron_poker_master" (
        git add -f neuron_poker_master/
    )
)

REM 添加当前目录下所有更改（包括未跟踪的文件）
echo 添加所有其他更改...
git add -A

REM 提交更改（即使没有更改也强制提交）
echo 📝 强制提交更改...
git commit -m "更新游戏文件 %date% %time%" --allow-empty

if %errorlevel% neq 0 (
    echo ❌ 提交失败！
    goto ERROR
)

REM 推送函数
echo.
echo ☁️ 开始推送（将尝试3次）...
echo.

set RETRY_COUNT=0
:PUSH_LOOP
set /a RETRY_COUNT+=1
echo 尝试第 %RETRY_COUNT% 次推送...

REM 使用 Token 推送（修复了URL格式）
git push https://yangkp1105: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@github.com/yangkp1105/Warehouse.git main

if %errorlevel% equ 0 (
    echo ✅ 第 %RETRY_COUNT% 次推送成功！
    goto CLOSE
) else (
    echo ❌ 第 %RETRY_COUNT% 次推送失败
    if %RETRY_COUNT% lss 3 (
        echo 等待 5 秒后重试...
        timeout /t 5 /nobreak >nul
        goto PUSH_LOOP
    ) else (
        echo.
        echo ⚠️ 3次尝试均失败
        echo.
        echo 可能的原因：
        echo 1. 网络连接不稳定 - 请检查网络
        echo 2. GitHub 被墙 - 需要开代理
        echo 3. Token 无效 - 请重新生成
        echo 4. Token 格式错误 - 确保已正确填写
        echo.
        echo 当前 Token 格式: https://yangkp1105:%TOKEN%@github.com/...
        echo 请确认 Token 是否以 ghp_ 开头
        echo.
        goto ERROR
    )
)

:CLOSE
REM 恢复 Git 设置
echo 🔒 恢复 Git 设置...
git config --global http.sslVerify true
git config --global --unset http.lowSpeedLimit
git config --global --unset http.lowSpeedTime

REM 关闭 VS Code
echo 🔚 正在关闭 VS Code...
taskkill /F /IM Code.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ VS Code 已关闭
) else (
    echo ⚠️ VS Code 未运行
)

echo.
echo ✅ 所有操作完成！
echo 结束时间: %date% %time%
echo.
timeout /t 3 /nobreak >nul
exit

:ERROR
echo.
echo ❌ 发生错误，操作中止
git config --global http.sslVerify true
pause
exit