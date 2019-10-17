## 长字符串

单引号和双引号不能跨行使用
```python
s = 'hello，\
world'
```

使用三重引号来表示一个长字符串 ''' """
三重引号可以换行，并且会保留字符串中的格式
```python
#'''不能换行，否则就是多行注释
s = ''' 
hello，
world
'''
```

## 字符串

### 指定占位符

> %s 在字符串中表示任意字符
> %f 浮点数占位符
> %d 整数占位符

```python
b = 'Hello %s'%'孙悟空' #Hello 孙悟空
b = 'hello %s 你好 %s'%('tom','孙悟空')#hello tom 你好 孙悟空
b = 'hello %3.5s'%'abcdefg' # %3.5s字符串的长度限制在3-5之间 hello abcde

b = 'hello %s'%123.456 #123.456在这里表示字符
b = 'hello %.2f'%123.456 #保留小数点后两位
b = 'hello %d'%123.95 #取整数
'''
hello 123.456
hello 123.46
hello 123
'''
# 可以通过在字符串前添加一个f来创建一个格式化字符串
# 在格式化字符串中可以直接嵌入变量
b = 'world'
c = f'hello {b}' # hello world


```

### 复制字符串

	字符串可以使用乘法就行复制操作
```python
a = a * 2 #xyzxyz
a = a * 3 #xyzxyzxyz
print(a)
```

## 输入和输出
```python
name = input('请输入你的名字:')
print('name:' , name)

```

