compile:
    npm run compile

build:
    npx vsce package

install:
    code --install-extension mpy-studio-1.0.0.vsix

push_typings:
    cd typings
    git add .
    git commit -m "fixed bugs."
    git push origin main

pull_typings:
    cd typings
    git pull origin main