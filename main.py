from transformers import AutoTokenizer, AutoModelForCausalLM
import http.server
import socketserver
import json

# Set up the model
tokenizer = AutoTokenizer.from_pretrained('gpt2')
model = AutoModelForCausalLM.from_pretrained('gpt2')

# Function to generate the response and return text embedding
def generateResponseAndEmbedding(text):
  # Encode the input text to then feed to the model
  input_ids = tokenizer.encode(text, add_special_tokens=True, return_tensors="pt")
  output = model.generate(input_ids, max_length=200, num_return_sequences=1)
  generated_response = tokenizer.decode(output[0], skip_special_tokens=True)

  # Get the sentence embedding
  vector = model.transformer.wte.weight[input_ids,:]

  return generated_response, vector

# Handle saving an embedding to the database for later
def saveEmbeddingToDatabase(embedding):
    print("Saving embedding to db...")


# Handle incoming requests
class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle returning the single webpage
        if self.path == "/" or self.path == "/index.html":
            self.path = "/index.html"
            try:
                with open(self.path[1:], "rb") as file:
                    content = file.read()
                    self.send_response(200)
                    if self.path.endswith(".html"):
                        self.send_header("Content-type", "text/html")
                    elif self.path.endswith(".css"):
                        self.send_header("Content-type", "text/css")
                    elif self.path.endswith(".js"):
                        self.send_header("Content-type", "application/javascript")
                    self.end_headers()
                    self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"File not found")

    def do_POST(self):
        # Handle generating a response when a prompt is sent
        if self.path == "/generate":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")

            # Get the promt, generate what we need, save generated response to the database
            post_data_json = json.loads(post_data)
            prompt = post_data_json["prompt"]
            response, vector = generateResponseAndEmbedding(prompt)
            saveEmbeddingToDatabase(vector)

            # Create our response object
            response_obj = {"generated_response": response}
            response_json = json.dumps(response_obj)

            # Send the response
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response_json.encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Page not found.")

# Handle starting a simple server
PORT = 8000
with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
