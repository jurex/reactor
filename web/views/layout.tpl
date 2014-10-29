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

    {% block content %}{% endblock %}    
  </body>
  {% assets "app_js" %}
    <script type="text/javascript" src="{{ ASSET_URL }}"></script>
  {% endassets %}
</html>