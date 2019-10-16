## python 工具介绍


## Python和Sublime的整合

   1. 在Sublime中执行Python代码，ctrl + b 自动在Sublime内置的控制台中执行  
        这种执行方式，在某些版本的Sublime中对中文支持不好，并且不能使用input()函数
    
   2. 使用SublimeREPL来运行python代码    
        安装完成，设置快捷键，希望按f5则自动执行当前的Python代码
        { "keys": ["f5"], "caption": "SublimeREPL:Python","command": "run_existing_window_command", "args":{"id": "repl_python_run","file": "config/Python/Main.sublime-menu"}},

### Sublime Text 3中使用input()输入内容的问题

1. 安装插件：ctrl+shift+p.在弹出窗口中输入REPL,找到sublimeREPL:Python ，按回车开始安装
2. 使用插件：

 >  Tools->SublimeREPL->Python ->Python-RUN current file

就会重新打开一个标签页，该标签页就相当于控制台了，可以在里面输入内容，input函数会接收该内容，程序的输出结果也会显示在该标签页中。

3. 配置快捷键

 >   Preferences->Key Buildings

在user窗口中输入以下内容：

```json
[
    { "keys": ["ctrl+b"], "caption": "SublimeREPL:Python", 
                      "command": "run_existing_window_command", "args":
                      {
                           "id": "repl_python_run",
                           "file": "config/Python/Main.sublime-menu"
                      } 
    },
]

```

使用快捷键`ctrl+b`就会启动控制台