#/usr/bin/env bash

pylint ./cmd.py eptc | tee pylint_report.log
