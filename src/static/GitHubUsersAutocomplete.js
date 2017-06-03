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
	self.loading = false;

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
		self.loading = true;
		$http.get("api/rankuser?username=" + self.searchText)
		.then(function(response){
			var item = response.data;
			self.showUser(item);
			self.loading = false;
		}, function(response){
			self.loading = false;
			var error = response.data ? response.data : "Error. Is the server sleeping?";
			$mdToast.show(
				$mdToast.simple()
				.textContent(error)
				.toastClass('md-toast-error')
			);
		});
		event.preventDefault();
	}

	self.showUser = function(item){
		self.resultUsers.push(item);
	};
	self.removeUser = function(item){
		self.resultUsers.splice(self.resultUsers.indexOf(item), 1);
	};
});
