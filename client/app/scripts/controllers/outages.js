'use strict';

/**
 * @ngdoc function
 * @name dcmetrometricsApp.controller:OutagesCtrl
 * @description
 * # OutagesCtrl
 * Controller of the dcmetrometricsApp
 */
angular.module('dcmetrometricsApp')
  .controller('OutagesCtrl', ['$scope', '$uiViewScroll', '$location', '$state', 'directory', 'statusTableUtils', 

     function ($scope, $uiViewScroll, $location, $state, directory, statusTableUtils) {

      $scope.directory = directory;
      $scope.statusTableUtils = statusTableUtils;
      $scope.elevatorOutages = undefined;
      $scope.escalatorOutages = undefined;

      // Get the unit directory
      directory.get_directory().then( function(data) {

        var i, key, outage;

        // Sort the outages by station name and unit code.
        var sortFunc = function(unit1, unit2) {
          var s1 = directory.getStationName(unit1);
          var s2 = directory.getStationName(unit2);
          
          if (s1 < s2) {
            return -1;
          } else if (s2 < s1) {
            return 1;
          }

          // Station match, sort by code.
          if(s1.unit_id < s2.unit_id) {
            return -1;
          } else {
            return 1;
          }

        };

        $scope.data = data;
        $scope.escalatorOutages = data.escalatorOutages.sort(sortFunc);
        $scope.elevatorOutages = data.elevatorOutages.sort(sortFunc);
        $scope.unitIdToUnit = data.unitIdToUnit;

        // Count how many station outages there are.
        var stationDict = {};
        for(i = 0; i < data.escalatorOutages.length; i++) {
          outage = data.escalatorOutages[i];
          stationDict[outage.station_name] = 1;
        }
        for(i = 0; i < data.elevatorOutages.length; i++) {
          outage = data.elevatorOutages[i];
          stationDict[outage.station_name] = 1;
        }

        var stations_with_outage = [];
        for(key in stationDict) {
          if(stationDict.hasOwnProperty(key)) {
            stations_with_outage.push(key);
          }
        }

        console.log(stationDict);

        $scope.stations_with_outage = stations_with_outage;


        // Get recent statuses
        directory.get_recent_updates().then( function(data) {
          $scope.recentUpdates = data;
        });

      });




      // Figure out which tab is active from state

      $scope.escalatorTabActive = $state.is("outages.escalators");
      $scope.elevatorTabActive = $state.is("outages.elevators");


      $scope.getSymptomClass = function(unit) {

          var catToClass = {
            BROKEN : 'danger',
            INSPECTION : 'warning',
            OFF : 'danger',
            ON : 'success',
            REHAB : 'info'
          };

          var category = unit.key_statuses.lastStatus.symptom_category;
          return catToClass[category];

      };

      $scope.selectEscalatorTab = function() {
        console.log("selected escalator tab");
        $state.go("outages.escalators");
      };

      $scope.selectElevatorTab = function() {
        console.log("selected elevator tab");
        $state.go("outages.elevators");
      };

      $scope.showEscalators = function() {
        return $scope.$state.is("outages.escalators") ||
          $scope.$state.is("outages");
      };

      $scope.showElevators = function() {
        return $scope.$state.is("outages.elevators");
      };



     }]);

