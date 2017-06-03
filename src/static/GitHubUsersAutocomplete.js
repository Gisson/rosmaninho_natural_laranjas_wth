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
	self.filters = [];
	self.selectedLanguages = [];

	function querySearch (query) {
		var results = query ? self.items.filter( createFilterFor(query) ) : self.items, deferred;

		deferred = $q.defer();
		$http.get("https://api.github.com/search/users?q=" + query)
		.then(function(response) {
			deferred.resolve(response.data.items);
			self.items = response.data.items;
		}, function(response){
			var error = response.data.message ? response.data.message : "No message. Maybe the internet is sleepy";
			deferred.reject(response.data ? response.data : []);
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
			return (angular.lowercase(item.login).indexOf(lowercaseQuery) === 0);
		};

	}

	self.submit = function (event){
		self.loading = true;
		$http.post("api/rankuser?username=" + self.searchText,
		JSON.stringify({
			'filters' : self.filters,
			'languages' : self.selectedLanguages,
		}))
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


	self.transformLanguageChip = function(chip){
		return undefined; // simply add
	};
	self.searchLanguageText = "";
	self.selectedLanguage = "";

	self.languages = ["C", "C++", "Java", "JavaScript", "Python", "Bash", "HTML", "CSS", "PHP"];

	self.queryLanguage = function (query) {
		return query ? self.languages.filter( createSimpleFilterFor(query) ) : self.languages;
	}

	function createSimpleFilterFor(query) {
		var lowercaseQuery = angular.lowercase(query);
		return function filterFn(item) {
			return angular.lowercase(item).indexOf(lowercaseQuery) === 0;
		};
	}

	self.currentWeight = 1;

	self.transformFilterChip = function(chip){
		console.log("chip: " + chip);
		return {
			'filter'	: chip,
			'weight'	: self.currentWeight,
		};;
	};
});
