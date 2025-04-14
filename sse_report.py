import os
import sys

from core import constant
from core.context.context import Context
from core.errors.error import ErrorCode, Error
from core.utils import file_utils, alert
from core.utils.log import logger
from doc_engine.doc_engine import DocEngin

if __name__ == '__main__':
    logger.init()
    err = Error(ErrorCode.SUCCESS)
    try:
        # reportJobId = sys.argv[1]
        # env = sys.argv[2]
        # output = sys.argv[3]
        reportJobId = "21990"
        env = "beta"
        output = "/output/"
        current_directory = os.getcwd()
        wokDir = current_directory + constant.PATH_WORK_DIR
        resourceDir = current_directory + constant.PATH_RESOURCE_DIR
        pluginDir = current_directory + constant.PATH_PLUGIN
        outputDir = current_directory + output
        err = file_utils.mkdir(wokDir)
        err = file_utils.mkdir(resourceDir)
        err = file_utils.mkdir(outputDir)
        ctx = Context(reportJobId, env, resourceDir, wokDir, pluginDir)
        # init alert client
        config_path = env + constant.CONFIG_SUFFIX
        alert_client = alert.AlertClient(config_path)
        err = ctx.onCreate()
        reportname = ""

        if err.code == ErrorCode.SUCCESS:
            engin: DocEngin = DocEngin()
            err = engin.createReport(ctx.templatePath, ctx.reportName, outputDir)
            if err.code == ErrorCode.SUCCESS:
                engin.processTemplate(ctx)
                engin.parser(ctx)
                engin.saveReport()
            else:
                reportname = engin.reportPath
                alert_client.send_alert_msg(reportname, ctx.reportJobName, ctx.reportJobCreator, reportJobId, err.msg)
                logger.error(err.msg)
        else:
            alert_client.send_alert_msg(reportname, ctx.reportJobName, ctx.reportJobCreator, reportJobId, err.msg)
            logger.error(err.msg)
        if err.code != ErrorCode.SUCCESS:
            sys.exit(err.code)
    except BaseException as e:
        logger.error(f"{e}")
        sys.exit(ErrorCode.INTERNAL_ERROR)
