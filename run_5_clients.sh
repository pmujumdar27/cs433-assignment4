#!/bin/bash

python3 ./tcp_client_sc_thread.py 1 square_root_of_4.txt &
python3 ./tcp_client_sc_thread.py 1 checkmate.txt &
python3 ./tcp_client_sc_thread.py 1 pi.txt &
python3 ./tcp_client_sc_thread.py 1 shakespear.txt &
python3 ./tcp_client_sc_thread.py 1 war_and_peace.txt &