
# Setup VS Code

1. install the extension packages for VSCode:
   1. *franneck94*:
      1. **Coding Tools Extension Pack**: independent from the programming language
      2. **Python Dev Extension Pack**: tools for development with Paython
         1. python docstring generator: to generate the doc strings
2. Generate Python Config Files
   1. 'strg'+'shift'+'p'
   2. Python Config: Generate Python Config Files: will generate some cofiguration and setting files
3. Select the Python interpreter
4. *Terminal: Create new Terminal* and select the virtual environment
5. setup docstring:
   1. open settings by *str+*
   2. go to extensions/Python Docstring Generator config
   3. set the Docstring formate to numpy, google or sphinx - google is prefered

## VS Code Debugger

The debugger is configured to run the debugger on the current open file (see first configuration). In `launch.json` file from *.vscode* folder it can be configured to always start from the main file. (see second configuration).

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debug: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        }
    ]
}

{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debug: Current File",
            "type": "python",
            "request": "launch",
            "program": "${workspacefolder}/dkb/api.py",
            "console": "integratedTerminal"
        }
    ]
}

```

