# close-vscode.ps1
# 设置控制台编码为 UTF-8
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
chcp 65001 > $null

Write-Host "================================" -ForegroundColor Green
Write-Host "   VS Code 关闭自动上传工具" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# 进入项目目录
Set-Location "C:\CodeProjects\Money Games"
Write-Host "当前目录: $(Get-Location)" -ForegroundColor Cyan

# 检查是否有更改
$status = git status --porcelain

if ($status) {
    Write-Host "检测到以下更改：" -ForegroundColor Yellow
    git status --short
    
    Write-Host ""
    Write-Host "正在上传到 GitHub..." -ForegroundColor Green
    
    # 添加 main.py
    git add main.py
    
    # 提交更改
    $commitMessage = "关闭VS Code前自动备份 $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git commit -m "$commitMessage"
    
    # 推送到远程
    $pushResult = git push origin main 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "上传成功！" -ForegroundColor Green
        Write-Host "提交信息: $commitMessage" -ForegroundColor Cyan
    } else {
        Write-Host "上传失败！" -ForegroundColor Red
        Write-Host "错误信息: $pushResult" -ForegroundColor Red
        Write-Host ""
        Write-Host "按任意键继续关闭 VS Code..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
} else {
    Write-Host "ℹ没有需要上传的更改" -ForegroundColor Yellow
}

# 等待2秒让用户看到结果
Start-Sleep -Seconds 2

# 关闭 VS Code
Write-Host ""
Write-Host "正在关闭 VS Code..." -ForegroundColor Cyan
$vscodeProcess = Get-Process -Name "Code" -ErrorAction SilentlyContinue

if ($vscodeProcess) {
    $vscodeProcess | Stop-Process -Force
    Write-Host "VS Code 已关闭" -ForegroundColor Green
} else {
    Write-Host "VS Code 未运行" -ForegroundColor Yellow
}

# 自动关闭 PowerShell 窗口
Start-Sleep -Seconds 1
Stop-Process -Id $PID