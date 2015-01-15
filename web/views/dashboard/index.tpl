{% extends "layout.tpl" %}
{% block content %}

<div id="dashboard">

  <!-- Main jumbotron for a primary marketing message or call to action -->
  <div class="jumbotron">
    <div class="container">
      <h1>Dashboard <i class="fa fa-angellist"></i></h1>
      <p>This is a template for a simple marketing or informational website. It includes a large callout called a jumbotron and three supporting pieces of content. Use it as a starting point to create something more unique.</p>
      <p><a class="btn btn-primary btn-lg" role="button">Learn more &raquo; </a></p>
    </div>
  </div>

</div>
<div id="console">
  <div class="container">
    <div class="controls">
      <div class="input-group">
        <input type="text" class="form-control" placeholder="JSON encoded event">
        <span class="input-group-btn">
          <button class="btn btn-default ui-send" type="button">Send</button>
        </span>
      </div>
    </div>
    <div class="events">
    </div>
  </div>
</div>
{% endblock %}