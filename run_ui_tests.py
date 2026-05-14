"""前端 E2E 回归测试运行入口。"""
import sys
import subprocess


def main():
    cmd = [
        sys.executable, "-m", "pytest",
        "--html=ui_report.html",
        "--self-contained-html",
        "-v",
        "--timeout=30",
    ]

    # 额外参数透传
    cmd.extend(sys.argv[1:])

    print(f"▶ 执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=__file__.rsplit("\\", 1)[0])
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
