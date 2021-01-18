这篇主要讲RedissonLock和RLock。Redisson分布式锁的实现是基于RLock接口，RedissonLock实现RLock接口。

## 一、RLock接口

#### 1、概念

```java
public interface RLock extends Lock, RExpirable, RLockAsync
```

很明显RLock是继承Lock锁，所以他有Lock锁的所有特性，比如lock、unlock、trylock等特性,同时它还有很多新特性：强制锁释放，带有效期的锁,。

#### 2、RLock锁API

这里针对上面做个整理，这里列举几个常用的接口说明

```java
public interface RLock {
    //----------------------Lock接口方法-----------------------

    /**
     * 加锁 锁的有效期默认30秒
     */
    void lock();
    /**
     * tryLock()方法是有返回值的，它表示用来尝试获取锁，如果获取成功，则返回true，如果获取失败（即锁已被其他线程获取），则返回false .
     */
    boolean tryLock();
    /**
     * tryLock(long time, TimeUnit unit)方法和tryLock()方法是类似的，只不过区别在于这个方法在拿不到锁时会等待一定的时间，
     * 在时间期限之内如果还拿不到锁，就返回false。如果如果一开始拿到锁或者在等待期间内拿到了锁，则返回true。
     *
     * @param time 等待时间
     * @param unit 时间单位 小时、分、秒、毫秒等
     */
    boolean tryLock(long time, TimeUnit unit) throws InterruptedException;
    /**
     * 解锁
     */
    void unlock();
    /**
     * 中断锁 表示该锁可以被中断 假如A和B同时调这个方法，A获取锁，B为获取锁，那么B线程可以通过
     * Thread.currentThread().interrupt(); 方法真正中断该线程
     */
    void lockInterruptibly();

    //----------------------RLock接口方法-----------------------
    /**
     * 加锁 上面是默认30秒这里可以手动设置锁的有效时间
     *
     * @param leaseTime 锁有效时间
     * @param unit      时间单位 小时、分、秒、毫秒等
     */
    void lock(long leaseTime, TimeUnit unit);
    /**
     * 这里比上面多一个参数，多添加一个锁的有效时间
     *
     * @param waitTime  等待时间
     * @param leaseTime 锁有效时间
     * @param unit      时间单位 小时、分、秒、毫秒等
     */
    boolean tryLock(long waitTime, long leaseTime, TimeUnit unit) throws InterruptedException;
    /**
     * 检验该锁是否被线程使用，如果被使用返回True
     */
    boolean isLocked();
    /**
     * 检查当前线程是否获得此锁（这个和上面的区别就是该方法可以判断是否当前线程获得此锁，而不是此锁是否被线程占有）
     * 这个比上面那个实用
     */
    boolean isHeldByCurrentThread();
    /**
     * 中断锁 和上面中断锁差不多，只是这里如果获得锁成功,添加锁的有效时间
     * @param leaseTime  锁有效时间
     * @param unit       时间单位 小时、分、秒、毫秒等
     */
    void lockInterruptibly(long leaseTime, TimeUnit unit);  
}

```

RLock相关接口，主要是新添加了 `leaseTime` 属性字段，主要是用来设置锁的过期时间,避免死锁。

## 二、RedissonLock实现类

```java
public class RedissonLock extends RedissonExpirable implements RLock

```

RedissonLock实现了RLock接口，所以实现了接口的具体方法。这里我列举几个方法说明下

#### 1、void lock()方法

```
    @Override
    public void lock() {
        try {
            lockInterruptibly();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

```

发现lock锁里面进去其实用的是`lockInterruptibly`（中断锁，表示可以被中断）,而且捕获异常后用 Thread.currentThread().interrupt()来真正中断当前线程，其实它们是搭配一起使用的。

```java
private static Lock lock = new ReentrantLock(); lock.lock(); //必须等持有锁对象的线程做完事情，其他等待的线程才可以做事情。而且中途不能退出。 
lock.lockInterruptibly(); //也必须是等待持有锁对象的线程做完事情，其他线程才能做事情，但中途可以退出
```

具体有关lockInterruptibly()方法讲解推荐一个博客。`博客`：[Lock的lockInterruptibly()](https://blog.csdn.net/zengmingen/article/details/53260650)

接下来执行流程,这里理下关键几步

```java
   /**
     * 1、带上默认值调另一个中断锁方法
     */
    @Override
    public void lockInterruptibly() throws InterruptedException {
        lockInterruptibly(-1, null);
    }
    /**
     * 2、另一个中断锁的方法
     */
    void lockInterruptibly(long leaseTime, TimeUnit unit) throws InterruptedException 
    /**
     * 3、这里已经设置了锁的有效时间默认为30秒  （commandExecutor.getConnectionManager().getCfg().getLockWatchdogTimeout()=30）
     */
    RFuture<Long> ttlRemainingFuture = tryLockInnerAsync(commandExecutor.getConnectionManager().getCfg().getLockWatchdogTimeout(), TimeUnit.MILLISECONDS, threadId, RedisCommands.EVAL_LONG);
    /**
     * 4、最后通过lua脚本访问Redis,保证操作的原子性
     */
    <T> RFuture<T> tryLockInnerAsync(long leaseTime, TimeUnit unit, long threadId, RedisStrictCommand<T> command) {
        internalLockLeaseTime = unit.toMillis(leaseTime);

        return commandExecutor.evalWriteAsync(getName(), LongCodec.INSTANCE, command,
                "if (redis.call('exists', KEYS[1]) == 0) then " +
                        "redis.call('hset', KEYS[1], ARGV[2], 1); " +
                        "redis.call('pexpire', KEYS[1], ARGV[1]); " +
                        "return nil; " +
                        "end; " +
                        "if (redis.call('hexists', KEYS[1], ARGV[2]) == 1) then " +
                        "redis.call('hincrby', KEYS[1], ARGV[2], 1); " +
                        "redis.call('pexpire', KEYS[1], ARGV[1]); " +
                        "return nil; " +
                        "end; " +
                        "return redis.call('pttl', KEYS[1]);",
                Collections.<Object>singletonList(getName()), internalLockLeaseTime, getLockName(threadId));
    }

```

那么void lock(long leaseTime, TimeUnit unit)方法其实和上面很相似了，就是从上面第二步开始的。

#### 2、tryLock(long waitTime, long leaseTime, TimeUnit unit)

接口的参数和含义上面已经说过了，现在我们开看下源码，这里只显示一些重要逻辑。

```java
 	@Override
    public boolean tryLock(long waitTime, long leaseTime, TimeUnit unit) throws InterruptedException {
        long time = unit.toMillis(waitTime);
        long current = System.currentTimeMillis();
        long threadId = Thread.currentThread().getId();
        Long ttl = tryAcquire(leaseTime, unit, threadId);
        //1、 获取锁同时获取成功的情况下，和lock(...)方法是一样的 直接返回True，获取锁False再往下走
        if (ttl == null) {
            return true;
        }
        //2、如果超过了尝试获取锁的等待时间,当然返回false 了。
        time -= System.currentTimeMillis() - current;
        if (time <= 0) {
            acquireFailed(threadId);
            return false;
        }

        // 3、订阅监听redis消息，并且创建RedissonLockEntry，其中RedissonLockEntry中比较关键的是一个 Semaphore属性对象,用来控制本地的锁请求的信号量同步，返回的是netty框架的Future实现。
        final RFuture<RedissonLockEntry> subscribeFuture = subscribe(threadId);
        //  阻塞等待subscribe的future的结果对象，如果subscribe方法调用超过了time，说明已经超过了客户端设置的最大wait time，则直接返回false，取消订阅，不再继续申请锁了。
        //  只有await返回true，才进入循环尝试获取锁
        if (!await(subscribeFuture, time, TimeUnit.MILLISECONDS)) {
            if (!subscribeFuture.cancel(false)) {
                subscribeFuture.addListener(new FutureListener<RedissonLockEntry>() {
                    @Override
                    public void operationComplete(Future<RedissonLockEntry> future) throws Exception {
                        if (subscribeFuture.isSuccess()) {
                            unsubscribe(subscribeFuture, threadId);
                        }
                    }
                });
            }
            acquireFailed(threadId);
            return false;
        }

       //4、如果没有超过尝试获取锁的等待时间，那么通过While一直获取锁。最终只会有两种结果
        //1)、在等待时间内获取锁成功 返回true。2）等待时间结束了还没有获取到锁那么返回false。
        while (true) {
            long currentTime = System.currentTimeMillis();
            ttl = tryAcquire(leaseTime, unit, threadId);
            // 获取锁成功
            if (ttl == null) {
                return true;
            }
           //   获取锁失败
            time -= System.currentTimeMillis() - currentTime;
            if (time <= 0) {
                acquireFailed(threadId);
                return false;
            }
        }
    }

```

`重点` tryLock一般用于特定满足需求的场合，但不建议作为一般需求的分布式锁，一般分布式锁建议用void lock(long leaseTime, TimeUnit unit)。因为从性能上考虑，在高并发情况下后者效率是前者的好几倍

#### 3、unlock()

解锁的逻辑很简单。

```java
@Override
    public void unlock() {
        // 1.通过 Lua 脚本执行 Redis 命令释放锁
        Boolean opStatus = commandExecutor.evalWrite(getName(), LongCodec.INSTANCE,
                RedisCommands.EVAL_BOOLEAN,
                "if (redis.call('exists', KEYS[1]) == 0) then " +
                        "redis.call('publish', KEYS[2], ARGV[1]); " +
                        "return 1; " +
                        "end;" +
                        "if (redis.call('hexists', KEYS[1], ARGV[3]) == 0) then " +
                        "return nil;" +
                        "end; " +
                        "local counter = redis.call('hincrby', KEYS[1], ARGV[3], -1); " +
                        "if (counter > 0) then " +
                        "redis.call('pexpire', KEYS[1], ARGV[2]); " +
                        "return 0; " +
                        "else " +
                        "redis.call('del', KEYS[1]); " +
                        "redis.call('publish', KEYS[2], ARGV[1]); " +
                        "return 1; "+
                        "end; " +
                        "return nil;",
                Arrays.<Object>asList(getName(), getChannelName()),
                LockPubSub.unlockMessage, internalLockLeaseTime,
                getLockName(Thread.currentThread().getId()));
        // 2.非锁的持有者释放锁时抛出异常
        if (opStatus == null) {
            throw new IllegalMonitorStateException(
                    "attempt to unlock lock, not locked by current thread by node id: "
                            + id + " thread-id: " + Thread.currentThread().getId());
        }
        // 3.释放锁后取消刷新锁失效时间的调度任务
        if (opStatus) {
            cancelExpirationRenewal();
        }
    }

```

使用 EVAL 命令执行 Lua 脚本来释放锁：

1. key 不存在，说明锁已释放，直接执行 `publish` 命令发布释放锁消息并返回 `1`。
2. key 存在，但是 field 在 Hash 中不存在，说明自己不是锁持有者，无权释放锁，返回 `nil`。
3. 因为锁可重入，所以释放锁时不能把所有已获取的锁全都释放掉，一次只能释放一把锁，因此执行 `hincrby` 对锁的值**减一**。
4. 释放一把锁后，如果还有剩余的锁，则刷新锁的失效时间并返回 `0`；如果刚才释放的已经是最后一把锁，则执行 `del` 命令删除锁的 key，并发布锁释放消息，返回 `1`。

`注意`这里有个实际开发过程中，容易出现很容易出现上面第二步异常，非锁的持有者释放锁时抛出异常。比如下面这种情况

```java
      //设置锁1秒过去
        redissonLock.lock("redisson", 1);
        /**
         * 业务逻辑需要咨询2秒
         */
        redissonLock.release("redisson");
      /**
       * 线程1 进来获得锁后，线程一切正常并没有宕机，但它的业务逻辑需要执行2秒，这就会有个问题，在 线程1 执行1秒后，这个锁就自动过期了，
       * 那么这个时候 线程2 进来了。在线程1去解锁就会抛上面这个异常（因为解锁和当前锁已经不是同一线程了）
       */
```

