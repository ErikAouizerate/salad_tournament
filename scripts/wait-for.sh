#!/bin/bash
# wait-for.sh - Wait for a service to be available
# Usage: ./wait-for.sh host:port [-t timeout] [-- command args]

cmdname=$(basename $0)
timeout=15
quiet=0

# Process arguments
while [[ $# -gt 0 ]]
do
    case "$1" in
        *:* )
        hostport=(${1//:/ })
        host=${hostport[0]}
        port=${hostport[1]}
        shift 1
        ;;
        -q | --quiet)
        quiet=1
        shift 1
        ;;
        -t | --timeout)
        timeout="$2"
        if [[ $timeout == "" ]]; then break; fi
        shift 2
        ;;
        --timeout=*)
        timeout="${1#*=}"
        shift 1
        ;;
        --)
        shift
        break
        ;;
        --help)
        echo "Usage: $cmdname host:port [-t timeout] [-- command args]"
        exit 0
        ;;
        *)
        echo "Unknown argument: $1"
        exit 1
        ;;
    esac
done

if [[ "$host" == "" || "$port" == "" ]]; then
    echo "Error: you need to provide a host and port to test."
    exit 1
fi

# Function to wait for a connection
wait_for() {
    if [[ $quiet -eq 0 ]]; then
        echo "Waiting for $host:$port..."
    fi
    
    for i in `seq $timeout` ; do
        nc -z "$host" "$port" > /dev/null 2>&1
        
        result=$?
        if [[ $result -eq 0 ]]; then
            if [[ $quiet -eq 0 ]]; then
                echo "$host:$port is available after $i seconds"
            fi
            return 0
        fi
        sleep 1
    done
    
    echo "Operation timed out" >&2
    exit 1
}

wait_for

# Execute the command if given
if [[ $# -gt 0 ]]; then
    exec "$@"
fi
