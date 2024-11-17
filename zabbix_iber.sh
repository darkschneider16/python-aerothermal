#!/bin/bash

# Script to get energy consumptions from the day before

SCRIPT=$(basename "$0")
VIRTUAL_ENV="$HOME/.venv"
VIRTUAL_PACKAGE="python3-venv"
PYTHON="python"
PIP_PACKAGES="zabbix_utils deprecated requests"
SCRIPT_DIR="$HOME/python-aerothermal"
SCRIPT_PY="${SCRIPT_DIR}/zabbix_iber.py"
IDE_CRED="/etc/ide-credentials.ini"
LOG_FILE="/var/log/zabbix-iber.log"

# First we check if the arguments are fine
function usage {
        echo "Usage: $(basename "$0")"
        echo "    -c file containing the i-DE credentials"
        echo "    -l logfile"
        echo "    -h usage"
        exit 1
}

if [[ ${#} -eq 0 ]]; then
        usage
fi

while getopts "c:l:h" option
do
        case "${option}" in
                c)      IDE_CRED=${OPTARG}
                        ;;
                l)      LOG_FILE=${OPTARG}
                        ;;
                h)      usage
                        ;;
                :)      echo -e "Option requires an argument"
                        usage
                        ;;
                ?)      echo -e "Invalid command option"
                        usage
                        ;;
        esac
done

if ! [ ${OPTIND} -eq 5 ]
then
        usage
fi

echo "$(date) >>> Begin of ${SCRIPT}" >> "${LOG_FILE}"

# We must check if a python virtualenv is installed
if [ ! -f "${VIRTUAL_ENV}/bin/activate" ]
then
        # We must create the python virtualenv but we must check if we have the right tool
        if ! dpkg -l | grep ${VIRTUAL_PACKAGE} >> "${LOG_FILE}"
        then
                echo "> Before continuing you must install the package: ${VIRTUAL_PACKAGE}" >> "${LOG_FILE}"
                echo " $ sudo apt install ${VIRTUAL_PACKAGE}" >> "${LOG_FILE}"
                exit 1
        else
                # We create the directory but if it exists we must recreate it
                if [ -d "${VIRTUAL_ENV}" ]
                then
                        rm -Rf "${VIRTUAL_ENV}"
                fi
                mkdir "${VIRTUAL_ENV}"
                # We create the python virtualenv
                python3 -m venv  "${VIRTUAL_ENV}" >> "${LOG_FILE}"
        fi
fi

# We must assure that pip packages are installed in the python virtual env
source "${VIRTUAL_ENV}"/bin/activate
pip install --upgrade pip >> "${LOG_FILE}"
for p in ${PIP_PACKAGES}
do
        pip install "$p" >> "${LOG_FILE}"
done

{
        echo "$(date) >>> Begin of ${SCRIPT_PY} invocation"
        ${PYTHON} "${SCRIPT_PY}" "${IDE_CRED}"
        echo "$(date) >>> End of ${SCRIPT_PY} invocation"
} >> "${LOG_FILE}"

# And Just for convenience
deactivate

echo "$(date) >>> End of ${SCRIPT}" >> "${LOG_FILE}"