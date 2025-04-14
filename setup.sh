#!/bin/bash

ads_name="ads-cli"
ads_sh_name="ads-cli.sh"
ads_credential_name="credentials"
usr_bin_path="/usr/local/bin"
ads_credential_target_path="$HOME/.aws"
src_path="./tools"

if [ ! -f "$usr_bin_path/$(basename "$ads_name")" ]; then
  sudo cp $src_path/$ads_name $usr_bin_path
  sudo chmod +x /usr/local/bin/ads-cli
  echo "$ads_name已成功拷贝到$usr_bin_path"
else
    echo "$usr_bin_path/$ads_name已存在，未进行拷贝"
fi

if [ ! -f "$usr_bin_path/$(basename "$ads_sh_name")" ]; then
  sudo cp $src_path/$ads_sh_name $usr_bin_path
  chmod +x /usr/local/bin/ads-cli.sh
  echo "$ads_sh_name已成功拷贝到$usr_bin_path"
else
    echo "$usr_bin_path/$ads_sh_name已存在，未进行拷贝"
fi

if [ ! -f "$ads_credential_target_path/$(basename "$ads_credential_name")" ]; then
  sudo mkdir -p $ads_credential_target_path
  sudo cp $src_path/$ads_credential_name $ads_credential_target_path
  echo "$ads_credential_name已成功拷贝到$ads_credential_target_path"
else
    echo "$ads_credential_target_path/$ads_credential_name已存在，未进行拷贝"
fi