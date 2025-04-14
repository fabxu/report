# sse-report

## 1、描述

此项目用于根据报告模板生成评测报告，项目采用python开发，由研发和评测同学共同维护。项目采用插件式设计，评测同学可以根据报告需要开发报告内容生成插件和生成内容组件，并注册到核心组件中，核心组件会根据报告模板中定义的特殊变量调用插件生成相应的内容进行替换，最终生成评测报告。

## 2、方案设计

[技术方案](https://ones.ainewera.com/wiki/#/team/Ttz6FJha/space/96KkXmPP/page/TQF2mk1r)

## 3、开发插件

### 3.1、本地开发环境搭建

python：3.7、3.8经测试可用

ads：运行根目录下的setup.sh安装ads工具，用以从oss上下载相关资源

python依赖库：pip install -i http://pkg.sensetime.com/repository/pypi-proxy/simple --trusted-host pkg.sensetime.com --no-cache-dir -r requirements.txt

### 3.2、插件开发调试

1、在./plugins新建自己的插件目录xxx，如./plugins/test

2、在新建的目录下添加自己的插件代码，继承BasePlugin实现以下4个接口

```
    # ctx: Context非常重要，可以从ctx里获取一些插件所需要的全局变量或者调用其他插件
    # 自定义插件构造函数，注意不能更改参数，插件加载通过反射来创建对应插件
    def __init__(self, workPath: str, prop: dict):
        self._workdir = workPath + prop["key"] + "/"
        self.key = prop["key"]
        self.name = prop[constant.KEY_NAME]
        self.des = prop["des"]
        self.version = prop[constant.KEY_VERSION]
        # 项目会在./workspace目录下为每个插件创建一个与key相同的工作目录，用以存放插件中间过程生成的资源，获取插件自己工作目录：self._workdir
        file_utils.mkdir(self._workdir)

    # 插件初始化时调用
    def onCreate(self, ctx: Context) -> Error:
        pass

    # 调用插件此接口生成相关内容
    def onProcess(self, ctx: Context, params: str = None) -> (Error, BaseResource):
        pass

    # 插件销毁时调用，暂时没用
    def onDestroy(self) -> Error:
        pass
```

3、插件中获取环境变量和调用其他插件

```
        jobName = ctx.getEnv(constant.ENV_KEY_TASK_JOB, "name")
        err, res = ctx.mgr.process("Other_test", ctx)
```

4、开发完在./plugins/plugins.json添加插件注册信息，**注意key需唯一，class为自定义插件类全路径名**

```
[
  {
    "name": "Compare_Result",
    "key": "Compare_Result",
    "class": "plugins.t68_line_plugin.t68_line_plugin.T68LinePlugin",
    "des": "评测结果比较",
    "version": "v1.0.0"
  }
]
```

### 3.2、本地调试

完成插件开发和注册工作后可以本地运行项目进行调试

启动命令：./sse_report.py jobid env customEnv output

| 参数名    | 参数功能描述                                                 |
| --------- | ------------------------------------------------------------ |
| jobid     | 评测报告生成工作流任务的id，注意需要先在评测平台创建报告生成工作流任务，用此任务id |
| env       | 项目环境配置，local： 本地开发调试配置local_config.yml，beta：beta环境配置beta_config.yml，release：生产环境配置release_config.yml |
| customEnv | 用户自定义环境变量json字符串，{"keyxxx": "valuexxxx"}，在报告模版，或者插件中可以通过key来获取自定义环境变量的值，此环境变量对应评测平台工作流任务里的环境变量 |
| output    | 报告输出路径                                                 |

完成调试后可以提交代码，如果增加了新的python依赖库请更新./requirements.txt

后续可以增加本地报告模板调试

### 3.2、beta环境验证

在beta环境创建评测报告生成工作流任务进行验证测试

## 4、环境变量及插件算子明细

[环境变量及算子明细](https://ones.ainewera.com/wiki/#/team/Ttz6FJha/space/96KkXmPP/page/JqzHAfg1)

## 5、注意

### 5.1、字号段落等格式设置

修改报告模版中对应变量或者变量所在字段的字号及段落格式，将会直接作用于生成的评测报告文档中；

### 5.2、模版中变量书写注意事项

1、都用英文

2、在一个变量中不要改变字号、字体、颜色等信息

项目中是用python-docx操作docx文档，python-docx中paragraph对应文档中段落，run对应段落中属性相同的一个连续字符串，

![](./res/Screenshot from 2025-01-26 11-21-02.png)

下图中"Werqwer839.34523sdfjk"、"中国"、"你好吗"就分别属于不同**run**，项目中是以**run**为单位读取数据，以便在后续报告中同一个段落设置不同显示属性的变量，但带来的问题就是一个变量中要保持字号、字体、颜色等显示属性相同，否则会被分成多个**run**导致，匹配失败！

此外还发现在ms office中及时是显示属性相同，也有可能被分成多个**run**，先在的解决方法是，编辑好的模版，在ubuntun下用LibreOffice打开，修改一个变量后再保存，会解决此问题。后续会增加模版检查脚本来检查模版是否存在这种问题。
