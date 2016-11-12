#/usr/bin/env bash

pylint ./cmd.py ./setup.py pypoabus | tee pylint_report.log
