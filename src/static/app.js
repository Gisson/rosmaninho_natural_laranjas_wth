var app = angular.module('app', ['ngMaterial', 'ngMessages', 'ngAnimate']);

app.config(function($mdThemingProvider) {
	$mdThemingProvider.theme('default')
	.primaryPalette('blue')
	.accentPalette('green')
	.dark();
});

app.config(function ($httpProvider) {
	$httpProvider.defaults.transformRequest = function(data){
		return data;
	}
});

app.controller('rank', function($scope, $http) {
	$http.get("api/rankuser")
	.then(function(response) {
		$scope.build_time = response.data;
	});
});


