if [[ $1 = "flush" ]];
then
    rm -rf out/dig/* out/httpx/* out/nmap/* out/nuclei/* out/subfinder/*;
    touch out/dig/.gitkeep out/httpx/.gitkeep out/nmap/.gitkeep out/nuclei/.gitkeep out/subfinder/.gitkeep;
    echo "" > tool.log;
    echo "Cleared logs and progress"
else
    ./venv/bin/python3 ./index.py "$@";
fi
