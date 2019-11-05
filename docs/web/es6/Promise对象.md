
>  	Promise对象: 代表了未来某个将要发生的事件(通常是一个异步操作)
>  	有了promise对象, 可以将异步操作以同步的流程表达出来, 避免了层层嵌套的回调函数(俗称'回调地狱')

 
## Promise的三种状态

+ pending
+ fulfilled
+ rejected

1. promise 对象初始化状态为 pending
2. 当调用resolve(成功)，会由pending => fulfilled
3. 当调用reject(失败)，会由pending => rejected

> 注意promsie状态 只能由 pending => fulfilled/rejected, 一旦修改就不能再变


## 使用Promise基本步骤

### 创建Promise对象
```javascript
//初始化状态为pending
let promise = new Promise((resolve, reject) => {
  //执行异步操作
  if(异步操作成功) {
    resolve(value);//pending => fullfilled
  } else {
    reject(errMsg);//pending => rejected
  }
})
```

### 调用promise的then()
```javascript
promise.then(function(
  result => console.log(result),
  errorMsg => alert(errorMsg)
))
```

## Promise对象方法

(1) then方法注册 当resolve(成功)/reject(失败)的回调函数
```
// onFulfilled 是用来接收promise成功的值
// onRejected 是用来接收promise失败的原因
promise.then(onFulfilled, onRejected);
```

> 注意：then方法是异步执行的

(2) resolve(成功) onFulfilled会被调用

```
const promise = new Promise((resolve, reject) => {
   resolve('fulfilled'); // 状态由 pending => fulfilled
});
promise.then(result => { // onFulfilled
    console.log(result); // 'fulfilled' 
}, reason => { // onRejected 不会被调用
    
})
```

(3) reject(失败) onRejected会被调用

```
const promise = new Promise((resolve, reject) => {
   reject('rejected'); // 状态由 pending => rejected
});
promise.then(result => { // onFulfilled 不会被调用
  
}, reason => { // onRejected 
    console.log(reason); // 'rejected'
})
```
(4) promise.catch
```
在链式写法中可以捕获前面then中发送的异常,
promise.catch(onRejected)
相当于
promise.then(null, onRrejected);

// 注意
// onRejected 不能捕获当前onFulfilled中的异常
promise.then(onFulfilled, onRrejected); 

// 可以写成：
promise.then(onFulfilled)
       .catch(onRrejected); 

```
## promise chain

promise.then方法每次调用 都返回一个新的promise对象 所以可以链式写法

```javascript
function taskA() {
    console.log("Task A");
}
function taskB() {
    console.log("Task B");
}
function onRejected(error) {
    console.log("Catch Error: A or B", error);
}

var promise = Promise.resolve();
promise
    .then(taskA)
    .then(taskB)
    .catch(onRejected) // 捕获前面then方法中的异常
```
## Promise的静态方法

(1) Promise.resolve 返回一个fulfilled状态的promise对象
```javascript
Promise.resolve('hello').then(function(value){
    console.log(value);
});

Promise.resolve('hello');
// 相当于
const promise = new Promise(resolve => {
   resolve('hello');
});
```
(2) Promise.reject 返回一个rejected状态的promise对象
```javascript
Promise.reject(24);
new Promise((resolve, reject) => {
   reject(24);
});
```
(3) Promise.all 接收一个promise对象数组为参数

> 只有全部为resolve才会调用 通常会用来处理 多个并行异步操作

```javascript
const p1 = new Promise((resolve, reject) => {
    resolve(1);
});

const p2 = new Promise((resolve, reject) => {
    resolve(2);
});

const p3 = new Promise((resolve, reject) => {
    resolve(3);
});

Promise.all([p1, p2, p3]).then(data => { 
    console.log(data); // [1, 2, 3] 结果顺序和promise实例数组顺序是一致的
}, err => {
    console.log(err);
});
```
(4) Promise.race 接收一个promise对象数组为参数

> Promise.race 只要有一个promise对象进入 FulFilled 或者 Rejected 状态的话，就会继续进行后面的处理。

```javascript
function timerPromisefy(delay) {
    return new Promise(function (resolve, reject) {
        setTimeout(function () {
            resolve(delay);
        }, delay);
    });
}
var startDate = Date.now();

Promise.race([
    timerPromisefy(10),
    timerPromisefy(20),
    timerPromisefy(30)
]).then(function (values) {
    console.log(values); // 10
});
```