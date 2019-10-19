

>    程序运行过程中，一旦出现异常将会导致程序立即终止，异常以后的代码全部都不会执行！    

## 处理异常

```    
    try语句
        try:
            代码块（可能出现错误的语句）
        except 异常类型 as 异常名:
            代码块（出现错误以后的处理方式）
        except 异常类型 as 异常名:
            代码块（出现错误以后的处理方式）
        except 异常类型 as 异常名:
            代码块（出现错误以后的处理方式）
        else：
            代码块（没出错时要执行的语句）    
        finally:
            代码块（该代码块总会执行）    
  
```

>  try是必须的 else语句有没有都行,except和finally至少有一个               
         

## 抛出异常

+ 使用 raise 语句来抛出异常，
+ raise语句后需要跟一个异常类 或 异常的实例

```python
# 可以自定义异常类，只需要创建一个类继承Exception即可
class MyError(Exception):
    pass

def add(a,b):
    # 如果a和b中有负数，就向调用处抛出异常
    if a < 0 or b < 0:
        # raise用于向外部抛出异常，后边可以跟一个异常类，或异常类的实例
        # raise Exception    
        # 抛出异常的目的，告诉调用者这里调用时出现问题，希望你自己处理一下
        # raise Exception('两个参数中不能有负数！')  
        raise MyError('自定义的异常')
        
        # 也可以通过if else来代替异常的处理
        # return None
    r = a + b
    return r

print(add(-123,456))    
```