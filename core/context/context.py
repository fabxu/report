import json
from typing import Any

import requests
import yaml

from core import constant
from core.bean.beans import Job, Workflow
from core.errors.error import Error, ErrorCode
from core.utils import utils
from core.utils.log import logger

CONFIG_SSE_HOST = "sseHost"
CONFIG_SSE_BASE_PATH = "sseBasePath"
CONFIG_AUTH_HEADER = "authHeader"
CONFIG_ADS_PROFILE = "ads"
CONFIG_LOCAL_TEMPLATE = "localTemplate"


class Config:
    def __init__(self, env: dict):
        self.sseHost = utils.getValue(env, CONFIG_SSE_HOST, None)
        self.sseBasePath = utils.getValue(env, CONFIG_SSE_BASE_PATH, None)
        header = utils.getValue(env, CONFIG_AUTH_HEADER, {})
        if len(header) > 0:
            self.authHeader = header
        else:
            self.authHeader = {}
        self.ads = utils.getValue(env, CONFIG_ADS_PROFILE, {})
        self.localTemplate = utils.getValue(env, CONFIG_LOCAL_TEMPLATE, None)


def parserConfig(configPath: str) -> (Error, Config):
    with open(configPath, "r") as file:
        data = yaml.safe_load(file)
        return Error(ErrorCode.SUCCESS), data
    return Error(ErrorCode.PARSER_ERROR, f"parser config failed, config {configPath}"), nil


def requestJob(id: str, getJobUrl: str, header: dict = {}) -> (Error, dict):
    msg = None
    code = ErrorCode.SUCCESS
    url = getJobUrl + id
    result = {}
    rsp = requests.get(url, headers=header)
    if rsp.status_code == constant.HTTP_CODE_SUCCESS:
        resp = rsp.json()
        if resp is None:
            msg = "Request job failed, No body"
            code = ErrorCode.REQUEST_ERROR
            logger.error(msg)
        else:
            if constant.HTTP_KEY_CODE in resp:
                errorCode = resp[constant.HTTP_KEY_CODE]
                if errorCode == "":
                    result = resp[constant.HTTP_KEY_DATA]
                else:
                    msg = f"Request job failed! Code : {errorCode}"
                    code = ErrorCode.REQUEST_ERROR
                    logger.error(msg)
            else:
                msg = "Request job failed!"
                code = ErrorCode.REQUEST_ERROR
                logger.error(msg)
    else:
        msg = f"request job failed, status_code: {rsp.status_code}"
        code = ErrorCode.REQUEST_ERROR
        logger.error(msg)
    return Error(code, msg), result


def requestWorkflow(id: str, getWorkflowUrl: str, header: dict = {}) -> (Error, dict):
    msg = None
    code = ErrorCode.SUCCESS
    url = getWorkflowUrl + id
    result = {}
    rsp = requests.get(url, headers=header)
    if rsp.status_code == constant.HTTP_CODE_SUCCESS:
        resp = rsp.json()
        if resp is None:
            msg = "Request workflow failed, No body"
            code = ErrorCode.REQUEST_ERROR
            logger.error(msg)
        else:
            if constant.HTTP_KEY_CODE in resp:
                errorCode = resp[constant.HTTP_KEY_CODE]
                if errorCode == "":
                    result = resp[constant.HTTP_KEY_DATA]
                else:
                    msg = f"Request workflow failed! Code : {errorCode}"
                    code = ErrorCode.REQUEST_ERROR
                    logger.error(msg)
            else:
                msg = "Request workflow failed!"
                code = ErrorCode.REQUEST_ERROR
                logger.error(msg)
    else:
        msg = f"request workflow failed, status_code: {rsp.status_code}"
        code = ErrorCode.REQUEST_ERROR
        logger.error(msg)
    return Error(code, msg), result


class GlobalData:
    def __init__(self):
        self.reportJob = None
        self.job = None
        self.compareJob = None
        self.reportWorkflow = None
        self.globals: dict = {}

    def buildGlobal(self):
        self.globals[constant.ENV_KEY_TASK_REPORT] = self.reportJob
        self.globals[constant.ENV_KEY_TASK_JOB] = self.job
        self.globals[constant.ENV_KEY_TASK_COMPARE] = self.compareJob
        self.globals[constant.ENV_KEY_TASK_REPORT_WORKFLOW] = self.reportWorkflow


class Context:
    def __init__(self, id: str, envConfig: str, resourcePath: str, workPath: str, pluginPath: str):
        self.reportJobId = id
        self.templatePath = ""
        self.reportName = ""
        self.reportJobCreator = ""
        self.reportJobName = ""
        self._resourcePath = resourcePath
        self._workPath = workPath
        self._configName = envConfig + constant.CONFIG_SUFFIX
        self._globalData = GlobalData()
        self._customEnv: dict = {}
        from .plugin_manager import PluginManager
        self.mgr = PluginManager(pluginPath)

    def getEnv(self, envKey: str, fieldName: str) -> (Error, Any):
        if envKey in self._customEnv:
            return Error(ErrorCode.SUCCESS), self._customEnv[envKey]
        if envKey in self._globalData.globals:
            if hasattr(self._globalData.globals[envKey], fieldName):
                return Error(ErrorCode.SUCCESS), getattr(self._globalData.globals[envKey], fieldName)
            else:
                return Error(ErrorCode.NOT_FOUND_ERROR, f"No the field {fieldName} in env {envKey}"), None
        else:
            return Error(ErrorCode.NOT_FOUND_ERROR, f"No the env {envKey}"), None

    def onCreate(self) -> Error:
        err, data = parserConfig(self._configName)
        if err.code == ErrorCode.SUCCESS:
            self.config = Config(data)
            err = self._requireJobResource()
            if err.code == ErrorCode.SUCCESS:
                self._globalData.buildGlobal()
                if len(self._globalData.reportJob.customConfig) > 0:
                    self._customEnv = json.loads(self._globalData.reportJob.customConfig)
                    logger.info("self._customEnv: " + str(self._customEnv))
                self.mgr.load(self._workPath)
                self.mgr.create(self)
        return err

    def _requireJobResource(self) -> Error:
        getJobUrl = self.config.sseHost + self.config.sseBasePath + constant.PATH_SSE_JOB
        err, reportJob = requestJob(self.reportJobId, getJobUrl, self.config.authHeader)
        if err.code == ErrorCode.SUCCESS:
            self._globalData.reportJob = Job(reportJob)
            self.reportJobCreator = self._globalData.reportJob.createdBy
            self.reportJobName = self._globalData.reportJob.name
            getWorkflowUrl = self.config.sseHost + self.config.sseBasePath + constant.PATH_SSE_WORKFLOW
            err, workflow = requestWorkflow(self._globalData.reportJob.workflowTemplateId, getWorkflowUrl,
                                            self.config.authHeader)
            if err.code == ErrorCode.SUCCESS:
                self._globalData.reportWorkflow = Workflow(workflow)
                if self.config.localTemplate is None:
                    self._globalData.reportWorkflow.savePath = f"{self._resourcePath}{self._globalData.reportWorkflow.templateName}"
                    self.templatePath = self._globalData.reportWorkflow.savePath
                    self.reportName = self._globalData.reportJob.name
                    ads_profile = self.config.ads.get("profile", "")

                    err = utils.downloadFromS3(ads_profile, self._globalData.reportWorkflow.templatePath,
                                               self._globalData.reportWorkflow.savePath)
                else:
                    self._globalData.reportWorkflow.savePath = f"{self._resourcePath}{self.config.localTemplate}"
                    self.templatePath = self._globalData.reportWorkflow.savePath
                if err.code == ErrorCode.SUCCESS:
                    if self._globalData.reportJob.jobId is not None:
                        errJob, job = requestJob(self._globalData.reportJob.jobId, getJobUrl, self.config.authHeader)
                        if errJob.code == ErrorCode.SUCCESS:
                            self._globalData.job = Job(job)
                            self._globalData.job.evalSavePath = f"{self._resourcePath}{self._globalData.job.id}/"
                            err = utils.downloadFromS3(ads_profile, self._globalData.job.evalResultsPath,
                                                       self._globalData.job.evalSavePath)
                            if err.code == ErrorCode.SUCCESS:
                                if self._globalData.reportJob.compareId is not None:
                                    errCompare, compareJob = requestJob(self._globalData.reportJob.compareId,
                                                                        getJobUrl, self.config.authHeader)
                                    if errCompare.code == ErrorCode.SUCCESS:
                                        self._globalData.compareJob = Job(compareJob)
                                        self._globalData.compareJob.evalSavePath = f"{self._resourcePath}{self._globalData.compareJob.id}/"
                                        err = utils.downloadFromS3(ads_profile,
                                                                   self._globalData.compareJob.evalResultsPath,
                                                                   self._globalData.compareJob.evalSavePath)
                                    else:
                                        err = Error(ErrorCode.REQUEST_ERROR, errCompare.msg)
                        else:
                            err = Error(ErrorCode.REQUEST_ERROR, errJob.msg)
                    else:
                        err = Error(ErrorCode.DATA_ERROR, "don't have jobId or compareId in report job")
            else:
                err = Error(ErrorCode.DATA_ERROR, "request workflow failed")
        return err

    def getWorkPath(self):
        return self._workPath

    def getResourcePath(self):
        return self._resourcePath

    def loadPlugins(self) -> Error:
        pass
