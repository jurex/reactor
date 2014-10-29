<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Reactor Automation</title>

    {% assets "app_css" %}
        <link rel="stylesheet" type="text/css" href="{{ ASSET_URL }}"></script>
    {% endassets %}


    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    {% if current_user.is_authenticated() %}
    <!-- Fixed navbar -->
    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#"><i class="fa fa-code"></i> Reactor</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="/">Dashboard</a></li>
            <li><a href="/devices">Devices</a></li>
            <li><a href="/events">Events</a></li>
            <li><a href="/about">About</a></li>
          </ul>
          <ul class="nav navbar-nav navbar-right">
            <li><a href="/profile" data-original-title="Profile"><i class="fa fa-user"></i></a></li>
            <li><a href="/logout" data-original-title="Logout"><i class="fa fa-sign-out"></i></a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>
    {% endif %}
    {% block content %}{% endblock %}    
  </body>
  {% assets "app_js" %}
    <script type="text/javascript" src="{{ ASSET_URL }}"></script>
  {% endassets %}
</html>