#!/usr/bin/env sh

MSG=" ********** iniciando container do python jupyter "
echo MSG

pip install -r /requirements.txt
pip3 install debugpy -t /tmp
# python /tmp/debugpy --listen 0.0.0.0:3001 --wait-for-client /app/main.py


jupyter notebook --autoreload --notebook-dir='/app'   --port=8008 --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token='55823d0ba2d38a542305271c1fb68bfccdef227680059b62' 

# date=$(stat -c %y /app/main.py)
while sleep 1; do
  date2=$(stat -c %y /app/main.py)

  # if [[ $date2 != $date ]]; then
  #   python /tmp/debugpy --listen 0.0.0.0:3001 --wait-for-client /app/main.py
  #   date=$(stat -c %y /app/main.py)
  # fi
done
