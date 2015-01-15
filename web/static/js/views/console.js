App.ConsoleView = Backbone.View.extend({
  el: '#console',
  initialize: function() {
    this.$events = this.$el.find("#events");
    this.render();

    App.eventbus.on('event', function(event){
      this.$events.append('<div class="event">'+ event + '</div>');
    });
  },
  events: {
    'click ui-send': 'onSend'
  },
  render: function(){
    var that = this;


    this.$events.append('<div class="event">Console Ready</div>');
    
    return this;
  },
  onSubmit: function() {

  console.log("submitting new event");

  }
});
