$(document).ready(function() {
  'use strict';

  // set env
  //App.user = Env.user;

  App.eventbus = io.connect('/test'); 
  
  // init router
  App.router = new App.Router;
  Backbone.history.start({pushState: true});
  
});