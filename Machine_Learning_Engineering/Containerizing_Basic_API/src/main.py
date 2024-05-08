from fastapi import FastAPI


app = FastAPI()


@app.get("/health")
def read_health():
	return {"status": "healthy"}

@app.get("/hello")
def say_hello(name : str):
	if name:
		return {"message": f"Hello {name}"}




