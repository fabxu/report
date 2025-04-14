#!/bin/bash

declare config_file="$HOME/.aws/credentials"

# Check if aws credentials file exists
if [ ! -f "$config_file" ]; then
    echo -e "\033[31m [E] \033[0m AWS credentials file not found at $config_file."
    echo "Please run 'sudo pip3 install awscli' and 'aws configure' first. See https://ones.ainewera.com/wiki/#/team/Ttz6FJha/space/C6ZKWiJU/page/EuBEuksg"
    exit 1
fi

# Check if ads-cli is installed
if ! command -v ads-cli &> /dev/null; then
    echo -e "\033[31m [E] \033[0m ads-cli could not be found."
    echo "Please run 'curl -sSL http://fileserver.devops.senseauto.com/infra/install-ads.sh | bash'"
    exit 1
fi

# Function to parse aws credentials file and extract aws_access_key_id
get_aws_access_key_id() {
    awk -F "=" -v section="$1" 'BEGIN{ in_section = 0; } {
        gsub(/^[ \t]+|[ \t]+$/, "", $1);
        gsub(/^[ \t]+|[ \t]+$/, "", $2);

        if ($1 ~ /^\[.*\]$/) {
            in_section = ($1 == "[" section "]");
        }

        if (in_section && $1 == "aws_access_key_id" && $2 != "") {
            print $2;
            exit;  # Stop processing after finding the key
        }
    }' "$config_file"
}

# Function to parse aws credentials file and extract aws_secret_access_key
get_aws_secret_access_key() {
    awk -F "=" -v section="$1" 'BEGIN{ in_section = 0; } {
        gsub(/^[ \t]+|[ \t]+$/, "", $1);
        gsub(/^[ \t]+|[ \t]+$/, "", $2);

        if ($1 ~ /^\[.*\]$/) {
            in_section = ($1 == "[" section "]");
        }

        if (in_section && $1 == "aws_secret_access_key" && $2 != "") {
            print $2;
            exit;  # Stop processing after finding the key
        }
    }' "$config_file"
}

declare -a modified_params=()
declare profile=""
declare aws_access_key_id=""
declare aws_secret_access_key=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --profile)
            profile="$2"

            aws_access_key_id=$(get_aws_access_key_id "$profile")
            if [ -z "$aws_access_key_id" ]; then
                echo -e "\033[31m [E] \033[0m aws_access_key_id not found for profile '$profile'."
                exit 1
            fi

            aws_secret_access_key=$(get_aws_secret_access_key "$profile")
            if [ -z "$aws_secret_access_key" ]; then
                echo -e "\033[31m [E] \033[0m aws_secret_access_key not found for profile '$profile'."
                exit 1
            fi

            shift 2
            ;;
        *)
            # Other parameters, add to the array
            modified_params+=("$1")
            shift
            ;;
    esac
done

# Modify s3:// parameters in the array
for ((i=0; i<${#modified_params[@]}; i++)); do
    echo "modified_params[$i] = ${modified_params[$i]}"
    if [[ ${modified_params[$i]} == s3://* ]]; then
        modified_params[$i]="s3://$aws_access_key_id:$aws_secret_access_key@${modified_params[$i]#s3://}"
    fi
done

ads-cli "${modified_params[@]}"

