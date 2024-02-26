{
    'name': 'Real estate',
    'author':'Prashanna',
    'sequence': -1,
    'website': 'https://www.realestate.tech',
    'summary': 'realestate development',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_inherit.xml',
        'views/client_action.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'estate/static/src/**/*.js',
            'estate/static/src/**/*.xml',
            'estate/static/src/**/*.scss',
        ]
    },
    'demo':[],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}