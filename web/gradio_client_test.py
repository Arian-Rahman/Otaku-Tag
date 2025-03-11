from gradio_client import Client

client = Client("soothsayer1221/Otaku-Tag")
result = client.predict(
		description="Naruto is a strong fighter!!",
		api_name="/predict"
)
print(result)