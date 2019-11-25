nginx 配置文件位置 
`
/usr/local/nginx/conf/nginx.conf 
`
配置文件中的内容 包含三部分内容
+ 全局块：
	配置服务器整体运行的配置指令 比如 worker_processes  1;处理并发数的配置 
+ events 块：
	影响 Nginx 服务器与用户的网络连接 比如 worker_connections  1024; 支持的最大连接数为 1024 
+ http 块： 
	还包含两部分： http 全局块 server 块