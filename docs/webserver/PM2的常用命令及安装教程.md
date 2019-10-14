PM2 （github上的源码）是开源的基于Nodejs的进程管理器，包括守护进程，监控，日志的一整套完整的功能，基本是Nodejs应用程序不二的守护进程选择，事实上它并不仅仅可以启动Nodejs的程序，只要是一般的脚本的程序它同样可以胜任。

### 主要特性

>内建负载均衡（使用Node cluster 集群模块） 
>后台运行 
>0秒停机重载 
>开机自启动脚本 
>停止不稳定的进程（避免无限循环） 
>控制台检测 
>提供远程控制和实时的接口API (允许和PM2进程管理器交互)

### 安装

	$ npm install -g pm2

查看是否安装成功

	$ pm2 -v

如果提示command not found，尝试建立软链接

### 常用命令

	$ pm2 start app.js              # 启动app.js应用程序
	$ pm2 start app.js -i 4         # cluster mode 模式启动4个app.js的应用实例     # 4个应用程序会自动进行负载均衡
	$ pm2 start app.js --name="api" # 启动应用程序并命名为 "api"
	
	$ pm2 start app.js --watch      # 当文件变化时自动重启应用
	
	$ pm2 start script.sh           # 启动 bash 脚本
	
	$ pm2 list                      # 列表 PM2 启动的所有的应用程序
	
	$ pm2 monit                     # 显示每个应用程序的CPU和内存占用情况
	
	$ pm2 show [app-name]           # 显示应用程序的所有信息


    $ pm2 logs                      # 显示所有应用程序的日志

    $ pm2 logs [app-name]           # 显示指定应用程序的日志

    $ pm2 flush


    $ pm2 stop all                  # 停止所有的应用程序

    $ pm2 stop 0                    # 停止 id为 0的指定应用程序

    $ pm2 restart all               # 重启所有应用

    $ pm2 reload all                # 重启 cluster mode下的所有应用

    $ pm2 gracefulReload all        # Graceful reload all apps in cluster mode

    $ pm2 delete all                # 关闭并删除所有应用

    $ pm2 delete 0                  # 删除指定应用 id 0

    $ pm2 scale api 10              # 把名字叫api的应用扩展到10个实例

    $ pm2 reset [app-name]          # 重置重启数量


    $ pm2 startup                   # 创建开机自启动命令

    $ pm2 save                      # 保存当前应用列表

    $ pm2 resurrect                 # 重新加载保存的应用列表

    $ pm2 update                    # Save processes, kill PM2 and restore processes

    $ pm2 generate                  # Generate a sample json configuration file

    $ pm2 deploy app.json prod setup    # Setup "prod" remote server

    $ pm2 deploy app.json prod          # Update "prod" remote server

    $ pm2 deploy app.json prod revert 2 # Revert "prod" remote server by 2

    $ pm2 module:generate [name]    # Generate sample module with name [name]

    $ pm2 install pm2-logrotate     # Install module (here a log rotation system)

    $ pm2 uninstall pm2-logrotate   # Uninstall module

    $ pm2 publish                   # Increment version, git push and npm publish