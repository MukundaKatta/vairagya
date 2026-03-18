# vairagya

**Vairagya — Digital Detox Coach. AI-guided digital wellness and screen time management.**

![Build](https://img.shields.io/badge/build-passing-brightgreen) ![License](https://img.shields.io/badge/license-proprietary-red)

## Install
```bash
pip install -e ".[dev]"
```

## Quick Start
```python
from src.core import Vairagya
 instance = Vairagya()
r = instance.manage(input="test")
```

## CLI
```bash
python -m src status
python -m src run --input "data"
```

## API
| Method | Description |
|--------|-------------|
| `manage()` | Manage |
| `automate()` | Automate |
| `schedule()` | Schedule |
| `execute()` | Execute |
| `get_status()` | Get status |
| `optimize()` | Optimize |
| `get_stats()` | Get stats |
| `reset()` | Reset |

## Test
```bash
pytest tests/ -v
```

## License
(c) 2026 Officethree Technologies. All Rights Reserved.
