# ERICA python utilities

A set of python scripts for common tasks in ERICA.

## Limiting memory of python scripts

#### Why?
Python scripts that consume too much memory do not terminate gracefully in ERICA. 
Outside of ERICA, python scripts are typically terminated by the operating system. 
In ERICA, if a python scripts consumes too much memory, it will bring the instance down.
This results in having to restart your workspace.

#### Solution
The kill.py script contains a python decorator that automatically kills your script if it uses too much memory. 
The use of the script is strongly recommended to minimize ERICA annoyances and frustrations.
This is an example of how to use it:

```python
from kill import set_memory_limit

@set_memory_limit(8)  # Set the memory limit to 8 GB
def main():
    # code here

if __name__ == "__main__":
    main()
```

Another example:
```python
from kill import set_memory_limit

@set_memory_limit(2)  # Set the memory limit to 2 GB
def some_function(blah, blah2):
    # code here

```
