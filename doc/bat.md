[MS Batch](https://learn.microsoft.com/de-de/windows-server/administration/windows-commands/pushd)

- `cd` change directory
- `md` make directory
- `rd` remove directory
- `dir` 
- `exit` to close the console
- `start` starts program in a new window
- `time` displays the time
- `pause` 

- `move` moves files
    ```
    move <source file> <destination dir>
    move file.txt .\example_dit
    ```
- `path` display or set the path variable
- `ren` rename file and directory
    ```
    ren <source files> <destination file>
    ```
- `find` search for a string in a file or input and outputs the matching line
- `fc` compares two files and outputs the differences

- `.` current directory
- `>` create a file
```
Arguments for echo function:
echo %1
echo %2

Setting variables /A is for numercal values:
set /A name=value
set say=Hello World
echo %say%

Making variable local:
SETLOCAL 
set /A local=value
ENDLOCAL
local doesn't exist anymore
```

# Strings
```
set a=
if [%a%]==[] echo "is empty"
set first=hello
set second=world
:: concataneted
set final=%first% %second%
echo final

set str=helloWorld
:: depicts string from 0 to 5 excluding
set str=%str:~0,5%

set long="this is a long string"
:: depicts 5 characters from the end of the string
set str=%str:~-5%
:: remove from "long" the string -> replace the string with no value
set new=%str:long=%
:: remove first and last value from the string:
set str=%str:~1,-1%

:: convert to integer
set var=60
set /A var2=%var%+40 

```

# Flow Control 

## goto
```
goto :label2

:label1

## if else
if "string"==%str% echo str is equal
:label2
if "string"==%str% (
    echo str is equal
)
else (
    echo str is not equal
)
```
## for loop
`FOR /L %%i IN (start,step,end) DO (`
```
FOR /L %%i IN (0,2,8) DO (
    ECHO %%i
)
:: reverse loop
FOR /L %%i IN (10,-1,1) DO (
    ECHO %%i
)
```
`/L` denotes that the loop is going through range
# operators
- EQU test equality btw. two objects
- NEQ test if two are not equal
- LSS test if left object is less than the right
- LEQ test if left object is less or equal than right
- GTR test if right object is less than the left
- GEQ test if right object is less or equal than left

- AND
- OR
- NOT

## bit wise
- &
- |
- ^ xor 1^1=0

# Arrays
Each element has the same type.
- create Arrays
```
set myArray=1 2 3 4
(for %%i in (%myArray%) do (
    ech0 %%i
    echo !myArray[%%i]!
))

set arr[0]=1
set arr[1]=2
set arr[2]=3
:: accessing one element
echo %arr[0]%
```

# Function
## Declaration

## Definition