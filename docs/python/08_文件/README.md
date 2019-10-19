 

## 文件（File）


### 打开和关闭

> open(file, mode='r', buffering=-1, encoding_=None, errors=None, newline=None, closefd=True, opener=None)

 + 参数：
   - file: 要打开的文件的名字（路径）
   - encoding: 指定打开是的编码,一般指定utf-8
   - buffering: 指定要读取的字符的数量,默认值为-1，它会读取文件中的所有字符
   - mode: 指定读写
    - r 表示只读的
    - w 表示是可写的，使用w来写入文件时，如果文件不存在会创建文件，如果文件存在则会截断文件，即删除文件中的内容
    - a 表示追加内容，如果文件不存在会创建文件，如果文件存在则会向文件中追加内容
    - x 用来新建文件，如果文件不存在则创建，存在则报错
    - 为操作符增加功能
        - r+ 即可读又可写，文件不存在会报错
        - w+ 写的基础上读的功能
        - a+ 追加的基础上增加读的功能
    - 读取模式:
        - rt:读取文本文件
        - rb:读取二进制文件 
 + 返回值：
   - 返回一个对象，这个对象就代表了当前打开的文件

```python
file_name = 'demo.txt'
file_obj = open(file_name)
content = file_obj.read()
print(content)
# 调用close()方法来关闭文件
file_obj.close()
```

    `with ... as` 语句


```python
file_name = 'hello'
# 在with语句中可以直接使用file_obj来做文件操作
# 此时这个文件只能在with中使用，一旦with结束则文件会自动close()
try:
    with open(file_name) as file_obj :
        print(file_obj.read())
except FileNotFoundError:
    print(f'{file_name} 文件不存在~~')


```


### 文件读取

+ read() : 读取所有
+ readline(): 读取一行
+ readlines()： 用于一行一行的读取内容，它会一次性将读取到的内容封装到一个列表中返回




### 文件写入

write()


### os


+ os.listdir() 获取指定目录的目录结构
+ os.getcwd() 获取当前所在的目录
+ os.chdir() 切换当前所在的目录 作用相当于 cd
+ os.mkdir("xxx") 在当前目录下创建一个名字为 xxx 的目录
+ os.rmdir('abc') 删除目录
+ os.remove('aa.txt') 删除文件
+ os.rename('旧名字','新名字') 可以对一个文件进行重命名，也可以用来移动一个文件