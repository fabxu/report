from core import constant
from core.context.context import Context
from core.errors.error import Error, ErrorCode
from core.plugin.base_plugin import BasePlugin
from core.resource.assemble_resource import AssembleResource
from core.resource.resource import BaseResource
from core.resource.image_resource import ImageResource
from core.resource.text_resource import TextResource
from plugins.t68_line_plugin.generate_result import GenerateResult


class T68LinePlugin(BasePlugin):
    def __init__(self, workPath: str, prop: dict):
        super().__init__(workPath, prop)
        self.generate_result = GenerateResult(self._workdir)

    def onCreate(self, ctx: Context) -> Error:
        return Error(ErrorCode.SUCCESS)

    def onProcess(self, ctx: Context, params: str = None) -> (Error, BaseResource):
        # 获取环境变量
        # 评测任务评测结果目录
        err, jobResultPath = ctx.getEnv(constant.ENV_KEY_TASK_JOB, "evalSavePath")
        if err.code != ErrorCode.SUCCESS:
            return err, None
        # 对比任务评测结果目录
        err, compareJobResultPath = ctx.getEnv(constant.ENV_KEY_TASK_COMPARE, "evalSavePath")
        if err.code != ErrorCode.SUCCESS:
            return err, None

        res = self.generate_result.process(jobResultPath, compareJobResultPath)

        resource: AssembleResource = AssembleResource()
        jobName = ctx.getEnv(constant.ENV_KEY_TASK_JOB, "name")
        # # 调用其他插件获取结果
        # err, res = ctx.mgr.process("Other_test", ctx)
        resource.putRes("jobName", TextResource(jobName))

        for sheet_name, tmp in res.items():
            for des_name, data_ in tmp.items():
                if "_image" in des_name:
                    resource.putRes(des_name, ImageResource(data_))
                else:
                    resource.putRes(des_name, TextResource(data_))
        return Error(ErrorCode.SUCCESS), resource

    def onDestroy(self) -> Error:
        return Error(ErrorCode.SUCCESS)
