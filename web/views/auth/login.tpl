{% extends "layout.tpl" %}
{% block content %}
  <div class="container">

      <form class="form-signin" method="post" role="form">
        {{ form.hidden_tag() }}
        <h2 class="form-signin-heading">Log in</h2>

        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}
              <div class="alert alert-danger" role="alert">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <input id="username" name="username" type="text" class="form-control" placeholder="Username" required autofocus>
        <input id="password" name="password" type="password" class="form-control" placeholder="Password" required>
        <div class="checkbox">
          <label>
            <input type="checkbox" value="remember-me"> Remember me
          </label>
        </div>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Log in</button>
      </form>

    </div> <!-- /container -->
{% endblock %}