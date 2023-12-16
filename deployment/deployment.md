# [1. About FastAPI versions](https://fastapi.tiangolo.com/de/deployment/versions/)
- 현재 FastAPI의 버전이 `0.x.x` 인 이유는 현재로 정기적으로 새로운 기능이 추가되고 있고 계속해서 버그가 수정되고 있기 때문입니다.
- 현재 작성중인 애플리케이션에서 동작하는 fastpi 버전을 고정하세요
    ```
    fastapi==0.45.0
    또는
    fastapi>=0.45.0,<0.46.0
    ```
- 사용가능한 버전을 확인하세요 : [Release Notes.](https://fastapi.tiangolo.com/de/release-notes/)
- PATCH 버전에서는 버그나 non-breaking change를 포함합니다.
- MINOR 버전에서는 breaking change를 포함합니다.
- Test를 실행하여 FastAPI 버전을 업그레이드 하세요
- starlette 버전을 고정할 필요는 없습니다.
- pydantic은 FastAPI에 대한 테스트를 자체적으로 수행합니다.
<br/><br/>