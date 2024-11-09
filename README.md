# dolphin-anty
                       
<img style="border-radius: 5px" height="50px" src="https://raw.githubusercontent.com/CrocoFactory/.github/main/branding/sensei/logo/bookmark.svg">

The package for interacting with API of anti-detect browser Dolphin Anty. The project is powered by 
[Sensei](https://sensei.crocofactory.dev)

# Example:
Here is code example
               
Sync example

```python
from dolphin_anty.sync_api import ProfileAPI
from dolphin_anty import Context

Context.api_token = 'your_token'

profiles = ProfileAPI.list()
print(profiles) 
```

```text
[ProfileAPI(id=448528176, team_id=3600451, user_id=3682454, name='Profile 1', ...), ...]
```

Async example:
```python
import asyncio

from dolphin_anty.async_api import ProfileAPI
from dolphin_anty import Context

Context.api_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNTk2ZTRmMThkMjExMTBjNDUzN2I0ZmMzYjk1YmY2NjEzYTkyNjE4MmE5NTc4NzM1ZGY1NmQxNDVlODIyNmFiMGFmYTc1MmFkNTIxZGQ2OGIiLCJpYXQiOjE3MzExNjIwNTQuMDc4MjY4LCJuYmYiOjE3MzExNjIwNTQuMDc4MjcxLCJleHAiOjE3Mzg5MzgwNTQuMDcwNzIyLCJzdWIiOiIzNjgyNDU0Iiwic2NvcGVzIjpbXX0.sEHEwRYtHJ-_f6orj_j0iVSuSbHWo9fgF-0Eu3cHHVTTqu0cNJjUxcttaEN8wS2yCbukB8CQzp10PdVfOFoRtI-nR2wPB-mBA9Hwj5o2aqZcDngMGiKlYQfgdhpL-AtYZIzEqq9GmlbomMvhT4nwUCwB6xlv7PtAGGY-hLnayaCCTJjZoWneaczbSkmuoA7tb0IK8ee3PyqSUY7-WF-Io8a2cs7v7hCKZFJe_KTJx8CykXZ-llpxosHojPc7iTtQPxgdq3xjuJ16Dy6VA3tIyM_Aqws57KiYe4XsO4Mi8EbF62FoAXb_rjx_1p2Gyi1k2ITezhamPkK-eo1pvkCLJwZmZnNqbYbACZ0GeaFHJmfzL_CrGs6G96m0Q3yRY2fDQiN_rxL9E4tIQ2juUHL6dKoR8LXGwglFvrvkxHSYrxdcxS-pVtHTdDDjRhJ5WshV-5aRp6rAaiJSR-FKAPq0fjNka1oWNvb_VoUZxPW64p0sdEe-6oOLAQq3rVn4oImrpjUVK5WqPnQYUmdU00xbTKbN3WvUQ8Um5sX12SIn1Qf4iryJ-d68fpq-wBoM4Qa-twnmGvr-tlO7vP06elLdazQTUnRcyIdkfJYOzEtKIp9WIYbq7cTqGiJvm75LzQtAvR2jRzG-PuqZFycmrnzBbo_B-ujCei1aRAARYS9aRDY'


async def main() -> None:
    profiles = await ProfileAPI.list()
    print(profiles)

asyncio.run(main())
```

```text
[ProfileAPI(id=448528176, team_id=3600451, user_id=3682454, name='Profile 1', ...), ...]
```

# Installing dolphin-anty
To install `dolphin-anty` from PyPi, you can use that:

```shell
pip install dolphin-anty
```

To install `dolphin-anty` from GitHub, use that:

```shell
pip install git+https://github.com/blnkoff/dolphin-anty.git
```