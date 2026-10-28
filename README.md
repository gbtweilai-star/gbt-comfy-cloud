# comfy_cloud

**One capability bit from GBT V8, packaged standalone.** No. 19 of 341,
`creation` domain (Creation).

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
</p>

> **云卡 ComfyUI 触手**（主人令 2026-10-13「她不需要 ComfyUI，直接使用触手就可以生产出高质量视频」）：把云卡上的 ComfyUI **包成她自己的器官**——她不用知道 ComfyUI 是什么。本机到 8188 没路（实测代理 404），所以所有调用都在**卡内**执行，经云卡触手 pod_link 的 run 递脚本、down 取产物并回读哈希对账。op：读 `status/nodes/models/queue/history`；写 `submit`（原样图）· **`video`（一句话 → sd15 首帧 → svd_xt 动作 → ffmpeg 编码 mp4）** · `fetch`（卡→本机对账）· `free`。常用说法：出视频 / 生成视频 / 高质量视频 / 让她出片 / 云卡出片 / 不要碰 ComfyUI / 触手自己出。铁律：令牌不回显 · **产物以卡上与本机 sha256 一致为准** · 卡上 `mm_sd_v15_v2.ckpt` 实测认不出类型（不许当默认）。

That description is copied verbatim from the registry. `tests/test_spec.py` pins it,
so documentation drift fails the build instead of shipping quietly.

## What this package actually is

It is the **contract** for one capability: its name, its parameters, the values it
accepts, and whether it can change state that cannot be restored. It is not the
implementation — that lives in the runtime this bit was extracted from.

So `run()` goes through a narrow `Backend` protocol, and the default backend is a
stub that **says so**:

```
status="validated"   backend="stub"   data={"executed": false}
```

Never `status="ok"`. A stub that reports success is worse than no stub, because the
caller stops looking for the real thing.

## Install

```bash
git clone https://github.com/gbtweilai-star/gbt-comfy-cloud.git
cd gbt-comfy-cloud
python -m pip install -e ".[dev]"
```

## Use

```bash
python -m gbt_comfy_cloud info                  # capability card
python -m gbt_comfy_cloud spec --json           # machine-readable contract
python -m gbt_comfy_cloud check --payload '{}'
python -m gbt_comfy_cloud run   --payload '{}'
```

Real `info` output from this machine:

```text
comfy_cloud  (creation)  v1.0.0
----------------------------------------
**云卡 ComfyUI 触手**（主人令 2026-10-13「她不需要 ComfyUI，直接使用触手就可以生产出高质量视频」）：把云卡上的 ComfyUI **包成她自己的器官**——她不用知道 ComfyUI 是什么。本机到 8188 没路（实测代理 404），所以所有调用都在**卡内**执行，经云卡触手 pod_link 的 run 递脚本、down 取产物并回读哈希对账。op：读 `status/nodes/models/queue/history`；写 `submit`（原样图）· **`video`（一句话 → sd15 首帧 → svd_xt 动作 → ffmpeg 编码 mp4）** · `fetch`（卡→本机对账）· `free`。常用说法：出视频 / 生成视频 / 高质量视频 / 让她出片 / 云卡出片 / 不要碰 ComfyUI / 触手自己出。铁律：令牌不回显 · **产物以卡上与本机 sha256 一致为准** · 卡上 `mm_sd_v15_v2.ckpt` 实测认不出类型（不许当默认）。

gated      : True   <- needs explicit consent
external   : False
multi-op   : True
params     : (none)
values     : status, nodes, models, queue, history
```

Wire a real implementation:

```python
from gbt_comfy_cloud import run

class MyBackend:
    name = "my-backend"
    def invoke(self, cap, payload):
        return {"cap": cap, "handled": sorted(payload)}

result = run({}, backend=MyBackend())
assert result.status == "ok"
```

## Parameters

| name | required | notes |
|---|---|---|
| — | no | the registry declares no required parameters |

Registry hint (`params_hint`): (empty)

**注册表登记的取值 / 子动作（5 个）**：`status`、`nodes`、`models`、`queue`、`history`

Types are deliberately absent: the registry does not declare them, and an invented
type is worse than no type, because callers believe it.

## Boundaries

- Gated: this bit is marked `safe: false` in the registry — it can change state that no inverse action restores.
- No external service dependency declared.
- Multi-op (`multi_op: true`): several sub-actions share one name — read `op` before calling.
- No implementation ships here. Bring a backend; the protocol is one method.

## What this is not

Not a wrapper around a hosted API. Not a model. Not a promise that calling it does
anything on its own. It is the typed seam plus the validation, which is the part that
stays correct even when the implementation changes.

## Tests

```bash
python -m pytest
```

```text
20 passed, 3 skipped in 0.11s
```

## Provenance

| field | value |
|---|---|
| capability | `comfy_cloud` |
| domain | `creation` |
| handler | `comfy_cloud` |
| safe | `False` (gated = `True`) |
| external | `False` |
| atlas page | [creation/comfy_cloud](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/creation/comfy_cloud.md) |
| full index | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

The parent README says 348 capabilities; an AST pass over the registry enumerates
`341 + 0 unimplemented + 0 disabled = 341`. The extra 7 are historical duplicates.
Numbering here follows 341 and matches the `gbt-caps` index one-to-one.

## License

MIT.
