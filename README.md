# envalidate #

---
validating and accessing environment variables in python

* check that your program runs with all demand and validate environment variables

* immutable API for your environment variables

# API #

---

**envalidate.read_env(environment, validators, reporter)**

returns a sanitized, immutable environment object, and accepts three positional arguments:

* environment - An object containing your env vars (eg. os.environ)

* validators - An object that specifies the format of required vars.

* reporter - Pass in a function to override the default error handling and console output. See
  src/reporter.ts for the default implementation.

By default, read_env() will log an error message and throw if any required env vars are missing or
invalid. You can override this behavior by writing your own reporter.

```sh

import os

from envalidate import Bool, Email, IPAddress, Json, Number, Port, Str, Url, read_env

validators = {
    "APP_NAME": Str(),
    "IP": IPAddress(default="127.0.0.1"),
    "PORT": Port(default=8000),
    "IS_TEST": Bool(),
    "EMAIL": Email(default="user@test.com"),
    "HOME_PAGE": Url(default="https://www.google.com"),
    "CONFIG": Json(desc="app config"),
    "AGENTS": Number(choices=[1, 2, 3, 4, 5, 6]),
}

env = read_env(os.environ, validators)

```

# Validator types #

---

Python's os.environ only stores strings, but sometimes you want to retrieve other types (booleans, numbers), or validate that an env var is in a specific format (JSON, url, email address). To these ends, the following validation functions are available:

* Str() - Passes string values through, will ensure an value is present unless a default value is given. Note that an empty string is considered a valid value

* Bool() - Parses env var strings "1", "0", "true", "false", "t", "f" into booleans

* Number() - Parses an env var (eg. "42", "0.23", "1e5") into a Number

* Email() - Ensures an env var is an email address

* IPAddress() - Ensures an env var is an ip address (v4 or v6)

* Port() - Ensures an env var is a TCP port (1-65535)

* Url() - Ensures an env var is a url with a protocol and hostname

* Json() - Parses an env var with json.loads

Each validation function accepts an (optional) object with the following attributes:

* choices - An Array that lists the admissable parsed values for the env var.

* default - A fallback value, which will be present in the output if the env var wasn't specified. Providing a default effectively makes the env var optional. Note that default values are not passed through validation logic.

* desc - A string that describes the env var.

* example - An example value for the env var.

* docs - A url that leads to more detailed documentation about the env var.

# Custom validators #

---

You can easily create your own validator class with envalidate.EnValidator. 
It takes a function as its only parameter, and should either return a cleaned value, or throw if the input is unacceptable:

```sh
from typing import Any

from envalidate import EnValidator
from envalidate.exceptions import EnvError

class UpperCaseValidator(EnValidator):
    def __validate__value__(self, value) -> Any:
        if not value:
            raise EnvError(f"{value} is empty.")
        return value.upper()

```

# Error Reporting #

---

By default, if any required environment variables are missing or have invalid values, envalidate will log a message and raise exception. 
You can override this behavior by passing in your own Reporter.

Additionally, envalidate exposes EnvError and EnvMissingError, which can be checked in case specific error handling desired.

# Motivation #

---

[Node envalid package](https://www.npmjs.com/package/envalid)

[The Twelve-Factor App](http://www.12factor.net/config)

