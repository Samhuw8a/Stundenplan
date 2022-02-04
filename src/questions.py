from PyInquirer import Separator
weekdays=("Mo","Di","Mi","Do","Fr","Sa","So")
def is_valid_time(time:str)->bool:
    try:
        int(time.split(":")[0])
        int(time.split(":")[1])
        return True
    except:
        pass
    return False

delete_lec=[ {
        'type'    : 'list',
        'name'    : 'tag',
        'message' : 'Welcher Wochentag willst du wählen',
        'choices' : weekdays
    }, {
        'type'    : 'input',
        'name'    : 'start',
        'message' : 'Startzeit deiner Lektion',
        'validate': is_valid_time
    }]

create_lec = [ {
        'type'    : 'list',
        'name'    : 'tag',
        'message' : 'Welcher Wochentag willst du wählen',
        'choices' : weekdays
    }, {
        'type'    : 'input',
        'name'    : 'zimmer',
        'message' : 'Zimmer'
    }, {
        'type'    : 'input',
        'name'    : 'fach',
        'message' : 'Fach',
        'validate': lambda x: x.isalpha()
    }, {
        'type'    : 'input',
        'name'    : 'lek',
        'message' : 'Anzahl Lektionen',
        'validate': lambda x: str(x).isdigit()
    }, {
        'type'    : 'input',
        'name'    : 'start',
        'message' : 'Start der Lektion',
        'validate': is_valid_time
    }, {
        'type'    : 'input',
        'name'    : 'ende',
        'message' : 'Ende der Lektion',
        'validate': is_valid_time
    }]

edit_input=[ {
        'type'    : 'list',
        'name'    : 'tag',
        'message' : 'Welcher Wochentag willst du wählen',
        'choices' : weekdays
    }, {
        'type'    : 'input',
        'name'    : 'start',
        'message' : 'Startzeit deiner Lektion',
        'validate': is_valid_time
    },
    {
        'type': 'list',
        'name': 'cmd',
        'message': 'was willst du bearbeiten',
        'choices':["Zimmer","Fach","Anzahl_Lek","Ende","Start"]
    }]

add_temps=[ {
        'type': 'list',
        'name': 'tag',
        'message' : 'An welchen Wochentag ist die Zu verschiebende Lektion',
        'choices' : weekdays
    },
    {
        'type'    : 'input',
        'name'    : 'start',
        'message' : 'Start der Lektion',
        'validate': is_valid_time
    },
    {
        'type': 'list',
        'name': 'n_tag',
        'message' : 'Verschiebungstag',
        'choices' : weekdays
    },
    {
        'type'    : 'input',
        'name'    : 'n_start',
        'message' : 'Start der verschobenen Lektion',
        'validate': is_valid_time
    }]

delete_temps=[ {
        'type': 'list',
        'name': 'tag',
        'message' : 'Tag der verschobenen Lektion',
        'choices' : weekdays
    },
    {
        'type'    : 'input',
        'name'    : 'start',
        'message' : 'Start der verschobenen Lektion',
        'validate': is_valid_time
    }]

Zimmer = [{ 'type': 'input', 'name': 'cmd', 'message': 'Zimmer' }]
Fach = { 'type': 'input', 'name': 'cmd', 'message': 'Fach', 'validate': lambda x: x.isalpha() }
Anzahl_Lek = [{ 'type': 'input', 'name': 'cmd', 'message': 'Anzahl_Lek', 'validate': lambda x: str(x).isdigit() }]
Ende = [{ 'type': 'input', 'name': 'cmd', 'message': 'Ende', 'validate': is_valid_time }]
Start= [{ 'type': 'input', 'name': 'cmd', 'message': 'Start', 'validate': is_valid_time }]

UI_qs = [{
    'type'    : 'list',
    'name'    : 'cmd',
    'message' : 'Was willst du machen',
    'choices' : ['list','day','now',Separator("==>-<=="),'add','del','ed',Separator("==>-<=="),'temp']
    } ]

Temp_qs=[ {
        'type'    : 'list',
        'name'    : 'cmd',
        'message' : 'Was willst du machen',
        'choices' : ['list','add', 'rem','reactivate','clear']
}]

Day_qs = [ {
        'type'    : 'list' ,
        'name'    : 'day',
        'message' : 'welcher Tag willst du',
        'choices' : [ "Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
} ]
