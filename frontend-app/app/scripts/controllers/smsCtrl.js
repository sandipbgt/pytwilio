(function() {
    angular
        .module('smsCtrl', [
            'mgcrea.ngStrap',
            'smsService',
        ])
        .controller('smsController', ['$rootScope', '$alert', 'SMS', function($rootScope, $alert, SMS) {
            var self = this;
            self.processing = false;
            self.smsData = {};

            self.send = function() {
                self.processing = true;
                SMS.send(self.smsData)
                    .success(function(data) {
                        self.processing = false;
                        $alert({
                            content: 'SMS sent successfully!',
                            placement: 'top-right',
                            animation: 'bounceIn',
                            type: 'success',
                            duration: 3
                        });
                    })
                    .error(function(data) {
                        self.processing = false;
                        $alert({
                              title: 'Error!',
                              content: data.message,
                              animation: 'bounceIn',
                              placement: 'top-right',
                              type: 'danger',
                              duration: 3
                            });
                    });
            };
        }]);
 })();