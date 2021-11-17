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
https://en.wikipedia.org/wiki/2019_FIFA_Women's_World_Cup_squads
~~~

> Dados das jogadoras:

~~~
https://fbref.com/en/squads/{code}/{year}/{team_name}-Stats


{code} = code da página correspondente
{year} = ano da copa (1991 à 2019)
{team_name} = nome da seleção
~~~
