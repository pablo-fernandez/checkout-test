source env/bin/activate

export DEBUG="True"
export ROOT=`pwd`
export MANAGE="python $ROOT/manage.py"
export STATIC_URL="/static/"

alias m=$MANAGE