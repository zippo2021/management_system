# -*- coding: utf-8 -*-

'''
this two dicts allows to iterate easily over models and UserData attrs,
using globals(), setattr(), getattr()
see in staff_manager.source_functions
'''

permissions_names = ('event_worker', 'teacher', 'mentor', 'observer')

perms_to_classes = {'event_worker' : 'EventWorker',
					'teacher' : 'Teacher',
					'mentor' : 'Mentor',
					'observer' : 'Observer'
					}

