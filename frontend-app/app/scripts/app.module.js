(function() {
    angular
        .module('pytwilioApp', [
            'ngAnimate',
            'app.routes',
            'mainCtrl',
            'smsCtrl',
            'callCtrl',
        ])
        .constant("CONFIG", {
            "BASE": "http://localhost:5000",
            "BASE_API": "http://localhost:5000/api"
        });
})();