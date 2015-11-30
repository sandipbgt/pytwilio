(function() {
    angular
        .module('callCtrl', [
            'mgcrea.ngStrap',
            'callService',
        ])
        .controller('callController', ['$rootScope', '$alert', 'Call', function($rootScope, $alert, Call) {
            var self = this;
            self.processing = false;
            self.callData = {};

            self.call = function() {
                self.processing = true;
                Call.call(self.callData)
                    .success(function(data) {
                        self.processing = false;
                        $alert({
                            content: 'Phone call created successfully!',
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