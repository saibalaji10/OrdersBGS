from fpdf import FPDF
import threading
from django.core.mail import EmailMessage
from .printerconstants import *


class OrderPrinter(FPDF):

    def __init__(self, orders_list):
        super().__init__()
        self.orders_list = orders_list

    def get_name(self):
        name = 'NIL'
        try:
            if (self.orders_list):
                name = str(self.orders_list[0].order.customer.name)
                if not name:
                    name = 'NIL'
        except:
            print('Exception while getting name for pdf')
        finally:
            return name

    def get_phone_number(self):
        number = 'NIL'
        try:
            if (self.orders_list):
                number = str(self.orders_list[0].order.customer.number)
                if not number:
                    number = 'NIL'
        except:
            print('Exception while getting name for pdf')
        finally:
            return number

    def get_date(self):
        try:
            if (self.orders_list):
                return self.orders_list[0].order.date.strftime("%d/%m/%y")
            return 'NIL'
        except:
            print('Exception while getting name for pdf')

    def get_time(self):
        try:
            if (self.orders_list):
                return self.orders_list[0].order.date.strftime("%H:%M %p")
            return 'NIL'

        except:
            print('Exception while getting name for pdf')

    def header(self):
        self.set_font(FONT, 'B', TITLE_FONT_SIZE)
        self.cell(80)
        self.image('bgs.png', w=30, h=30)
        self.ln(10)
        self.cell(CELL_WIDTH, CELL_HEIGHT, 'Name: ' + self.get_name(), 0, 0, 'L')
        self.cell(70)
        self.cell(CELL_WIDTH, CELL_HEIGHT, 'Order Date: ' + self.get_date(), 0, 0, 'L')
        self.ln()
        self.cell(CELL_WIDTH, CELL_HEIGHT, 'Phone: ' + self.get_phone_number(), 0, 0, 'L')
        self.cell(70)
        self.cell(CELL_WIDTH, CELL_HEIGHT, 'Time: ' + self.get_time(), 0, 0, 'L')
        self.ln()
        self.cell(60)
        self.cell(CELL_WIDTH, CELL_HEIGHT, 'Order List', 0, 0, 'C')

        self.ln(20)

    # Page footer
    def footer(self):
        self.set_y(-15)
        self.set_font(FONT, '', 8)
        self.cell(0, CELL_HEIGHT, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def print_title(self):
        self.cell(18)
        self.cell(90, CELL_HEIGHT, 'PRODUCT', 1, 0, 'C')
        self.cell(30, CELL_HEIGHT, 'VARIANT', 1, 0, 'C')
        self.cell(30, CELL_HEIGHT, 'QTY.', 1, 0, 'C')

        self.ln()

    def print_body(self):
        self.set_font(FONT, '', BODY_FONT_SIZE)
        for item in self.orders_list:
            self.cell(18)
            self.cell(90, CELL_HEIGHT, item.product_attribute.product.name, 1, 0, 'C')
            self.cell(30, CELL_HEIGHT, item.product_attribute.attribute.name, 1, 0, 'C')
            self.cell(30, CELL_HEIGHT, str(item.quantity), 1, 0, 'C')
            self.ln()

    def send_mail(self):
        """attachment = self.pdf.output('Order.pdf', 'S')
        mail  = EmailMessage("Order", "Please find the attached order pdf", to=["mynameisbaju@gmail.com"])
        mail.attach('Orders.pdf', attachment, 'application/pdf')
        mail.content_subtype = "html"
        mail.send(fail_silently=True)"""

    def print_orders(self):
        self.alias_nb_pages()
        self.add_page()
        self.set_font(FONT, '', BODY_FONT_SIZE)
        self.print_title()
        self.print_body()
        self.send_mail()

    def execute_action(self):
        try:
            printer_thread = threading.Thread(target=self.print_orders, name='printer_thread')
            printer_thread.start()
        except:
            print('Exception while executing the printer thread')

    def download_pdf(self):
        try:
            self.print_orders()
            pdf_string = self.output('Order.pdf', 'S')
            return pdf_string
        except:
            print('Exception while executing the printer thread')
