# Back-end Flask Restful API
## API Documentation
https://climatempo-talent.rj.r.appspot.com/
BackUp: https://climatempotalent.larsdehlwes.com.br/

## API Endpoints
### Autocomplete da Cidade
Method: GET

Endpoint: autocomplete_city

Parameters:
* user_input (required: True, String)

Example: https://climatempo-talent.rj.r.appspot.com/autocomplete_city?user_input=Osas

### Previsão do Tempo
Method: GET

Endpoint: weatherforecast

Parameters:
* city_id (required: True, Integer)
* unit_temperature (required: True, String, 'fahrenheit' ou 'celsius' ou 'F' ou 'C')
* unit_precipitation (required: True, String, 'inch' ou 'mm')

Example: https://climatempo-talent.rj.r.appspot.com/weatherforecast?city_id=3735&unit_temperature=fahrenheit&unit_precipitation=inch

## Deploy
### GCP
Crie um novo projeto e anote o identificador do projeto `<project-id>`. Em seguída, autentique-se and faça o deploy: 
```
gcloud app create --project=<project-id>
gcloud components install app-engine-python
gcloud app deploy --project=<project-id>
```

### No seu provedor de nuvem preferido ou em um servidor dedicado
Crie uma máquina virtual e utiliza o Dockerfile para realizar o deploy.

## To Do
- [x] Documentação da API (Swagger?) (completado em 21-08-2023)
- [x] Remover caratéres especiais no autocomplete (completado em 19-08-2023 17:52)
- [ ] Reincluir alguma forma de logging
- [x] Ativar server-side caching (completado em 21-08-2023)
- [x] Incluir testes automatizados (iniciado em 23-08-2023)
- [x] Dockerfile (completado em 03-09-2023)
