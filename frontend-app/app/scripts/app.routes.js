(function() {
    angular
        .module('app.routes', ['ui.router'])
        .config(['$stateProvider', '$urlRouterProvider',
            function($stateProvider, $urlRouterProvider) {
                $stateProvider
                    .state('home', {
                        url: '/',
                        templateUrl: 'views/home.html'
                    })
                    .state('sms', {
                        url: '/sms',
                        templateUrl: 'views/twilio/sms.html',
                        controller: 'smsController',
                        controllerAs: 'smsCtrl'
                    })
                    .state('call', {
                        url: '/call',
                        templateUrl: 'views/twilio/call.html',
                        controller: 'callController',
                        controllerAs: 'callCtrl'
                    });

                    $urlRouterProvider.otherwise('/');
            }
        ]);
})();