from bs4 import BeautifulSoup


class Parser:

    def get_all_data(self, main_html_doc, ratings_html_doc):
        main_soup = BeautifulSoup(main_html_doc, 'html.parser')
        ratings_soup = BeautifulSoup(ratings_html_doc, 'html.parser')
        ratings_data = dict(
            zip(['construction_quality', 'worth_buying', 'innovation', 'feature', 'ease_of_use', 'design'],
                self.get_ratings(ratings_soup)
                )
        )
        data = {
            'title': self.get_title(main_soup),
            'price': self.get_price(main_soup),
            'prev_price': self.get_prev_price(main_soup),
            'image_url': self.get_image_link(main_soup)
        }
        data.update(ratings_data)
        return data

    @staticmethod
    def get_title(soup):
        title_tage = soup.find('h1', attrs={'class': 'c-product__title'})
        if title_tage:
            return title_tage.text.strip()
        return None

    @staticmethod
    def get_price(soup):
        price_tage = soup.find('div', attrs={'class': 'c-product__seller-price-pure'})
        if price_tage:
            return price_tage.text.strip()
        return None

    @staticmethod
    def get_prev_price(soup):
        prev_price_tage = soup.find('div', attrs={'class': 'c-product__seller-price-prev'})
        if prev_price_tage:
            return prev_price_tage.text.strip()
        return None

    @staticmethod
    def get_image_link(soup):
        image_tag = soup.find('img', attrs={'class': 'js-gallery-img'})
        if image_tag:
            return image_tag.get('data-src')
        return None

    @staticmethod
    def get_ratings(soup):
        rating_tags = soup.find_all('span', attrs={'class': 'c-rating__overall-word'})
        return [rating_tag.text for rating_tag in rating_tags]
