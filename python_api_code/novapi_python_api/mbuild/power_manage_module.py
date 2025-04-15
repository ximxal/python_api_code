
# Copyright (python), 2018-2019, MakeBlock
# file    power_manage_module.py
# @author  payton
# @version V1.0.0
# @date    2018/09/12
#
# `<Author>`         `<Time>`        `<Version>`        `<Descr>`
#  payton            2018/09/12     1.0.0            build the new.
#  payton            2018/10/11     1.0.1            not use neurons engine.
#  
# 
from makeblock import power_manage
from decorator import *

@decorator
def is_auto_mode():
    return power_manage.is_auto_mode()
