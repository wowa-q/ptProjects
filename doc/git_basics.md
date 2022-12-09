https://www.youtube.com/watch?v=HVsySz-h9r4&t=4s


- `git remote -v` shows the remote repository 
- `git branch -a` shows the branches 
- `git branch --merged`  shows which branhces were merged into the actual branch
- `git log` shows all the commits on the current branch

# Configuration
- `git config --global user.name "woka"` sets the user 
- `git config -- global user.email "w.kloos@gmx.de"` sets the user email, used for accessing repository
- `git config --list`: shows the configuration

# Setup git repository
## local code base to start tracking in git
1. go to the folder where the project is located and
2. `git init` makes git repository from the folder
3. `git status` to show untracked files in the folder 
4. create `.gitignore` file (test file)
5. rerun `git status` to check if unwanted files are ignored
6. `git add .` or `git add -A` to add all files to stage 
    - `git add file.extension` to add one file to stage
7. `git reset` to remove all files from stage or `git reset file.extension` to remove one file from the stage 
8. `git commit -m "message"` to commit the files from the stage are to repository

## clone repository from remote repository
1. `git clone <url> <where to clone>`
    - `.` to clone to current directory
2. `git remote -v` lists information about the repository
3. `git branch -a` shows all the branches including branches on remote repository
4. after chenges on the code `git diff` to show the changes, which were done