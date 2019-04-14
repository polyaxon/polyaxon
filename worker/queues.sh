if [ $? -eq 0 ]; then
    if [ -z "$2" ]; then
        echo "$(< "$1")"
    else
        echo "$2"
    fi
fi
