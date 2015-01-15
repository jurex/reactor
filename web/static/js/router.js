App.Router = Backbone.Router.extend({
  routes: {
    "": "Dashboard",
    "/dashboard": "Dashboard",
    "console": "Console",
    "*actions": "Default"
  },
  Default: function (actions) {
    // no route match
  },
  Dashboard: function () {
    /*
    App.dashboard = new App.Dashboard();

    App.dashboard.fetch({success: function() {
      App.dashboardView = new App.DashboardView({model: App.dashboard});
      App.dashboardView.render();
    }}); 
    */
    console.log("prepairing dashboard view");

    App.consoleView = new App.ConsoleView();
  },
  Console: function () {
    App.console = new App.Console();
   
  }
});