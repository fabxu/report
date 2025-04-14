from core import constant
from core.utils import utils


class Job:
    def __init__(self, param: dict):
        self.name = utils.getValue(param, constant.KEY_NAME, None)
        self.id = utils.getValue(param, constant.KEY_ID, None)
        self.workflowTemplateId = utils.getValue(param, constant.KEY_WORKFLOW_TEMPLATE_ID, None)
        self.workflowTemplateName = utils.getValue(param, constant.KEY_WORKFLOW_TEMPLATE_NAME, None)
        self.workflowTemplateVersion = utils.getValue(param, constant.KEY_WORKFLOW_TEMPLATE_VERSION, None)
        self.customConfig = utils.getValue(param, constant.KEY_CUSTOM_CONFIG, None)
        self.evalObjectSoc = utils.getValue(param, constant.KEY_EVAL_OBJECT_SOC, None)
        self.evalObjectVersion = utils.getValue(param, constant.KEY_EVAL_OBJECT_VERSION, None)
        self.evalObjectCi = utils.getValue(param, constant.KEY_EVAL_OBJECT_CI, None)
        self.spaceId = utils.getValue(param, constant.KEY_SPACE_ID, None)
        self.spaceName = utils.getValue(param, constant.KEY_SPACE_NAME, None)
        self.inputType = utils.getValue(param, constant.KEY_INPUT_TYPE, None)
        dataset = utils.getValue(param, constant.KEY_DATASET_INPUT, None)
        if dataset is not None:
            self.datasetId = utils.getValue(param, constant.KEY_ID, None)
            self.datesetName = utils.getValue(param, constant.KEY_NAME, None)
        self.scriptInputType = utils.getValue(param, constant.KEY_SCRIPT_INPUT_TYPE, None)
        self.relatedIssues = utils.getValue(param, constant.KEY_RELATED_ISSUE, None)
        self.evalResultsPath = utils.getValue(param, constant.KEY_EVAL_RESULT, None)
        self.jobId = utils.getValue(param, constant.KEY_JOB_ID, None)
        compareJobs = utils.getValue(param, constant.KEY_COMPARE_JOBS, [])
        if len(compareJobs) > 0:
            self.compareId = compareJobs[0][constant.KEY_ID]
        else:
            self.compareId = None
        self.startTime = utils.getValue(param, constant.KEY_START_TIME, None)
        self.endTime = utils.getValue(param, constant.KEY_END_TIME, None)
        self.runningDuration = utils.getValue(param, constant.KEY_RUNNING_DURATION, None)
        self.createdBy = utils.getValue(param, constant.KEY_CREATED_BY, None)
        self.updatedBy = utils.getValue(param, constant.KEY_UPDATE_BY, None)
        self.createdAt = utils.getValue(param, constant.KEY_CREATED_AT, None)
        self.updatedAt = utils.getValue(param, constant.KEY_UPDATED_AT, None)
        self.evalSavePath = ""


class Workflow:
    def __init__(self, param: dict):
        self.name = utils.getValue(param, constant.KEY_NAME, None)
        self.id = utils.getValue(param, constant.KEY_ID, None)
        self.uuid = utils.getValue(param, constant.KEY_UUID, None)
        self.type = utils.getValue(param, constant.KEY_TYPE, None)
        self.spaceId = utils.getValue(param, constant.KEY_SPACE_ID, None)
        self.spaceName = utils.getValue(param, constant.KEY_SPACE_NAME, None)
        self.version = utils.getValue(param, constant.KEY_VERSION, None)
        self.policyId = utils.getValue(param, constant.KEY_POLICY_ID, None)
        uploadReportPath = utils.getValue(param, constant.KEY_TEMPLATE_PATH, [])
        if len(uploadReportPath) > 0:
            self.templatePath = uploadReportPath[0][constant.KEY_URL]
            self.templateName = uploadReportPath[0][constant.KEY_NAME]
        self.createdBy = utils.getValue(param, constant.KEY_CREATED_BY, None)
        self.updatedBy = utils.getValue(param, constant.KEY_UPDATE_BY, None)
        self.createdAt = utils.getValue(param, constant.KEY_CREATED_AT, None)
        self.updatedAt = utils.getValue(param, constant.KEY_UPDATED_AT, None)
        self.savePath = None
