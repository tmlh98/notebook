# 格式化字符串
a = 'hello'

# 字符串之间也可以进行加法运算
# 如果将两个字符串进行相加，则会自动将两个字符串拼接为一个
a = 'abc' + 'haha' + '哈哈'
# a = 123 
# 字符串只能不能和其他的类型进行加法运算，如果做了会出现异常 TypeError: must be str, not int
# print("a = "+a) # 这种写法在Python中不常见
a = 123
# print('a =',a)

# 在创建字符串时，可以在字符串中指定占位符
# %s 在字符串中表示任意字符
# %f 浮点数占位符
# %d 整数占位符
b = 'Hello %s'%'孙悟空'
print(b)
b = 'hello %s 你好 %s'%('tom','孙悟空')
print(b)
b = 'hello %3.5s'%'abcdefg' # %3.5s字符串的长度限制在3-5之间
b = 'hello %s'%123.456
b = 'hello %.2f'%123.456
b = 'hello %d'%123.95
b = '呵呵'

# print('a = %s'%a)

# 格式化字符串，可以通过在字符串前添加一个f来创建一个格式化字符串
# 在格式化字符串中可以直接嵌入变量
c = f'hello {a} {b}'

print(f'a = {a}')

# 练习 创建一个变量保存你的名字，然后通过四种格式化字符串的方式
#   在命令行中显示，欢迎 xxx 光临！

name = '欢迎 %s 光临！'%'tom'
print(name)
tom = 'Tom'
print(f'欢迎 {tom} 光临!')
 