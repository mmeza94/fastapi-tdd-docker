import json

from app.api import summaries


# Mocking del comportamiento de la librería newspaper3k para evitar solicitudes reales
def mock_download(self):
    # Simulamos que la descarga fue exitosa y que hay un artículo con un resumen
    self.is_downloaded = True
    self.summary = "Resumen simulado"
    return self


# Prueba para crear un resumen
def test_create_summary(test_app_with_db, monkeypatch):
    def mock_generate_summary(summary_id, url):
        return None

    # Usamos monkeypatch para sustituir la función
    monkeypatch.setattr(summaries, "generate_summary", mock_generate_summary)

    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )

    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar/"


# Prueba para crear un resumen con datos JSON inválidos
def test_create_summaries_invalid_json(test_app):
    response = test_app.post("/summaries/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "url"],
                "msg": "Field required",
                "input": {},
                "url": "https://errors.pydantic.dev/2.10/v/missing",
            }
        ]
    }


# Prueba para leer un resumen
def test_read_summary(test_app_with_db, monkeypatch):
    # Mocking para la función generate_summary si es necesario
    def mock_generate_summary(summary_id, url):
        return {"summary": "Resumen simulado"}

    monkeypatch.setattr(summaries, "generate_summary", mock_generate_summary)

    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.get(f"/summaries/{summary_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar/"
    # assert response_dict["summary"] == "Resumen simulado"
    assert response_dict["created_at"]


# Prueba para leer todos los resúmenes
def test_read_all_summaries(test_app_with_db, monkeypatch):
    def mock_generate_summary(summary_id, url):
        return {"summary": "Resumen simulado"}

    monkeypatch.setattr(summaries, "generate_summary", mock_generate_summary)

    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.get("/summaries/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == summary_id, response_list))) == 1


# # Prueba para eliminar un resumen
# def test_remove_summary(test_app_with_db):
#     response = test_app_with_db.post(
#         "/summaries/", data=json.dumps({"url": "https://foo.bar"})
#     )
#     summary_id = response.json()["id"]

#     response = test_app_with_db.delete(f"/summaries/{summary_id}/")
#     assert response.status_code == 200
#     assert response.json() == {"id": summary_id, "url": "https://foo.bar/"}


# Prueba para eliminar un resumen con ID incorrecto
def test_remove_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"

    response = test_app_with_db.delete("/summaries/0/")
    assert response.status_code == 422
    # assert response.json() == {
    #     "detail": [
    #         {
    #             "ctx": {"gt": 0},
    #             "input": "0",
    #             "loc": ["path", "id"],
    #             "msg": "Input should be greater than 0",
    #             "type": "greater_than",
    #             "url": "https://errors.pydantic.dev/2.5/v/greater_than",
    #         }
    #     ]
    # }


# Pruebas de actualización de resumen
def test_update_summary(test_app_with_db, monkeypatch):
    def mock_generate_summary(summary_id, url):
        return {"summary": "Resumen actualizado"}

    monkeypatch.setattr(summaries, "generate_summary", mock_generate_summary)

    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/summaries/{summary_id}/",
        data=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar/"
    assert response_dict["summary"] == "updated!"
    assert response_dict["created_at"]


# Prueba para actualizar un resumen con un ID incorrecto
def test_update_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.put(
        "/summaries/999/",
        data=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


# Prueba para actualizar un resumen con datos JSON inválidos
# def test_update_summary_invalid_json(test_app_with_db, monkeypatch):
#     # Mockeamos la función download de newspaper3k
#     with patch("newspaper.article.Article.download", mock_download):
#         response = test_app_with_db.post(
#             "/summaries/", data=json.dumps({"url": "https://foo.bar"})
#         )
#         summary_id = response.json()["id"]

#         response = test_app_with_db.put(f"/summaries/{summary_id}/", data=json.dumps({}))
#         assert response.status_code == 422
# assert response.json() == {
#     "detail": [
#         {
#             "input": {},
#             "loc": ["body", "url"],
#             "msg": "Field required",
#             "type": "missing",
#             "url": "https://errors.pydantic.dev/2.5/v/missing",
#         },
#         {
#             "input": {},
#             "loc": ["body", "summary"],
#             "msg": "Field required",
#             "type": "missing",
#             "url": "https://errors.pydantic.dev/2.5/v/missing",
#         }
#     ]
# }


# # Prueba para actualizar un resumen con claves inválidas
# def test_update_summary_invalid_keys(test_app_with_db, monkeypatch):
#     # Mockeamos la función download de newspaper3k
#     with patch("newspaper.article.Article.download", mock_download):
#         response = test_app_with_db.post(
#             "/summaries/", data=json.dumps({"url": "https://foo.bar"})
#         )
#         summary_id = response.json()["id"]

#         response = test_app_with_db.put(
#             f"/summaries/{summary_id}/", data=json.dumps({"url": "https://foo.bar"})
#         )
#         assert response.status_code == 422
#         # assert response.json() == {
#         #     "detail": [
#         #         {
#         #             "input": {"url": "https://foo.bar"},
#         #             "loc": ["body", "summary"],
#         #             "msg": "Field required",
#         #             "type": "missing",
#         #             "url": "https://errors.pydantic.dev/2.5/v/missing",
#         #         }
#         #     ]
#         # }


# # Prueba para crear un resumen
# def test_create_summary(test_app_with_db, monkeypatch):
#     def mock_generate_summary(summary_id, url):
#         return None

#     monkeypatch.setattr(summaries, "generate_summary", mock_generate_summary)

#     response = test_app_with_db.post(
#         "/summaries/", data=json.dumps({"url": "https://foo.bar"})
#     )

#     assert response.status_code == 201
#     assert response.json()["url"] == "https://foo.bar/"
