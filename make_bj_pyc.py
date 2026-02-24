# ========== auto_rename.py ==========
import py_compile
import os
import shutil
import glob

def compile_and_rename(source_file, custom_name=None):
    """
    编译 .py 文件并自动重命名生成的 .pyc
    """
    # 如果没有指定自定义名称，使用源文件名但扩展名改为 .pyc
    if custom_name is None:
        custom_name = source_file.replace('.py', '.pyc')
    
        print(f="="*50)
    print(f"📝 编译: {source_file}")
    print("="*50)
    
    # 1. 编译
    py_compile.compile(source_file)
    print("✅ 编译完成")
    
    # 2. 查找生成的 .pyc 文件
    pycache_dir = '__pycache__'
    if not os.path.exists(pycache_dir):
        print("❌ 找不到 __pycache__ 目录")
        return None
    
    # 获取源文件的基本名（不含扩展名）
    base_name = os.path.splitext(source_file)[0]
    
    # 在 __pycache__ 中查找对应的 .pyc
    found_pyc = None
    for file in os.listdir(pycache_dir):
        if file.startswith(base_name) and file.endswith('.pyc'):
            found_pyc = os.path.join(pycache_dir, file)
            break
    
    if not found_pyc:
        print("❌ 找不到生成的 .pyc 文件")
        return None
    
    print(f"📦 找到生成的 .pyc: {found_pyc}")
    
    # 3. 复制到当前目录并重命名
    target_path = os.path.join('.', custom_name)
    shutil.copy2(found_pyc, target_path)
    print(f"📋 已复制并重命名为: {target_path}")
    
    # 4. 可选：删除原来的 .pyc（如果需要）
    # os.remove(found_pyc)
    
    # 5. 显示文件信息
    file_size = os.path.getsize(target_path)
    print(f"📊 文件大小: {file_size} 字节")
    
    return target_path

# 使用示例
compile_and_rename('blackjack_pyc.py', 'blackjack.pyc')