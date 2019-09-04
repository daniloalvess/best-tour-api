# Best Tour API

API para encontrar o melhor trajeto, com base nas coordenadas informadas.

## Argumentos
- `visiting_time` - Se refere ao tempo de permanência em cada local. O valor deve ser uma fração de hora (Ex.: 0.25, 0.5, 0.75) ou até mesmo um número inteiro.

- `locations` - São as coordenadas (latitude, longitude) do local.

## Exemplo de requisição
```json
{
  "visiting_time": 0.5,
  "locations": [
    {
      "lat": -18.8785153,
      "lon": -41.9698963
    },
    {
      "lat": -18.510516,
      "lon": -41.866565
    },
    {
      "lat": -17.630215,
      "lon": -41.6182573
    },
    {
      "lat": -18.8917509,
      "lon": -41.9637153
    }
  ]
}
```
Para facilitar a identificação de cada coordenada, você pode adicionar o atributo `name`.
``` json
{
  "name": "Governador Valadares - Geral",
  "lat": -18.8785153,
  "lon": -41.9698963
},
```