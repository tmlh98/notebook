 
## 类和对象？

>对象是内存中专门用来存储数据的一块区域。
> 对象由三部分组成：
 1. 对象的标识（id）
 2. 对象的类型（type）
 3. 对象的值（value）

创建一个对象
```python
class 类名([父类]):
#    代码块
```
> isinstance()可以用来检查一个对象是否是一个类的实例


### self用来表示当前对象
```python
class Person :
    
    name = 'swk' # 公共属性，所有实例都可以访问
    
    def say_hello(self) :
        # 方法每次被调用时，解析器都会自动传递第一个实参
        # 第一个参数，就是调用方法的对象本身，
        # 一般我们都会将这个参数命名为self

        # say_hello()这个方法，可以显示如下格式的数据：
        #   你好！我是 xxx
        #   在方法中不能直接访问类中的属性
        print('你好！我是 %s' %self.name) # 必须通过self调用name

```

### 魔术方法

 在类中可以定义一些特殊方法, 即以`__`开头，`__`结尾的方法
 特殊方法不需要我们自己调用，特殊方法将会在特殊的时刻自动调用

#### `__init()__`

```python
class Person :
 
    # 创建对象的流程
    # p1 = Person()的运行流程
    #   1.创建一个变量
    #   2.在内存中创建一个新对象
    #   3.__init__(self)方法执行
    #   4.将对象的id赋值给变量
    name 
    # init会在对象创建以后开始执行
    # init可以用来向新创建的对象中初始化属性
    # 调用类创建对象时，类后边的所有参数都会依次传递到init()中
    #类似Java中的构造方法
    def __init__(self,name):
        print(self)
        # 通过self向新建的对象中初始化属性
        self.name = name

    def say_hello(self):
        print('大家好，我是%s'%self.name)

p =Person('天莫')
p.say_hello()#大家好，我是天莫
```
#### `__str__()`
 
 这个特殊方法会在尝试将对象转换为字符串的时候调用,类似java的`toString()`方法
 它的作用可以用来指定对象转换为字符串的结果  （print函数）.

#### `__repr__()`
     这个特殊方法会在对当前对象使用repr()函数时调用
    它的作用是指定对象在 ‘交互模式’中直接输出的效果   

#### other

```
# object.__add__(self, other)
# object.__sub__(self, other)
# object.__mul__(self, other)
# object.__matmul__(self, other)
# object.__truediv__(self, other)
# object.__floordiv__(self, other)
# object.__mod__(self, other)
# object.__divmod__(self, other)
# object.__pow__(self, other[, modulo])
# object.__lshift__(self, other)
# object.__rshift__(self, other)
# object.__and__(self, other)
# object.__xor__(self, other)
# object.__or__(self, other)

# object.__lt__(self, other) 小于 <
# object.__le__(self, other) 小于等于 <=
# object.__eq__(self, other) 等于 ==
# object.__ne__(self, other) 不等于 !=
# object.__gt__(self, other) 大于 >
# object.__ge__(self, other) 大于等于 >= 

# __len__()获取对象的长度

# object.__bool__(self)
# 可以通过bool来指定对象转换为布尔值的情况

```



### 封装

1. 如何隐藏一个对象中的属性？
   - 将对象的属性名，修改为一个外部不知道的名字
2. 如何获取（修改）对象中的属性？
   - 提供一个getter和setter方法使外部可以访问到属性
   - getter 获取对象中的指定属性（get_属性名）
   - setter 用来设置对象的指定属性（set_属性名）


```python
class Person:
    '''
        表示狗的类
    '''
    def __init__(self , name):
        self.hidden_name = name 

    def get_name(self):
        '''
            get_name()用来获取对象的name属性
        '''    
        return self.hidden_name

    def set_name(self , name):
        '''
            set_name()用来修改属性
        '''
        self.hidden_name = name


```

#### 使用双下划线开头定义属性
 
 双下划线开头的属性，是对象的隐藏属性，隐藏属性只能在类的内部访问，无法通过对象访问
 

```python
# 其实隐藏属性只不过是Python自动为属性改了一个名字
#  实际上是将名字修改为了，_类名__属性名 比如 __name -> _Person__name
class Person:
    def __init__(self,name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_name(self , name):
        self.__name = name        

p = Person('孙悟空')

# print(p.p.__name ) #__开头的属性是隐藏属性，无法通过对象访问
print(p._Person__name) #孙悟空
p._Person__name = '猪八戒'
print(p._Person__name) #猪八戒

```
   使用 `__ `开头的属性，实际上依然可以在外部访问，所以这种方式我们一般不用.
   一般我们会将一些私有属性（不希望被外部访问的属性）以"`_`"开头.
一般情况下，使用 "`_`"开头的属性都是私有属性，没有特殊需要不要修改私有属性.


#### 装饰器

```python
class Person:
    def __init__(self,name,age):
        self._name = name
        self._age = age

    # property装饰器，用来将一个get方法，转换为对象的属性
    # 添加为property装饰器以后，我们就可以像调用属性一样使用get方法
    # 使用property装饰的方法，必须和属性名是一样的
    @property    
    def name(self):
        print('get方法执行了~~~')
        return self._name

    # setter方法的装饰器：@属性名.setter
    @name.setter    
    def name(self , name):
        print('setter方法调用了')
        self._name = name        
        
p = Person('猪八戒',18)
p.name = '孙悟空'
print(p.name)

```






### 继承

   object是所有类的父类，所有类都继承自object
```python
class Person(object):
    pass
```
 issubclass() 检查一个类是否是另一个类的子类
```python
print(issubclass(Person , object)) #True
```
 isinstance()用来检查一个对象是否是一个类的实例
   - 如果这个类是这个对象的父类，也会返回True
   - 所有的对象都是object的实例
```python
print(isinstance(print , object))
```

#### super()
    super() 可以用来获取当前类的父类，并且通过super()返回对象调用父类方法时，不需要传递self

```python
# 父类中的所有方法都会被子类继承，包括特殊方法，也可以重写特殊方法
class Animal:
    def __init__(self,name):
        self._name = name
    @property
    def name(self):
        return self._name

    @name.setter    
    def name(self,name):
        self._name = name
class Dog(Animal):
    def __init__(self,name):
        # 希望可以直接调用父类的__init__来初始化父类中定义的属性
        # super() 可以用来获取当前类的父类，
        #   并且通过super()返回对象调用父类方法时，不需要传递self
        super().__init__(name)      

```




#### 重写

 如果在子类中如果有和父类同名的方法，则通过子类实例去调用方法时，
 会调用子类的方法而不是父类的方法，这个特点我们成为叫做方法的重写（覆盖，override）


#### 多重继承


 - 在开发中没有特殊的情况，应该尽量避免使用多重继承，因为多重继承会让我们的代码过于复杂
 - 如果多个父类中有同名的方法，则会现在第一个父类中寻找，然后找第二个，然后找第三个。。。
 - 前边父类的方法会覆盖后边父类的方法
```python
class C(A,B):
    pass
```




### 类的属性和方法

#### 类属性 
 
>  直接在类中定义的属性是类属性

```python
class Obj:
    # 类属性可以通过类或类的实例访问到
    # 但是类属性只能通过类对象来修改，无法通过实例对象修改
    count = 0
```

#### 实例属性

> 通过实例对象添加的属性属于实例属性

```python
class Obj:
    def __init__(self):
        # 实例属性只能通过实例对象来访问和修改，类对象无法访问修改
        self.name = 'xiaoming'

```
#### 实例方法

>  以self为第一个参数的方法都是实例方法
   

```python
class Obj:
    #   实例方法可以通过实例和类去调用
    #       当通过实例调用时，会自动将当前调用对象作为self传入
    #       当通过类调用时，不会自动传递self，此时我们必须手动传递self
    def test(self):
        print('这是test方法~~~ ' , self)    
```


#### 类方法

> 在类内部使用 `@classmethod` 来修饰的方法属于类方法
> 方法的第一个参数是cls，也会被自动传递，cls就是当前的类对象 

```python
class Obj:

    @classmethod
    def test(cls):
        pass
```
#### 静态方法  

> 在类中使用 `@staticmethod` 来修饰的方法属于静态方法  
  
 +  静态方法不需要指定任何的默认参数，静态方法可以通过类和实例去调用  
 +  静态方法，基本上是一个和当前类无关的方法，它只是一个保存到当前类中的函数
 +  静态方法一般都是一些工具方法，和当前类无关
```python 
class Obj:

    @staticmethod
    def test():
        pass
```


### 垃圾回收

```python
class A:
    def __init__(self):
        self.name = 'A class'

    # del是一个特殊方法，它会在对象被垃圾回收前调用
    def __del__(self):
        print(self , '被删除了~~~')
```