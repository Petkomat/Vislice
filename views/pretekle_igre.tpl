<!DOCTYPE html>
<html>

<body>

  <h1>Seznam že končanih iger:</h1>

  <ul>
  % for id_igre in koncane_igre:
    <li><a href="http://127.0.0.1:8080/igra/{{id_igre}}">{{id_igre}}</a></li>
  % end
</ul>

  <form action="/" method="get">
    <button type="submit">DOMOV</button>
  </form>
</body>

</html>