##  cronatb安装

分别安装`vixie-cron`和`crontabs`
```shell
yum -y install vixie-cron
```
```shell
yum -y install crontabs

```

>  `vixie-cron` 是 cron 的主程序；
>  `crontabs` 是用来安装、卸装、或列举用来驱动 cron 守护进程的表格的程序。

## 启动和配置服务

```shell
service crond start     #启动服务
service crond stop      #关闭服务
service crond restart   #重启服务
service crond reload    #重新载入配置
service crond status    #查看crontab服务状态
#设置开机自启动
chkconfig --level 345 crond on
```

## crontab的语法

```
crontab [-u username] [-l|-e|-r]
选项与参数：
-u  ：只有 root 才能进行这个任务，亦即帮其他使用者创建/移除 crontab 工作排程；
-e  ：编辑 crontab 的工作内容
-l  ：查阅 crontab 的工作内容
-r  ：移除所有的 crontab 的工作内容，若仅要移除一项，请用 -e 去编辑
```

### crontab文件格式：
用户所建立的crontab文件中，每一行都代表一项任务，每行的每个字段代表一项设置，它的格式共分为六个字段，前五段是时间设定段，第六段是要执行的命令段，格式如下：

```
minute   hour   day   month   week   command
```

特殊字符:
+ 星号（*）：代表’‘每’'的意思，例如month字段如果是星号，则表示每月都执行该命令。
+ 逗号（,）：表示分隔时段的意思，例如，“1,3,5,7,9”。
+ 中杠（-）：表示一个时间范围，例如“2-6”表示“2,3,4,5,6”。
+ 正斜线（/）：可以用正斜线指定时间的间隔频率，例如“0-23/2”表示每两小时执行一次。同时正斜线可以和星号一起使用，例如*/10，如果用在minute字段，表示每十分钟执行一次。

## 实例

| 描述                      | 语句                                       |
| ----------------------- | ---------------------------------------- |
| 每1分钟执行一次                | */1 * * * * command/1                    |
| 每小时的第15,30,45分钟执行       | 15,30,45 * * * * command                 |
| 7点到10点的第10,50分钟执行       | 10,20 7-50 * * * command                 |
| 每隔一天的7点到11点的第20和第40分钟执行 | 20,40 7-11 */1 * * command               |
| 每周一的7点到11点的第25和第50分钟执行  | 25,50 7-11 * * 1 command                 |
| 每天的3:30执行               | 30 3 * * * command                       |
| 每月1、10、20日的3 : 30执行     | 30 3 1,10,20 * * command                 |
| 每周六、周日的3 : 30执行         | 30 3 * * 6,0 command30 3 * * 6,7 command |
| 每天9点到16点之间每隔15分钟执行      | /15 9-16 * * * command                   |







