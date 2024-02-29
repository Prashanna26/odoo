{
    'name': 'Owl Practise',
    'author':'Prashanna',
    'sequence': -1,
    'website': 'https://www.todolist.tech',
    'summary': 'Owl development',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/owlpractise_view.xml',
    ],
    'assets':{
        'web.assets_backend': [
            'owlpractise/static/src/**/*.js',
            'owlpractise/static/src/**/*.xml',
            'owlpractise/static/src/**/*.scss',
        ]
    },
    'demo':[],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}