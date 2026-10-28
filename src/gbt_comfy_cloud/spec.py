"""The capability contract, copied verbatim from the GBT V8 registry.

Do not hand-edit: ``tests/test_spec.py`` pins every field against the
registry snapshot so drift fails the build instead of shipping quietly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

_RAW = r"""{
 "name": "comfy_cloud",
 "domain": "creation",
 "desc": "**云卡 ComfyUI 触手**（主人令 2026-10-13「她不需要 ComfyUI，直接使用触手就可以生产出高质量视频」）：把云卡上的 ComfyUI **包成她自己的器官**——她不用知道 ComfyUI 是什么。本机到 8188 没路（实测代理 404），所以所有调用都在**卡内**执行，经云卡触手 pod_link 的 run 递脚本、down 取产物并回读哈希对账。op：读 `status/nodes/models/queue/history`；写 `submit`（原样图）· **`video`（一句话 → sd15 首帧 → svd_xt 动作 → ffmpeg 编码 mp4）** · `fetch`（卡→本机对账）· `free`。常用说法：出视频 / 生成视频 / 高质量视频 / 让她出片 / 云卡出片 / 不要碰 ComfyUI / 触手自己出。铁律：令牌不回显 · **产物以卡上与本机 sha256 一致为准** · 卡上 `mm_sd_v15_v2.ckpt` 实测认不出类型（不许当默认）。",
 "handler": "comfy_cloud",
 "safe": false,
 "external": false,
 "requires_params": false,
 "params": [],
 "params_hint": "",
 "multi_op": true,
 "ops": [
  "status",
  "nodes",
  "models",
  "queue",
  "history"
 ],
 "ops_hint": ""
}"""


@dataclass(frozen=True)
class CapSpec:
    """Immutable description of one capability bit."""

    name: str
    domain: str
    desc: str
    handler: str
    safe: bool
    external: bool
    requires_params: bool
    params: Tuple[str, ...] = ()
    params_hint: str = ""
    multi_op: bool = False
    ops: Tuple[str, ...] = ()
    ops_hint: str = ""

    @property
    def gated(self) -> bool:
        """True when the registry marks this bit ``safe: false``.

        Gated does not mean "dangerous"; it means the action can change state
        that cannot be restored by running the inverse action.
        """
        return not self.safe

    @property
    def summary(self) -> str:
        """First clause of the description, for one-line listings."""
        for sep in ("\uff08", "\uff1b", "\u3002", ";"):
            if sep in self.desc:
                head = self.desc.split(sep, 1)[0].strip()
                if head:
                    return head
        return self.desc.strip()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "domain": self.domain,
            "desc": self.desc,
            "handler": self.handler,
            "safe": self.safe,
            "gated": self.gated,
            "external": self.external,
            "requires_params": self.requires_params,
            "params": list(self.params),
            "params_hint": self.params_hint,
            "multi_op": self.multi_op,
            "ops": list(self.ops),
            "ops_hint": self.ops_hint,
        }


_data = json.loads(_RAW)

SPEC = CapSpec(
    name=_data["name"],
    domain=_data["domain"],
    desc=_data["desc"],
    handler=_data["handler"],
    safe=_data["safe"],
    external=_data["external"],
    requires_params=_data["requires_params"],
    params=tuple(_data["params"]),
    params_hint=_data["params_hint"],
    multi_op=_data["multi_op"],
    ops=tuple(_data["ops"]),
    ops_hint=_data["ops_hint"],
)
