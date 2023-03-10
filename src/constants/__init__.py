# page urls
LOGIN_PAGE_URL = 'https://ucampus.knou.ac.kr/ekp/user/login/retrieveULOLogin.do'
STUDY_PAGE_URL = 'https://ucampus.knou.ac.kr/ekp/user/study/retrieveUMYStudy.sdo'

# play percentage
VIDEO_ELAPSE_PERCENT = 60

# query selectors
SELECTORS = {
    'LECTURE': {
        'ROOT': 'div.lecture-progress-item.inactive',
        'TITLE': '.lecture-title',
        'MORE': 'a#btn-toggle-@',
        'BODY': '.lecture-progress-item-body',
        'VIDEO': {
            'ROOT': 'ul.lecture-list > li',
            'TITLE': '.lecture-title',
            'WATCHED': 'a.ch',
            'SHOW_VIDEO': 'a.btn.lecture-view',
            'WAITING': 'span.con-waiting',
        },
    },
    'PLAYER': {
        'ROOT': 'ifrmVODPlayer_0',
        'PLAY': '.jw-icon-display2',
        'WATCH_CONTINUE': '#wp_elearning_seek',
        'ELAPSED': 'span.jw-text-elapsed',
        'TOTAL_DURATION': 'span.jw-text-duration',
        'END_STUDY': 'button.studyend',
    },
}

LOADING_SYMBOLS = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
