from core.errors.error import Error, ErrorCode
import subprocess


def getValue(map: dict, key: str, defaultValue: any) -> any:
    if key in map:
        return map[key]
    else:
        return defaultValue


def downloadFromS3(key_profile: str, s3Path: str, savePath: str) -> Error:
    cmd = f"ads-cli.sh --profile {key_profile} cp {s3Path} {savePath}"
    print(cmd)
    result = subprocess.run(cmd, shell=True)
    if result.stderr:
        return Error(code=ErrorCode.REQUEST_ERROR, msg=result.stderr)
    if result.returncode != 0:
        return Error(code=ErrorCode.REQUEST_ERROR,
                     msg=f"s3 download failed, return code: {result.returncode}, address: {s3Path}")
    return Error(code=ErrorCode.SUCCESS)
