#!/usr/bin/env python3
"""
Device Faker Config 镜像仓库推送脚本
"""

import subprocess
import sys


def run_command(cmd):
    """执行 git 命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def main():
    """主函数"""
    print("🔄 Device Faker Config - 推送到镜像仓库")
    print("=" * 60)
    
    # 检查是否在 git 仓库中
    success, _ = run_command("git rev-parse --git-dir")
    if not success:
        print("❌ 错误: 当前目录不是 git 仓库")
        return 1
    
    # 检查 mirror 远程仓库
    success, output = run_command("git remote -v")
    if not success or "mirror" not in output:
        print("❌ 错误: 未配置 mirror 远程仓库")
        print("\n请先配置镜像仓库:")
        print("git remote add mirror https://gitee.com/Seyud/device_faker_config_mirror.git")
        return 1
    
    # 显示当前分支
    success, branch = run_command("git branch --show-current")
    if success:
        branch = branch.strip()
        print(f"📍 当前分支: {branch}")
    
    # 检查是否有未提交的更改
    success, status = run_command("git status --porcelain")
    if success and status.strip():
        print("\n⚠️  警告: 检测到未提交的更改")
        print(status)
        response = input("\n是否继续推送? (y/N): ")
        if response.lower() != 'y':
            print("❌ 已取消推送")
            return 0
    
    # 推送所有分支
    print("\n🚀 推送所有分支到镜像仓库...")
    success, output = run_command("git push mirror --all")
    if not success:
        print(f"❌ 推送分支失败:")
        print(output)
        return 1
    
    if output.strip():
        print(output)
    print("✅ 分支推送成功")
    
    # 推送所有标签
    print("\n🏷️  推送所有标签到镜像仓库...")
    success, output = run_command("git push mirror --tags")
    if not success:
        print(f"❌ 推送标签失败:")
        print(output)
        return 1
    
    if output.strip():
        print(output)
    print("✅ 标签推送成功")
    
    # 显示最新提交
    print("\n📝 最新提交:")
    success, log = run_command("git log --oneline -3")
    if success:
        print(log)
    
    print("=" * 60)
    print("✅ 推送完成！")
    print("🔗 镜像仓库: https://gitee.com/Seyud/device_faker_config_mirror")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
