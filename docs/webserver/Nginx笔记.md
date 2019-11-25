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

1. 几个常见配置项：

+ $remote_addr 与 $http_x_forwarded_for 用以记录客户端的ip地址；
+ $remote_user ：用来记录客户端用户名称；
+ $time_local ： 用来记录访问时间与时区；
+ $request ： 用来记录请求的url与http协议；
+ $status ： 用来记录请求状态；成功是200；
+ $body_bytes_s ent ：记录发送给客户端文件主体内容大小；
+ $http_referer ：用来记录从那个页面链接访问过来的；
+ $http_user_agent ：记录客户端浏览器的相关信息；

2.  惊群现象：一个网路连接到来，多个睡眠的进程被同事叫醒，但只有一个进程能获得链接，这样会影响系统性能。

3. 每个指令必须有分号结束。

## Nginx location 正则

> 语法规则： location [ = | ~ | ~ * | ^~ ] /uri/ { … }

```
=	表示精确匹配
^~  表示uri以某个常规字符串开头
~	表示区分大小写的正则匹配
~*	表示不区分大小写的正则匹配
!~  区分大小写不匹配
!~* 不区分大小写不匹配
/ 	通用匹配，任何请求都会匹配到。
```

## Nginx 负载均衡详解

实例

``` 
upstream myserver { 
    server 192.168.10.121:3333;
    server 192.168.10.122:3333;
}
server {
    ....
    location  ~*^.+$ {         
        proxy_pass  http://myserver;  #myserver定义的服务器列表         
    }
}
```

### 热备

主服务器挂了后,使用备份服务器

```
upstream mysvr { 
    server 127.0.0.1:7878; 
    server 192.168.10.121:3333 backup;  #热备     
}
```
### 轮询

!> nginx默认就是轮询 , 其权重都默认为1
```
upstream mysvr { 
    server 127.0.0.1:7878;
    server 192.168.10.121:3333;       
}
```

### 加权轮询

权重高的服务器接受的请求数量要高于权重低的服务器

```
upstream mysvr { 
    server 127.0.0.1:7878 weight=1;
    server 192.168.10.121:3333 weight=2;
}
```
### ip_hash

nginx会让相同的客户端ip请求相同的服务器。

```
upstream mysvr { 
    server 127.0.0.1:7878; 
    server 192.168.10.121:3333;
    ip_hash;
}
```
 
关于nginx负载均衡配置的几个状态参数

+ down: 表示当前的server暂时不参与负载均衡。
+ backup: 预留的备份机器。当其他所有的非backup机器出现故障或者忙的时候，才会请求backup机器，因此这台机器的压力最轻。
+ max_fails: 允许请求失败的次数，默认为1。当超过最大次数时，返回proxy_next_upstream 模块定义的错误。
+ fail_timeout: 在经历了max_fails次失败后，暂停服务的时间。max_fails可以和fail_timeout一起使用。
```
upstream mysvr { 
    server 127.0.0.1:7878 weight=2 max_fails=2 fail_timeout=2;
    server 192.168.10.121:3333 weight=1 max_fails=2 fail_timeout=1;    
}
```