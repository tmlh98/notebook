### Markdown是什么
* Markdown 是一种轻量级标记语言，能将文本换成有效的XHTML(或者HTML)文档，它的目标是实现易读易写，成为一种适用于网络的书写语言。
* Markdown 语法简洁明了，易于掌握，所以用它来写作是件既效率又舒服的事情。我们所熟知的和一些大型CMS，如Joomla!、Drupal等都能很好的支持Markdown。我是因为写GitHub项目库中的Readme才开始接触Markdown。
* Markdown 不是想要取代 HTML，甚至也没有要和它相近，它的语法种类很少，只对应 HTML 标记的一小部分。
* Markdown 的构想不是要使得 HTML 文档更容易书写。在我看来， HTML 已经很容易写了。
* Markdown 的理念是，能让文档更容易读、写和随意改。
* HTML 是一种发布的格式，Markdown 是一种书写的格式。
* 就这样，Markdown 的格式语法只涵盖纯文本可以涵盖的范围。

### 标题：
最大支持到H6
```markdown
#  H1
##  H2
###  H3
####  H4
#####  H5
######  H6
```
另外，H1和H2还能用以下方式显示：

```markdown
一级标题
===
 
二级标题
---
```

### 文本强调：

```markdown
*斜体* or _强调_
**加粗** or __加粗__
***粗斜体*** or ___粗斜体__
```
但是，如果你的`*`和`_`两边都有空白的话，它们就只会被当成普通的符号：这是一段*文本强调*的说明示例。

如果要在文字前后直接插入普通的星号或底线，你可以用反斜线`\`（转义符）：\*这是一段被星号包围的文字\*

### 列表：

#### 无序列表：
```markdown
* 无序列表
* 子项
* 子项
 
+ 无序列表
+ 子项
+ 子项
 
- 无序列表
- 子项
- 子项
```

#### 有序列表：
```markdown
1. 第一行
2. 第二行
3. 第三行
 
1. 第一行
- 第二行
- 第三行
```

#### 组合：
```markdown
* 产品介绍（子项无项目符号）
    此时子项，要以一个制表符或者4个空格缩进
 
* 产品特点
    1. 特点1
    - 特点2
    - 特点3
* 产品功能
    1. 功能1
    - 功能2
    - 功能3
```

可有时我们会出现这样的情况，首行内容是以日期或数字开头：`2017. 公司年度目标。`

为了避免也被转化成有序列表，我们可以在`.`前加上反斜杠`\`（转义符）：`2017\. 公司年度目标。`

### 链接（title为可选项）：
#### 内嵌方式：
```markdown
[Segma](https://www.segma.tech/ "Segma")
```
#### 引用方式：
```markdown
[链接文字][id]
[id]: https://www.segma.tech/ "标题文字"
```
#### 引用存储文件：
```markdown
[链接文字](../path/file/readme.text "标题文字")
```
#### 还能这样使用：
```markdown
[链接文字][]
[链接文字]: https://www.segma.tech/
```
### 邮件：
```markdown
<example@cisdi.com.cn>
```

### 图片：
#### 内嵌方式：
```markdown
![替代文字](https://www.segma.tech//images/index-logo.png "标题文字")
```
#### 引用方式：
```markdown
![替代文字][logo]
[logo]: https://www.segma.tech/images/index-logo.png "标题文字"
```

### 代码和语法高亮：
标记一小段行内代码，将需要高亮的代码块用\`包裹起来：
```markdown
本文是一篇介绍`Markdown`的语法的文章
```
如果高亮的内容包含\`号，可以这样写：
```markdown
`` `包裹起来` ``
```

语法高亮，在\`\`\`之后添加代码段的语言：
````markdown
```html
    <div>Syntax Highlighting</div>
```

```css
    body{font-size:12px}
```

```javascript
    var s = "JavaScript syntax highlighting";
    alert(s);
```

```php
    <?php
      echo "hello, world!";
    ?>
```

```python
    s = "Python syntax highlighting"
    print s
```
````

### 引用：
代码：
```markdown
> Email-style angle brackets
> are used for blockquotes.
> > And, they can be nested.
> #### Headers in blockquotes
> * You can quote a list.
> * Etc.
```
示例：
> Email-style angle brackets
> are used for blockquotes.
> > And, they can be nested.
> #### Headers in blockquotes
> * You can quote a list.
> * Etc.

#### 另外支持提示等级（通过插件实现）
##### 1.注意
代码：
```markdown
>[!note]
> 注意事项
```
示例：
>[!note]
> 注意事项
##### 2.提示
代码：
```markdown
>[!tip]
> 提示事项
```
示例：
>[!tip]
> 提示事项
##### 3.警告
代码：
```markdown
>[!warning]
> 警告事项
```
示例：
>[!warning]
> 警告事项
##### 4.危险
代码：
```markdown
>[!danger]
> 危险事项
```
示例：
>[!danger]
> 危险事项


### 换行：
在一行的结尾处加上2个或2个以上的空格，也可以使用`</br>`标签  
```markdown
第一行文字，</br>
第二行文字
```

### 水平分割线：
```markdown
***
* * *
- - -
```

### 转义符(反斜杠`\`)：
Markdown 可以利用反斜杠来插入一些在语法中有其它意义的符号，例如：如果你想要用星号加在文字旁边的方式来做出强调效果，你可以在星号的前面加上反斜杠：
```markdown
\*literal asterisks\*
```
Markdown 支持以下这些符号前面加上反斜杠来帮助插入普通的符号：
```markdown
\反斜杠  
`反引号  
*星号  
_下划线  
{}花括号  
[]方括号  
()括弧  
#井字号  
+加号  
-减号  
.英文句 
!感叹号
```

### 补充：
Markdown也支持传统的HTML标签。

比如一个链接，你不太喜欢Markdown的写法，也可以直接写成
```markdown
<a href="https://www.segma.tech/">Segma</a>
```

### 附录
Markdown官网：[http://daringfireball.net/projects/markdown/](http://daringfireball.net/projects/markdown/)  
参考资料：[http://markdown.tw/](http://markdown.tw/)

Markdown在线编辑器：

[W3Cschool Markdown](https://www.w3cschool.cn/tools/index?name=markdown)  
[Dillinger](http://dillinger.io/)  
[Markdown Here](http://markdown-here.com/livedemo.html)