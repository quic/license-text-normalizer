Copyright (c) 2020, Qualcomm Innovation Center, Inc. All rights reserved.  
SPDX-License-Identifier: BSD-3-Clause  

# License Text Normalizer
Library that provides license text normalization functionality in Python.

A javascript implementation is also available: https://github.com/quic/license-text-normalizer-js

## Requirements
* Python 3.8+
* `pip`, `setuptools`

## Usage

### Normalize a license text using the default set of delimiters
```
from license_text_normalizer import normalize_license_text

text = "/* Copyright 2010 Google Inc. All Rights Reserved.\n */"

normalized_text = normalize_license_text(text)

assert normalized_text == "Copyright 2010 Google Inc. All Rights Reserved."
```

### Normalize a license text using a custom set of delimiters
```
from license_text_normalizer import normalize_license_text

text = " XXX  Copyright 2010 Google Inc. All Rights Reserved."

normalized_text = normalize_license_text(text, delimiters=["XXX"])

assert normalized_text == "Copyright 2010 Google Inc. All Rights Reserved."
```

## Development
See [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

## License
License Text Normalizer is licensed under the BSD 3-clause “New” or “Revised” License. See [LICENSE](LICENSE) for the full license text.
