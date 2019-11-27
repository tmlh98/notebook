## DockerFile 详解

> Dockerfile由一行行命令语句组成，并且支持用“#”开头作为注释，一般的，Dockerfile分为四部分：基础镜像信息，维护者信息，镜像操作指令和容器启动时执行的指令。


### docker 命令

+ docker run -d -p 91:80 nginx ：在后台运行nginx，若没有镜像则先下载，并将容器的80端口映射为宿主机的91端口。
	- -d：后台运行 
	- -P：随机端口映射
	- -p：指定端口映射
	- -net：网络模式

+ docker ps：列出运行中的容器
+ docker ps -a ：列出所有的容器
+ docker stop 容器id：停止容器
+ docker kill 容器id：强制停止容器
+ docker start 容器id：启动已停止的容器
+ docker inspect 容器id：查看容器的所有信息
+ docker container logs 容器id：查看容器日志
+ docker top 容器id：查看容器里的进程
+ docker exec -it 容器id /bin/bash：进入容器
+ exit：退出容器
+ docker rm 容器id：删除已停止的容器
+ docker rm -f 容器id：删除正在运行的容器


### Dockerfile指令

1. FROM

```
FROM <image>
or
FROM <image>:<tag>
```

!> 第一条指令必须为FROM指令，并且，如果在同一个Dockerfile中创建多个镜像时，可以使用多个FROM指令（每个镜像一次）

2. MAINTAINET

```
MAINTAINET <name>
```
指定维护者的信息

3. RUN
```
RUN <command> 
or
RUN ["", "", ""]
```
每条指令将在当前镜像基础上执行，并提交为新的镜像。（可以用“\”换行）

!> RUN命令在 image 文件的构建阶段执行，执行结果都会打包进入 image 文件

4. CMD
```
CMD ["","",""]
```

!> 容器时执行的命令，每个Dockerfile只能有一条CMD指令，如果指定了多条指令，则最后一条执行。（会被启动时指定的命令覆盖）

5. EXPOSE
```
EXPOSE <port>  [ <port> ...]
```
告诉Docker服务端暴露端口，在容器启动时需要通过 -p 做端口映射

6. ENV

```
ENV <key> <value>
```
指定环境变量，会被RUN指令使用，并在容器运行时保存

7. ADD
```
ADD  <src>  <dest>
```
复制指定的到容器的中，可以是Dockerfile所在的目录的一个相对路径；可以是URL，也可以是tar.gz（自动解压）

8. COPY
```
COPY <src>  <dest>
```
复制本地主机的（ 为 Dockerfile 所在目录的相对路径）到容器中的（当使用本地目录为源目录时，推荐使用 COPY）

9. ENTRYPOINT
```
ENTRYPOINT ["","",""]
```
配置容器启动后执行的命令，并且不可被 docker run 提供的参数覆盖。（每个 Dockerfile 中只能有一个 ENTRYPOINT ，当指定多个时，只有最后一个起效）

10. VOLUME
```
VOLUME ["/mnt"]
```
创建一个可以从本地主机或其他容器挂载的挂载点，一般用来存放数据库和需要保持的数据等

11. USER
```
USER daemon
```
指定运行容器时的用户名或 UID，后续的 RUN 也会使用指定用户。

12. WORKDIR
```
WORKDIR /path/to/workdir
```
为后续的 RUN 、 CMD 、 ENTRYPOINT 指令配置工作目录。（可以使用多个 WORKDIR 指令，后续命令如果参数是相对路径， 则会基于之前命令指定的路径）

13. ONBUILD
```
ONBUILD [INSTRUCTION]
```
配置当所创建的镜像作为其它新创建镜像的基础镜像时，所执行的操作指令
 



## docker 安装Mysql

```shell
docker run --name mysql57 \
-p 3306:3306 \
-v /home/appdata/mysql:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=root  123456\
-e MYSQL_DATABASE=test \
-e MYSQL_USER=tx \
-e MYSQL_PASSWORD=tx1998 \
-d \
mysql:5.7.18
```
参数说明:

+  MYSQL_ROOT_PASSWORD：必选变量，root 超级用户的密码。
+  MYSQL_DATABASE：可选变量，启动时创建的数据库的名称。
+  MYSQL_USER：可选变量，用户名
+  MYSQL_PASSWORD：可选变量，密码
+  MYSQL_ALLOW_EMPTY_PASSWORD：可选变量，设置 yes 允许 root 用户的空密码为空
+  MYSQL_RANDOM_ROOT_PASSWORD：可选变量，设置 yes 为 root 用户生成随机初始密码并打印到stdout。
+  MYSQL_ONETIME_PASSWORD：可选变量，在首次登录时强制更改密码。(MySQL 5.6+上支持此功能)



### only_full_group_by 问题

如果安装的版本是 5.7版本, 查询数据时出现如下错误
```
this is incompatible with sql_mode=only_full_group_by
```

可以使用使用下列方式解决

1. 查询 sql_mode

```select @@sql_mode```

结果如下

```
ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
```

2. 修改config-file.cnf

删除其中的 ONLY_FULL_GROUP_BY配置，重新设置到 config-file.cnf中

```sql
[mysqld]
# 表名不区分大小写
lower_case_table_names=1 
#server-id=1
datadir=/var/lib/mysql
#socket=/var/lib/mysql/mysqlx.sock
#symbolic-links=0
sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
```

3. 重启容器

```
docker restart mysql 
```



## docker 安装Nginx

1. 创建桥接网络

```shell
docker network create bridge-user
```

2. docker运行是指定桥接网络`bridge-user`

```shell
docker run -p 8080:8080  --name nginx --network=bridge-user \
-v /home/www/docker/nginx/html:/usr/share/nginx/html  \
-v /home/www/docker/nginx/conf/nginx.conf:/etc/nginx/nginx.conf \
-v /home/www/docker/nginx/conf.d:/etc/nginx/conf.d  \
-v /home/www/docker/nginx/logs:/var/log/nginx \
-d nginx
```
## 常见问题

### 时间差8小时

```
docker run -d -p 8080:8080 \
-v /etc/timezone:/etc/timezone \
-v /etc/localtime:/etc/localtime \
springboot:test
```