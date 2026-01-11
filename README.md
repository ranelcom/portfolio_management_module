# Python Portfolio management module

## Python venv

### Create venv
``` powershell
python -m venv .venv 
```

### Activate venv
``` powershell
.\.venv\Scripts\activate.ps1
```

### Deactivate venv
``` powershell
deactivate
```

## Install requirements
```
pip install -r requirements.txt
```

## Run Portfolio Management Module
``` powershell
python .\main.py
```

## Testing

### Simple test
``` powershell
pytest
```

### Coverage test
``` powershell
pytest test_portfolio.py -v --cov=test_portfolio --cov-report=html
```