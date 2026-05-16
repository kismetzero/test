import re

# 1. 常见 Readline 功能的中文释义字典
FUNC_COMMENTS = {
    "abort": "中止当前操作",
    "accept-line": "接受当前行并执行（相当于回车）",
    "backward-char": "光标向后移动一个字符（左箭头）",
    "backward-delete-char": "删除光标前的一个字符（退格键）",
    "backward-kill-word": "删除光标前的一个单词",
    "backward-word": "光标向后跳一个单词",
    "beginning-of-history": "跳转到历史记录的第一条",
    "beginning-of-line": "跳转到行首（Home键）",
    "call-last-kbd-macro": "执行最后一次定义的键盘宏",
    "capitalize-word": "将当前单词首字母大写",
    "clear-screen": "清屏（相当于 Ctrl+L）",
    "complete": "执行补全（Tab键）",
    "delete-char": "删除光标下的字符（Delete键）",
    "delete-horizontal-space": "删除光标周围的所有空格",
    "digit-argument": "输入数字参数",
    "display-shell-version": "显示 Shell 版本信息",
    "downcase-word": "将当前单词转为小写",
    "dump-functions": "列出所有 Readline 函数及其绑定",
    "dump-macros": "列出所有 Readline 宏及其绑定",
    "dump-variables": "列出所有 Readline 变量及其值",
    "emacs-editing-mode": "切换到 Emacs 编辑模式",
    "end-kbd-macro": "结束定义键盘宏",
    "end-of-history": "跳转到历史记录的最后一条",
    "end-of-line": "跳转到行尾（End键）",
    "exchange-point-and-mark": "交换光标和标记的位置",
    "execute-named-command": "按名称执行命令（Alt+x）",
    "forward-char": "光标向前移动一个字符（右箭头）",
    "forward-search-history": "向前搜索历史记录",
    "forward-word": "光标向前跳一个单词",
    "history-search-backward": "向后搜索以当前输入开头的历史命令",
    "history-search-forward": "向前搜索以当前输入开头的历史命令",
    "insert-comment": "在行首插入或移除注释符号 #",
    "insert-completions": "插入所有可能的补全内容",
    "kill-line": "删除从光标到行尾的内容",
    "kill-whole-line": "删除整行内容",
    "kill-word": "删除光标后的一个单词",
    "newline": "插入换行符",
    "non-incremental-reverse-search-history": "非增量反向搜索历史",
    "overwrite-mode": "切换覆盖/插入模式",
    "paste-from-clipboard": "从剪贴板粘贴",
    "possible-completions": "列出所有可能的补全项",
    "previous-history": "上一条历史记录（上箭头）",
    "quoted-insert": "字面插入下一个字符（Ctrl+V）",
    "re-read-init-file": "重新读取 .inputrc 配置文件",
    "reverse-search-history": "反向搜索历史记录（Ctrl+R）",
    "revert-line": "撤销对本行的所有修改",
    "self-insert": "插入自己（输入普通字符）",
    "set-mark": "设置标记",
    "shell-expand-line": "执行 Shell 扩展（如别名、变量替换）",
    "start-kbd-macro": "开始定义键盘宏",
    "tilde-expand": "执行波浪号 ~ 扩展",
    "transpose-chars": "交换光标前后的两个字符",
    "transpose-words": "交换光标前后的两个单词",
    "undo": "撤销上一步操作",
    "unix-filename-rubout": "删除光标前的一个路径或文件名",
    "unix-line-discard": "删除从行首到光标的内容（Ctrl+U）",
    "unix-word-rubout": "删除光标前的一个单词（Ctrl+W）",
    "upcase-word": "将当前单词转为大写",
    "yank": "粘贴（Yank）最近删除的内容（Ctrl+Y）",
    "yank-last-arg": "粘贴上一条命令的最后一个参数（Alt+.）",
    "yank-nth-arg": "粘贴上一条命令的第 N 个参数",
    "yank-pop": "轮换粘贴之前删除的内容",
}

# 2. 常见转义序列的按键翻译字典
KEY_COMMENTS = {
    r"\e[A": "上箭头", r"\e[B": "下箭头", r"\e[C": "右箭头", r"\e[D": "左箭头",
    r"\e[1~": "Home", r"\e[2~": "Insert", r"\e[3~": "Delete", r"\e[4~": "End",
    r"\e[5~": "Page Up", r"\e[6~": "Page Down", r"\e[7~": "Home", r"\e[8~": "End",
    r"\e[H": "Home", r"\e[F": "End", r"\eOH": "Home", r"\eOF": "End",
    r"\e[Z": "Shift + Tab", r"\e\r": "Ctrl + Enter",
    r"\C-a": "Ctrl+A", r"\C-b": "Ctrl+B", r"\C-d": "Ctrl+D", r"\C-e": "Ctrl+E",
    r"\C-h": "Ctrl+H", r"\C-i": "Tab", r"\C-j": "Ctrl+J", r"\C-k": "Ctrl+K",
    r"\C-l": "Ctrl+L", r"\C-m": "Enter", r"\C-n": "Ctrl+N", r"\C-p": "Ctrl+P",
    r"\C-r": "Ctrl+R", r"\C-s": "Ctrl+S", r"\C-t": "Ctrl+T", r"\C-u": "Ctrl+U",
    r"\C-v": "Ctrl+V", r"\C-w": "Ctrl+W", r"\C-y": "Ctrl+Y",
    r"\e": "Alt / Esc", r"\C-_": "Ctrl+/",
}

def get_key_comment(key_str):
    """根据按键字符串返回对应的按键名称"""
    for seq, name in KEY_COMMENTS.items():
        if seq in key_str:
            return name
    return ""

def annotate_bindv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
        open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            line = line.rstrip()
            # 跳过空行和已有的注释行
            if not line or line.strip().startswith('#') or line.strip().startswith('$'):
                outfile.write(line + '\n')
                continue
            
            # 匹配格式： "按键": 功能
            match = re.match(r'^(\s*".+?"\s*):\s*(\S+)', line)
            if match:
                key_part = match.group(1)
                func_name = match.group(2)
                
                comment_parts = []
                
                # 1. 添加按键的物理名称注释
                key_name = get_key_comment(key_part)
                if key_name:
                    comment_parts.append(key_name)
                
                # 2. 添加功能的中文释义
                func_desc = FUNC_COMMENTS.get(func_name, "")
                if func_desc:
                    comment_parts.append(func_desc)
                
                # 如果有注释内容，就拼接到行尾
                if comment_parts:
                    line += f"    # {' | '.join(comment_parts)}"
            
            outfile.write(line + '\n')

if __name__ == "__main__":
    input_filename = "bindv.txt"  # 你的原始文件
    output_filename = "bindv_annotated.txt" # 生成的带注释文件
    
    try:
        annotate_bindv(input_filename, output_filename)
        print(f"✅ 成功！已生成带注释的文件：{output_filename}")
    except FileNotFoundError:
        print(f"❌ 找不到文件 {input_filename}，请确保它和脚本在同一目录下。")