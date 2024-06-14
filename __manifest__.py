{
    'name': 'School Management',
    'version': '1.0',
    'category': 'Uncategorized',
    'license': 'LGPL-3',
    'author': 'Your Name',
    'website': 'https://www.itscholarbd.com',
    'data': [
        # 'data/demo.xml',
        'data/class.xml',
        'data/section.xml',
        'data/subject.xml',
        'security/user_group.xml',
        'views/student_view.xml',
        'views/menu.xml',
        'security/ir.model.access.csv',

    ],
    'assets': {
        'web.assets_backend': [
            'school_management/static/src/css/custom.scss',
            'school_management/static/src/js/calendar_popup.js',

            'school_management/static/src/components/*/*.js',
            'school_management/static/src/components/*/*.xml',
            'school_management/static/src/components/*/*.scss',
        ],
        'web.assets_frontend': [
            'https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,400i,700&display=fallback',
            'school_management/static/adminLTE-3.2.0/plugins/fontawesome-free/css/all.min.css',
            'https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css',
            'school_management/static/adminLTE-3.2.0/plugins/tempusdominus-bootstrap-4/css/tempusdominus-bootstrap-4.min.css',
            'school_management/static/adminLTE-3.2.0/plugins/icheck-bootstrap/icheck-bootstrap.min.css',
            'school_management/static/adminLTE-3.2.0/plugins/jqvmap/jqvmap.min.css',
            'school_management/static/adminLTE-3.2.0/dist/css/adminlte.min.css',
            'school_management/static/adminLTE-3.2.0/plugins/overlayScrollbars/css/OverlayScrollbars.min.css',
            'school_management/static/adminLTE-3.2.0/plugins/daterangepicker/daterangepicker.css',
            'school_management/static/adminLTE-3.2.0/plugins/summernote/summernote-bs4.min.css',

            # 'school_management/static/adminLTE-3.2.0/plugins/jquery/jquery.min.js',
            # 'school_management/static/adminLTE-3.2.0/plugins/jquery-ui/jquery-ui.min.js',
            # 'school_management/static/adminLTE-3.2.0/plugins/bootstrap/js/bootstrap.bundle.min.js',
            # 'school_management/static/adminLTE-3.2.0/plugins/chart.js/Chart.min.js',
            # 'school_management/static/adminLTE-3.2.0/plugins/sparklines/sparkline.js',
            # 'school_management/static/adminLTE-3.2.0/plugins/jqvmap/jquery.vmap.min.js',
            # 'school_management/static/adminLTE-3.2.0/plugins/jqvmap/maps/jquery.vmap.usa.js',
            # 'school_management/static/adminLTE-3.2.0/plugins/jquery-knob/jquery.knob.min.js',
            # 'school_management/static/adminLTE-3.2.0/plugins/moment/moment.min.js',
            'school_management/static/adminLTE-3.2.0/plugins/daterangepicker/daterangepicker.js',
            # 'school_management/static/adminLTE-3.2.0/plugins/tempusdominus-bootstrap-4/js/tempusdominus-bootstrap-4.min.js',
            'school_management/static/adminLTE-3.2.0/plugins/summernote/summernote-bs4.min.js',
            'school_management/static/adminLTE-3.2.0/plugins/overlayScrollbars/js/jquery.overlayScrollbars.min.js',
            'school_management/static/adminLTE-3.2.0/dist/js/adminlte.js',
            'school_management/static/adminLTE-3.2.0/dist/js/demo.js',
            'school_management/static/adminLTE-3.2.0/dist/js/pages/dashboard.js',
            'school_management/static/adminLTE-3.2.0/custom-js/custom.js',
            'school_management/static/adminLTE-3.2.0/custom-css/custom.scss'
        ]
    }
}
