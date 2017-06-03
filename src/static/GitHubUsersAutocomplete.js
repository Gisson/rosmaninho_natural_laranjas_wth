/**
 * Controller to Autocomplete GitHub Usernames
 * */

app.controller('GitHubUsersAutocomplete', function ($http, $timeout, $q, $log, $mdToast) {
	var self = this;
	self.isDisabled = false;
	self.noCache = false;
	self.delay = 250;

	self.itens = [];
	self.querySearch = querySearch;
	self.searchText = "";

	function querySearch (query) {
		var results = query ? self.itens.filter( createFilterFor(query) ) : self.itens, deferred;

		deferred = $q.defer();
		$http.get("https://api.github.com/search/users?q=" + query)
		.then(function(response) {
			deferred.resolve(response.data.items);
		}, function(response){
			deferred.reject(response.data);
			$mdToast.show(
				$mdToast.simple()
				.textContent(response.data.message)
				.toastClass('md-toast-error')
			);
		});

		return deferred.promise;
	}

	function createFilterFor(query) {
		var lowercaseQuery = angular.lowercase(query);

		return function filterFn(item) {
			return (item.value.indexOf(lowercaseQuery) === 0);
		};

	}

	self.submit = function (event){
		$http.get("api/rankuser?username=" + self.searchText)
		.then(function(response){
			self.data = response.data;
		}, function(response){
			$mdToast.show(
				$mdToast.simple()
				.textContent(response.data)
				.toastClass('md-toast-error')
			);
		});
		event.preventDefault();
	}

	self.data = "";
});
