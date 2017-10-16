from lxml import html
import requests

DEALS_BODIES_URL = 'http://www.warmoth.com/Pages/ClassicShowcase.aspx?deals=true&Body=2&sort=price'
DEALS_NECKS_URL = 'http://www.warmoth.com/Pages/ClassicShowcase.aspx?deals=true&Body=1&sort=price'

def get_warmoth_deals(url):
  results = []
  headers = requests.utils.default_headers()
  headers.update(
      {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
      }
  )
  doc = html.fromstring(requests.get(url, headers = headers).text)
  table_rows = doc.xpath("//table[contains(@class,'showcaseTable')]//tr[contains(@class,'showcase-item-container')]")
  
  for row in table_rows:
    deal = get_deal(row)
    results.append(deal)
  return results


class WarmothDeal:
  def __init__(self, item_number):
    self.item_number = item_number
    self.name = ""
    self.price = 0
    self.specs = ""
  
  def __str__(self):
    return str(self.__dict__)
  
  def __repr__(self):
    return str(self.__dict__)

def get_item_number(row):
  item_number = row.xpath("./descendant::span[contains(@class,'itemNum')]/text()")
  return item_number

def get_item_name(row):
  item_name = row.xpath("./descendant::span[contains(@class,'itemName')]/text()")
  return item_name

def get_item_price(row):
  item_price = row.xpath("./descendant::div[contains(@class,'showcasePrice')]/span/text()")
  return item_price

def get_item_specs(row):
  item_specs = row.xpath("./descendant::span[contains(@class,'specs')]/text()")
  return item_specs

def get_deal(row):
  item_number = get_item_number(row)
  deal = WarmothDeal(item_number)
  deal.name = get_item_name(row)
  deal.price = get_item_price(row)
  deal.specs = get_item_specs(row)
  
  return deal


if __name__ == "__main__":
  body_deals = get_warmoth_deals(DEALS_BODIES_URL)
  neck_deals = get_warmoth_deals(DEALS_NECKS_URL)

  for deal in body_deals:
    print(deal)