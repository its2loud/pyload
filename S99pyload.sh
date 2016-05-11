#!/bin/sh
COMMAND="/volume1/@appstore/pyload/bin/python /volume1/@appstore/pyload/pyload/pyLoadCore.py"

start() {
        echo "Starting PyLoad"
        $COMMAND --daemon
}

status() {
        echo -n "Status of PyLoad: "
        STATUS=$($COMMAND --status)
        if [[ $STATUS = "False" ]]; then
                echo "Not running"
        else
                echo "Running as PID $STATUS"
        fi
}

stop() {
        echo "Stopping PyLoad"
        $COMMAND --quit
}

case "$1" in
        start)
                start
                ;;
        stop)
                stop
                ;;
        restart)
                stop
                sleep 4
                start
                ;;
        status)
                status
                ;;
        *)
                echo "Usage: $0 (start|stop|restart|status)"
                exit 1
                ;;
esac
exit 0