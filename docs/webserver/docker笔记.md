## DockerFile 详解

> Dockerfile由一行行命令语句组成，并且支持用“#”开头作为注释，一般的，Dockerfile分为四部分：基础镜像信息，维护者信息，镜像操作指令和容器启动时执行的指令。

### Dockerfile指令

1. FROM
格式：FROM <image>或 FROM <image>:<tag>
第一条指令必须为FROM指令，并且，如果在同一个Dockerfile中创建多个镜像时，可以使用多个FROM指令（每个镜像一次）

2. MAINTAINET
格式：MAINTAINET <name>
指定维护者的信息

3. RUN
格式：RUN <command> 或 RUN ["", "", ""]
每条指令将在当前镜像基础上执行，并提交为新的镜像。（可以用“\”换行）

4. CMD
格式：CMD ["","",""]
指定启动容器时执行的命令，每个Dockerfile只能有一条CMD指令，如果指定了多条指令，则最后一条执行。（会被启动时指定的命令覆盖）

5. EXPOSE
格式：EXPOSE <port>  [ <port> ...]
告诉Docker服务端暴露端口，在容器启动时需要通过 -p 做端口映射

6. ENV
格式：ENV <key> <value>
指定环境变量，会被RUN指令使用，并在容器运行时保存

7. ADD
格式：ADD  <src>  <dest>
复制指定的到容器的中，可以是Dockerfile所在的目录的一个相对路径；可以是URL，也可以是tar.gz（自动解压）

8. COPY
格式：COPY <src>  <dest>
复制本地主机的（ 为 Dockerfile 所在目录的相对路径）到容器中的（当使用本地目录为源目录时，推荐使用 COPY）

9. ENTRYPOINT
格式：ENTRYPOINT ["","",""]
配置容器启动后执行的命令，并且不可被 docker run 提供的参数覆盖。（每个 Dockerfile 中只能有一个 ENTRYPOINT ，当指定多个时，只有最后一个起效）

10. VOLUME
格式：VOLUME ["/mnt"]
创建一个可以从本地主机或其他容器挂载的挂载点，一般用来存放数据库和需要保持的数据等

11. USER
格式：USER daemon
指定运行容器时的用户名或 UID，后续的 RUN 也会使用指定用户。

12. WORKDIR
格式：WORKDIR /path/to/workdir
为后续的 RUN 、 CMD 、 ENTRYPOINT 指令配置工作目录。（可以使用多个 WORKDIR 指令，后续命令如果参数是相对路径， 则会基于之前命令指定的路径）

13. ONBUILD

格式：ONBUILD [INSTRUCTION]
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
-e MYSQL_ROOT_PASSWORD=root  123456  设置root用户的密码为123456
-e MYSQL_DATABASE=test				 新建数据库为test
-e MYSQL_USER=tmlh                   新建tmlh用户
-e MYSQL_PASSWORD=tmlhtest           新建tmlh用户密码为tmlhtest  


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

