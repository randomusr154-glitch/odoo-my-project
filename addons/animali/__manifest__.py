{
    'name': 'Gestione Animali e Proprietari',  
    'version': '18.0.1.0.0',                    
    'category': 'Sales/CRM',                   
    'summary': 'Un modulo per gestire animali e proprietari', 
    'description': """
        Gestione Animali
        ================
        Questo modulo permette di:
        - Gestire l'anagrafica dei proprietari.
        - Gestire l'anagrafica degli animali associati.
    """,                                      
    'author': 'Zerouno',          
    'website': 'https://www.zerouno.it/',     
    'license': 'LGPL-3',                       
    'depends': ['base', 'portal'],                        
    'data': [
        'security/ir.model.access.csv',
        'views/owners_views.xml',
        'views/animals_views.xml',
        'views/config_views.xml',
        'views/animals_portal.xml',
        'views/animal_report.xml',
        'views/menus.xml',
    ],
    'images': ['static/description/icon.png'],  
    'installable': True,
    'application': True,                        
    'auto_install': False,
}