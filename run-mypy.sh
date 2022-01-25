#!/bin/bash

pip install -r ./requirements/dev.txt > /dev/null
MYPYPATH=. mypy --show-traceback --namespace-packages --explicit-package-bases .
