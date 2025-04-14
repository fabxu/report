from core import constant
from core.context.context import Context
from core.errors.error import Error, ErrorCode
from core.plugin.base_plugin import BasePlugin
from core.resource.assemble_resource import AssembleResource
from core.resource.resource import BaseResource
from core.resource.text_resource import TextResource


class TestPlugin(BasePlugin):
    def __init__(self, workPath: str, prop: dict):
        super().__init__(workPath, prop)

    def onCreate(self, ctx: Context) -> Error:
        return Error(ErrorCode.SUCCESS)

    def onProcess(self, ctx: Context, params: str = None) -> (Error, BaseResource):
        # 获取环境变量
        # 评测任务评测结果目录
        jobResultPath = ctx.getEnv(constant.ENV_KEY_TASK_JOB, "evalSavePath")
        # 对比任务评测结果目录
        compareJobResultPath = ctx.getEnv(constant.ENV_KEY_TASK_COMPARE, "evalSavePath")
        resource: AssembleResource = AssembleResource()
        jobName = ctx.getEnv(constant.ENV_KEY_TASK_JOB, "name")
        # 调用其他插件获取结果
        err, res = ctx.mgr.process("Other_test", ctx)
        resource.putRes("jobName", TextResource(jobName))
        resource.putRes("Other_test", res.getData())
        return Error(ErrorCode.SUCCESS), resource

    def onDestroy(self) -> Error:
        return Error(ErrorCode.SUCCESS)
