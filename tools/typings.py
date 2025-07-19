import sys
import json
import os

def ensure_typings_path(stub):
    # 如果已经是绝对路径或以typings/开头，直接返回，否则加前缀
    if stub.startswith("typings/") or stub.startswith("/") or stub.startswith("."):
        return stub
    return f"typings/{stub}"

# 1. 获取参数
if len(sys.argv) < 2 or sys.argv[1].lower() == "python":
    stubs = []
    board_key = "python"
else:
    board_key = sys.argv[1].lower()
    config_path = os.path.join(os.path.dirname(__file__), '../typings/config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    if board_key not in config['boards']:
        print(f"Board '{board_key}' not found in config.json")
        sys.exit(1)
    raw_stubs = config['boards'][board_key]['stubs']
    stubs = [ensure_typings_path(s) for s in raw_stubs]

vscode_settings_path = os.path.join(os.path.dirname(__file__), '../.vscode/settings.json')
settings = {}
if os.path.exists(vscode_settings_path):
    try:
        with open(vscode_settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except Exception as e:
        print(f"警告: 读取 .vscode/settings.json 失败，已自动重置为默认。错误信息: {e}")

# === 自动补全基础配置（强制写入） ===
settings["python.analysis.typeCheckingMode"] = "basic"
settings["python.analysis.diagnosticSeverityOverrides"] = {
    "reportMissingModuleSource": "none"
}

if stubs:
    settings["python.analysis.stubPath"] = stubs[0] if len(stubs) > 0 else ""
    settings["python.analysis.typeshedPaths"] = stubs
    settings["python.analysis.extraPaths"] = stubs
    print(f"已将 .vscode/settings.json 的 stubPath/typeshedPaths/extraPaths 设置为: {stubs}")
else:
    settings.pop("python.analysis.stubPath", None)
    settings.pop("python.analysis.typeshedPaths", None)
    settings.pop("python.analysis.extraPaths", None)
    print("已恢复为仅使用 python 插件的默认设置。")

with open(vscode_settings_path, 'w', encoding='utf-8') as f:
    json.dump(settings, f, ensure_ascii=False, indent=2)
