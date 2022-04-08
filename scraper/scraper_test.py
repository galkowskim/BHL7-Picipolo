from .scraper import getPrices


for page in range(1, 10):
    d = getPrices(page)
    print(page, d)
    
# while True:
#     d = getPrices(page)
#     if not d:
#         break