{% extends "layout.tpl" %}
{% block content %}
  <form action="" method="post" class="form-horizontal">
    {{ form.hidden_tag() }}
    <h2>Signin </h2>

    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul class=flashes>
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}

    <div class="control-group">
        <div class="controls">
          <input type="text" id="username" name="username" class="input-xlarge"
            placeholder="Enter Username" required>
        </div>
    </div>
 
    <div class="control-group">
        <div class="controls">
          <input type="password" id="password" name="password" class="input-xlarge"
            placeholder="Enter Password" required>
        </div>
    </div>
 
    <div class="control-group">
        <div class="controls">
          <button type="submit" class="btn btn-success">Signin</button>
        </div>
    </div>
  </form>
{% endblock %}