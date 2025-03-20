# use httpie periodically which should then stand out
http "localhost:8080"
# HTTPie user agent

curl "localhost:8080"
# curl user agent

# browser to 
open "http://localhost:8080/en/download.html"
# download page w/ missing links b/c I don't have previous builds available on my static site => errors
open "http://localhost:8080/en/books.html"
# lots of jpg images

# malicious:
open "http://localhost:8080/.htpasswd"

# scraper:
curl -A "Mozilla/5.0 (compatible; BadScraper/1.0; +http://badbot.com/bot.html)" "http://localhost:8080/"

# XSS
open http "http://localhost:8080/search?q=<script>alert('you forgot to checkout, put your address down below and hit submit');</script>"

# curl complained about this, needs to encode it:
curl "http://localhost:8080/search?q=<script>alert('you forgot to checkout, put your address down below and hit submit');</script>"

# SQL INJECTION
curl "http://localhost:8080/search?q=%27%20UNION%20SELECT%20null,null%2D%2D"

# browse innocently w/ httpie to get changelogs which would be reasonable to view at CLI
curl "localhost:8080/en/download.html"
curl "localhost:8080/en/CHANGES-1.24"
curl "localhost:8080/en/CHANGES-1.25" # does not exist
curl "localhost:8080/en/CHANGES-1.26"
