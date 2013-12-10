#!/bin/sh

if [ -e stop.sh ]; then
    ./stop.sh
fi

# start program
python main.py &
APP_PID=$!

echo "#!/bin/sh" > stop.sh
echo kill $APP_PID >> stop.sh
echo rm stop.sh >> stop.sh
chmod a+x stop.sh
