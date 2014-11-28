# -*- coding: utf-8 -*-

'''
this two dicts allows to iterate easily over models and UserData attrs,
using globals(), setattr(), getattr()
see in staff_manager.source_functions
'''

perms_to_language = {'event_worker' : 'Управляющий событиями',
					'teacher' : 'Учитель',
					'mentor' : 'Воспитатель',
					'observer' : 'Наблюдатель',
					'regular' : 'Ученик'
					}

perms_to_classes = {'event_worker' : 'EventWorker',
					'teacher' : 'Teacher',
					'mentor' : 'Mentor',
					'observer' : 'Observer',
					'regular' : 'RegularUser'
					}