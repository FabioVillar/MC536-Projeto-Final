# Dados de terceiros usados como input nas funções

> Usamos apenas Webscraping para aquisição dos dados, logo, as fontes de terceiros são apenas baseadas em links dos dois sites que colhemos as informações: FBREF e Wikipedia

## FBREF

Para o FBREF, temos os seguintes links:

> Dados gerais das seleções nas copas antes de 2019:

~~~
https://fbref.com/en/comps/106/{page_id}/qual/{year}-Womens-World-Cup-Qualifying-Rounds


{page_id} = id da página correspondente (varia entre 1779 e 1786)
{year} = ano da copa (1991 à 2019)
~~~

> Dados das seleções na copa de 2019:

~~~
https://fbref.com/en/comps/106/qual/Womens-World-Cup-Qualifying-Rounds
https://fbref.com/en/comps/106/Womens-World-Cup-Stats
~~~

> Dados das jogadoras:

~~~
https://fbref.com/en/squads/{code}/{year}/{team_name}-Stats


{code} = code da página correspondente
{year} = ano da copa (1991 à 2019)
{team_name} = nome da seleção
~~~

> Dados das partidas das copas antes de 2019:

~~~
https://fbref.com/en/comps/106/{page_id}/schedule/{year}-Womens-World-Cup-Scores-and-Fixtures


{page_id} = id da página correspondente (varia entre 1779 e 1786)
{year} = ano da copa (1991 à 2019)
~~~

> Dados das partidas de 2019:

~~~
https://fbref.com/en/comps/106/schedule/Womens-World-Cup-Scores-and-Fixture


{page_id} = id da página correspondente (varia entre 1779 e 1786)
{year} = ano da copa (1991 à 2019)
~~~

## Wikipedia

Para a Wikipedia, temos:

> Dados das premiações:

~~~
https://en.wikipedia.org/wiki/FIFA_Women's_World_Cup_awards
~~~

> Dados de seleções e jogadoras:

~~~
https://en.wikipedia.org/wiki/{year}_FIFA_Women's_World_Cup
https://en.wikipedia.org/wiki/{year}_FIFA_Women's_World_Cup_squads

{year} = ano da copa (1991 à 2019)
~~~

