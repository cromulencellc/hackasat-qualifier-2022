#!/usr/bin/env python3

import angr

import os

chall_path = os.getenv('CHALL_PATH', '/mnt/challenge/build/ominous_etude')

proj = angr.Project(chall_path)
main_obj = proj.loader.main_object
main_func = main_obj.get_symbol('main')
main_func_start = main_func.rebased_addr
main_func_end = main_func_start + main_func.size
first_exit = 0x4012d9
second_exit = 0x401329

state = proj.factory.blank_state(addr=main_func_start)
sm = proj.factory.simulation_manager(state)
sm.explore(find=second_exit, avoid=first_exit)
