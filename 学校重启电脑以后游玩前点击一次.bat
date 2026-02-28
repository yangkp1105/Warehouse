@echo off
chcp 65001 >nul
title 德州扑克 AI 安装运行脚本
color 0A

echo ========================================
echo   德州扑克 AI 安装运行脚本
echo ========================================
echo.

:: 设置绝对路径
set BASE_DIR=C:\CodeProjects\Money Games
set GAME_DIR=%BASE_DIR%\neuron_poker-master
set PYTHON_PATH=C:\Python39\python.exe

echo 基础目录：%BASE_DIR%
echo 游戏目录：%GAME_DIR%
echo.

:: 检查 Python 是否安装
echo 正在检查 Python 3.9...
%PYTHON_PATH% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python 3.9！
    echo 请先安装 Python 3.9.13 到 C:\Python39
    echo.
    echo 安装步骤：
    echo 1. 双击运行 python-3.9.13-amd64.exe
    echo 2. 务必勾选 "Add Python to PATH"
    echo 3. 选择 "Install Now"
    pause
    exit /b 1
) else (
    echo [OK] 找到 Python 3.9
)

:: 进入游戏目录
cd /d "%GAME_DIR%"
if %errorlevel% neq 0 (
    echo [错误] 无法进入游戏目录：%GAME_DIR%
    echo 请确认文件夹存在
    pause
    exit /b 1
)
echo [OK] 进入游戏目录：%CD%
echo.

:: 检查 offline_packages 文件夹
if not exist offline_packages (
    echo [错误] 找不到 offline_packages 文件夹！
    echo 请确保 %GAME_DIR%\offline_packages 存在
    pause
    exit /b 1
) else (
    echo [OK] 找到离线包文件夹
)

:: 检查 requirements.txt
if not exist requirements.txt (
    echo [错误] 找不到 requirements.txt！
    pause
    exit /b 1
) else (
    echo [OK] 找到依赖列表
)

:: 安装所有依赖
echo.
echo 正在安装所有依赖包（从本地）...
echo ----------------------------------------
%PYTHON_PATH% -m pip install --no-index --find-links ./offline_packages -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [提示] 批量安装遇到问题，尝试逐个安装关键包...
    
    echo 1. 安装 pyglet...
    %PYTHON_PATH% -m pip install --no-index --find-links ./offline_packages pyglet==1.5.11
    
    echo 2. 安装 gym...
    %PYTHON_PATH% -m pip install --no-index --find-links ./offline_packages gym==0.26.2
    
    echo 3. 安装 numpy...
    %PYTHON_PATH% -m pip install --no-index --find-links ./offline_packages numpy
    
    echo 4. 安装 pandas...
    %PYTHON_PATH% -m pip install --no-index --find-links ./offline_packages pandas
    
    echo 5. 安装 matplotlib...
    %PYTHON_PATH% -m pip install --no-index --find-links ./offline_packages matplotlib
    
    echo 6. 安装 docopt...
    %PYTHON_PATH% -m pip install --no-index --find-links ./offline_packages docopt
    
    echo 7. 安装 cloudpickle...
    %PYTHON_PATH% -m pip install --no-index --find-links ./offline_packages cloudpickle
) else (
    echo [OK] 所有依赖安装成功！
)

:: 验证关键包
echo.
echo 验证安装结果：
%PYTHON_PATH% -c "import gym; print('gym 版本:', gym.__version__)" 2>nul && echo [OK] gym 安装成功 || echo [警告] gym 导入失败
%PYTHON_PATH% -c "import pyglet; print('pyglet 版本:', pyglet.version)" 2>nul && echo [OK] pyglet 安装成功 || echo [警告] pyglet 导入失败

echo.
echo ----------------------------------------
echo 安装完成！正在启动游戏...
echo.

:: 运行游戏（1v1 人机对战）
echo 启动图形界面模式...
%PYTHON_PATH% main.py selfplay keypress --render

:: 如果出错，尝试无渲染模式
if %errorlevel% neq 0 (
    echo.
    echo [提示] 图形界面启动失败，尝试文字模式...
    %PYTHON_PATH% main.py selfplay keypress
)

echo.
echo 游戏已退出。
pause