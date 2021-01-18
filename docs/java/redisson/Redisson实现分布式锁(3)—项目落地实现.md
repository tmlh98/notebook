## 一、项目概述

#### 1、技术架构

项目总体技术选型

```
SpringBoot2.1.5 + Maven3.5.4 + Redisson3.5.4 + lombok(插件)
```

#### 2、加锁方式

该项目支持 `自定义注解加锁` 和 `常规加锁` 两种模式

**自定义注解加锁**

```java
 @DistributedLock(value="goods", leaseTime=5)
  public String lockDecreaseStock(){
    //业务逻辑
  }

```

**常规加锁**

```java
 //1、加锁
 redissonLock.lock("redisson", 10);
 //2、业务逻辑
 //3、解锁
 redissonLock.unlock("redisson");

```

#### 3、Redis部署方式

该项目支持四种Redis部署方式

```
1、单机模式部署
2、集群模式部署
3、主从模式部署
4、哨兵模式部署
```

该项目已经实现支持上面四种模式，你要采用哪种只需要修改配置文件`application.properties`，项目代码不需要做任何修改。

#### 4、项目整体结构

```
redis-distributed-lock-core # 核心实现
|
---src
      |
      ---com.jincou.redisson
                           |# 通过注解方式 实现分布式锁
                           ---annotation
                           |# 配置类实例化RedissonLock
                           ---config
                           |# 放置常量信息
                           ---constant
                           |# 读取application.properties信息后，封装到实体
                           ---entity    
                           |# 支持单机、集群、主从、哨兵 代码实现
                           ---strategy

redis-distributed-lock-web-test # 针对上面实现类的测试类
|
---src
      |
      ---java
            |
            ---com.jincou.controller
                                 |# 测试 基于注解方式实现分布式锁
                                 ---AnnotatinLockController.java
                                 |# 测试 基于常规方式实现分布式锁
                                 ---LockController.java
      ---resources                
           | # 配置端口号 连接redis信息(如果确定部署类型，那么将连接信息放到core项目中)
            ---application.properties

```

## 二、测试

模拟`1秒内100个线程`请求接口，来测试结果是否正确。同时测试3中不同的锁:lock锁、trylock锁、注解锁。

#### 1、lock锁

```java
   /**
     * 模拟这个是商品库存
     */
    public static volatile Integer TOTAL = 10;

    @GetMapping("lock-decrease-stock")
    public String lockDecreaseStock() throws InterruptedException {
        redissonLock.lock("lock", 10);
        if (TOTAL > 0) {
            TOTAL--;
        }
        Thread.sleep(50);
        log.info("======减完库存后,当前库存===" + TOTAL);
        //如果该线程还持有该锁，那么释放该锁。如果该线程不持有该锁，说明该线程的锁已到过期时间，自动释放锁
        if (redissonLock.isHeldByCurrentThread("lock")) {
           redissonLock.unlock("lock");
        }
        return "=================================";
    }

```

压测结果

![img](https://img2018.cnblogs.com/blog/1090617/201906/1090617-20190620160457530-219069000.png)

没问题，不会超卖！

#### 2、tryLock锁

```java
   /**
     * 模拟这个是商品库存
     */
    public static volatile Integer TOTAL = 10;

    @GetMapping("trylock-decrease-stock")
    public String trylockDecreaseStock() throws InterruptedException {
        if (redissonLock.tryLock("trylock", 10, 5)) {
            if (TOTAL > 0) {
                TOTAL--;
            }
            Thread.sleep(50);
            redissonLock.unlock("trylock");
            log.info("====tryLock===减完库存后,当前库存===" + TOTAL);
        } else {
            log.info("[ExecutorRedisson]获取锁失败");
        }
        return "===================================";
    }

```

测试结果

![img](https://img2018.cnblogs.com/blog/1090617/201906/1090617-20190620160509805-373780908.png)

没有问题 ，不会超卖！

#### 3、注解锁

```java
/**
     * 模拟这个是商品库存
     */
    public static volatile Integer TOTAL = 10;

    @GetMapping("annotatin-lock-decrease-stock")
    @DistributedLock(value="goods", leaseTime=5)
    public String lockDecreaseStock() throws InterruptedException {
        if (TOTAL > 0) {
            TOTAL--;
        }
        log.info("===注解模式=== 减完库存后,当前库存===" + TOTAL);
        return "=================================";
    }

```

测试结果

![img](https://img2018.cnblogs.com/blog/1090617/201906/1090617-20190620160520050-657011722.png)

没有问题 ，不会超卖！

通过实验可以看出，通过这三种模式都可以实现分布式锁，然后呢？哪个最优。

## 三、三种锁的锁选择

`观点` 最完美的就是lock锁，因为

```
1、tryLock锁是可能会跳过减库存的操作，因为当过了等待时间还没有获取锁，就会返回false,这显然很致命！

2、注解锁只能用于方法上，颗粒度太大，满足不了方法内加锁。

```

#### 1、lock PK tryLock 性能的比较

模拟`5秒内1000个线程`分别去压测这两个接口，看报告结果！

**1）lock锁**

压测结果 1000个线程平均响应时间为31324。吞吐量 14.7/sec

![img](https://img2018.cnblogs.com/blog/1090617/201906/1090617-20190620160532510-1165289045.png)

#### 2）tryLock锁

压测结果 1000个线程平均响应时间为28628。吞吐量 16.1/sec

![img](https://img2018.cnblogs.com/blog/1090617/201906/1090617-20190620160542186-124172156.png)

这里只是单次测试，有很大的随机性。从当前环境单次测试来看，tryLock稍微高点。

#### 2、常见异常 attempt to unlock lock, not ······

在使用RedissonLock锁时，很容易报这类异常，比如如下操作

```
       //设置锁1秒过去
        redissonLock.lock("redisson", 1);
        /**
         * 业务逻辑需要咨询2秒
         */
        redissonLock.release("redisson");

```

上面在并发情况下就会这样

![img](https://img2018.cnblogs.com/blog/1090617/201906/1090617-20190620160552028-1884674135.png)

造成异常原因：

```
线程1 进来获得锁后，但它的业务逻辑需要执行2秒，在 线程1 执行1秒后，这个锁就自动过期了，那么这个时候 
线程2 进来了获得了锁。在线程1去解锁就会抛上面这个异常（因为解锁和当前锁已经不是同一线程了）
```

所以我们需要注意，设置锁的过期时间不能设置太小，一定要合理，宁愿设置大点。

正对上面的异常，可以通过isHeldByCurrentThread()方法，

```java
  //如果为false就说明该线程的锁已经自动释放，无需解锁
  if (redissonLock.isHeldByCurrentThread("lock")) {
            redissonLock.unlock("lock");
  }
```