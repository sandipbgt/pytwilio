(function() {
    angular
        .module('smsService', [])
        .factory('SMS', ['CONFIG', '$http', function (CONFIG, $http) {

        	var smsFactory = {};

        	/**
        	 * Send SMS
        	 */
        	smsFactory.send = function(data) {
        		return $http.post(CONFIG.BASE_API + '/sms', data);
        	}

        	return smsFactory;
        }]);
})();