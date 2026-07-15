# Code organization

## Portable release scripts

- `config.py` defines paths relative to the repository root.
- `reproduce_key_results.py` reconstructs selected headline values from the public derived tables and figure source data.
- `validate_release.py` checks folder contents, CSV readability, figure presence, prohibited files, and workstation-specific paths in the public layer.

Run from the repository root:

```powershell
python code\validate_release.py
python code\reproduce_key_results.py
```

## Interpretation boundary

The scripts reproduce descriptive country-level comparisons. They do not estimate individual-level effects, causal effects, preventable burden, or national performance.
