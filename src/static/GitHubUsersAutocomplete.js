/**
 * Controller to Autocomplete GitHub Usernames
 * */

app.controller('GitHubUsersAutocomplete', function ($http, $timeout, $q, $log, $mdToast) {
	var self = this;
	self.isDisabled = false;
	self.noCache = false;
	self.delay = 250;

	self.items = [];
	self.querySearch = querySearch;
	self.searchText = "";
	self.resultUsers = [];

	function querySearch (query) {
		var results = query ? self.items.filter( createFilterFor(query) ) : self.items, deferred;

		deferred = $q.defer();
		$http.get("https://api.github.com/search/users?q=" + query)
		.then(function(response) {
			deferred.resolve(response.data.items);
			self.items = response.data.items;
		}, function(response){
			deferred.reject(response.data);
			var error = response.data.message ? response.data.message : "No message. Maybe the internet is sleepy";
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
			return (item.login.indexOf(lowercaseQuery) === 0);
		};

	}

	self.submit = function (event){
		$http.get("api/rankuser?username=" + self.searchText)
		.then(function(response){
			var item = response.data;
			self.showUser(item);
		}, function(response){
			$mdToast.show(
				$mdToast.simple()
				.textContent(response.data)
				.toastClass('md-toast-error')
			);
		});
		event.preventDefault();
	}

	self.showUser = function(item){
		item.rank = new Date().getMilliseconds() % 100;
		self.resultUsers.push(item);
	};
	self.removeUser = function(item){
		self.resultUsers.splice(self.resultUsers.indexOf(item), 1);
	};
});
