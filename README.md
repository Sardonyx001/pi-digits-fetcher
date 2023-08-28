# Pi Digits Fetcher

A tiny Python module that retrieves (arbitrary ranges of) decimal digits of the mathematical constant π (pi) using the [pi.delivery API](https://pi.delivery/).

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Class Details](#class-details)
- [Contributing](#contributing)
- [License](#license)

## Overview

I realized there was no obvious way to retrieve arbitrary ranges of pi digits so I wrote this tiny wrapper. It interacts with the pi.delivery API to fetch decimal digits of π (pi) and provides functionality to retrieve a specified number of digits from a given starting position.

Please do not abuse this API as it is provided for free. This module also does basic caching with requests_cache however it is only rudimentary, further caching functionalities are your own responsibility!

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/sardonyx001/pi-digits-fetcher.git
   cd pi-digits-fetcher
   ```

2. Install the required dependencies using `pip`:

   ```sh
   pip install requests requests_cache
   ```

## Usage

You can use the `PiDigits` class to fetch decimal digits of π (pi).

```python
from pidigits import PiDigits

pi_digits = PiDigits()
digits = pi_digits.get_next(100)  # Fetches the next 100 digits of pi starting from the default position
print(digits)  # Prints the fetched digits as a string
```

Example of extended usage:

```python
import pidigits

digits = pidigits.PiDigits()

""" Fetch the next 12345 digits of π (pi) starting 
    from position 0, i.e. the first decimal position 
    (and print the last 10) """
print(digits.get_next(12345)[-10:])
#Output: 4584002836

""" Fetch the next 12345 digits of π (pi) starting 
    from position 10 (and print the last 10) """
print(digits.get_next(12345,10)[-10:])
#Output: 2634165542

""" Fetch the next 12346 digits of π (pi) starting 
    from position 10 (and print the last 10) """
print(digits.get_next(12346,10)[-10:])
#Output: 6341655425 
""" Notice that its the output of 
    digits.get_next(12345,10)[-10:] shifted by 1 digit) """
```

## Class Details

### `PiDigits`

The main class to interact with the pi.delivery API and fetch decimal digits of π (pi).

- `get_encoded_api_url(num=None, start=None)`: Encodes the API URL using the number of digits to fetch and the position in pi's decimal numbers from where to start fetching.
- `get_next(num=None, start=None)`: Gets the next `num` digits starting from the position of `start`. Returns a `ListConvertibleString` representing the desired range of digits.
- `_get_range(start, end)`: Returns a string indicating a range of digits being fetched.

### `ListConvertibleString`

A helper class that extends the `str` class to allow for a list of digits representation.

- `to_list()`: Returns a list of digits (int) split from the original string.

## Contributing

Contributions are welcome! If you find any issues or want to enhance the functionality, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

---
