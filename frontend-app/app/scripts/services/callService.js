(function() {
    angular
        .module('callService', [])
        .factory('Call', ['CONFIG', '$http', function (CONFIG, $http) {

        	var callFactory = {};

        	/**
        	 * Send Call
        	 */
        	callFactory.call = function(data) {
        		return $http.post(CONFIG.BASE_API + '/call', data);
        	}

        	return callFactory;
        }]);
})();