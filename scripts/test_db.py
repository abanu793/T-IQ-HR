from db_utils import insert_resume, insert_prediction

rid = insert_resume("test_resume.pdf", "C:/dummy/test_resume.pdf")
insert_prediction(rid, 0.91, "fake")

print("DB insert successful")
