#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=src python -m gbt_comfy_cloud info
PYTHONPATH=src python -m gbt_comfy_cloud check --payload '{}'
PYTHONPATH=src python -m gbt_comfy_cloud run   --payload '{}'
