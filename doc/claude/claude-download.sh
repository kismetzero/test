#!/usr/bin/env bash

set -e

echo -e "\n\033[36m ===== [ claude 下载脚本 开始 ] ===== \033[0m"

# DOWNLOAD_DIR="$HOME/.claude/downloads"
DOWNLOAD_DIR="."
DOWNLOAD_BASE_URL="https://downloads.claude.ai/claude-code-releases"

# version=$(curl -fsSL "$DOWNLOAD_BASE_URL/latest")
version="2.1.173"
# version="2.1.170"

manifest_json_path="$DOWNLOAD_DIR/manifest-${version}.json"
echo "[下载] $manifest_json_path"
# curl -fsSL -o "$manifest_json_path" "$DOWNLOAD_BASE_URL/$version/manifest.json"

platforms=(
    "win32-x64"
    # "win32-arm64"
    "linux-x64"
    "linux-arm64"
    # "linux-x64-musl"
    # "linux-arm64-musl"
)

for platform in "${platforms[@]}"; do
    case "$platform" in
        *win*)
            binary_path="$DOWNLOAD_DIR/claude-$version-$platform.exe"
            echo "[下载] $binary_path"
            # curl -fsSL -o "$binary_path" "$DOWNLOAD_BASE_URL/$version/$platform/claude.exe"
            ;;
        *)
            binary_path="$DOWNLOAD_DIR/claude-$version-$platform"
            echo "[下载] $binary_path"
            # curl -fsSL -o "$binary_path" "$DOWNLOAD_BASE_URL/$version/$platform/claude"
            ;;
    esac

    checksum=$(cat "$manifest_json_path" | jq -r ".platforms[\"$platform\"].checksum // empty")
    actual=$(sha256sum "$binary_path" | cut -d' ' -f1)
    if [ "$actual" != "$checksum" ]; then
        echo "[错误] 文件校验失败 $binary_path"
        # rm -f "$binary_path"
        continue
    fi
    echo "[成功] 文件校验成功 $binary_path"
done

echo -e "\033[36m ===== [ claude 下载脚本 结束 ] ===== \033[0m \n"
